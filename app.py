import threading
import flask
from flask import send_file

from functions import *

app = flask.Flask(__name__)

status = {"done": False, "error": False}

@app.route('/')
@app.route('/admin')
@app.route('/social')
def root():
    return flask.render_template('index.html')

@app.route('/admin/add-dati-social', methods=['POST'])
def send_form_social():
    dati = flask.request.json

    if dati['social'] not in [row['nome'] for row in select_social()]:
        return "Social media non valido", 400

    if int(dati['visualizzazioni']) < 0:
        return "Numero di visualizzazioni non valido", 400

    if int(dati['interazioni']) < 0:
        return "Numero di interazioni non valido", 400

    if int(dati['follower']) < 0:
        return "Numero di followers non valido", 400

    try:
        giorno = datetime.strptime(dati['giorno'], '%Y-%m-%d').date()
    except ValueError:
        return 'Formato data non valido, usa yyyy-mm-dd', 400

    if giorno > date.today():
        return 'La data non può essere successiva ad oggi', 400

    try:
        ok, errore = insert_dati(dati)

        if not ok:
            return errore, 400
        else:
            return 'ok', 200
    except Exception as e:
        return "Errore nell'archiviazione dei dati", 400

@app.route('/social/<social_name>', methods=['GET'])
def get_dati_social(social_name):
    rows = select_dati_social(social_name)
    return flask.jsonify([dict(row) for row in rows])

@app.route('/admin/latest', methods=['GET'])
def get_latest():
    rows = select_latest()
    return flask.jsonify([dict(row) for row in rows])

@app.route('/admin/add-rassegna', methods=['POST'])
def send_form_rassegna():
    try:
        global status
        status["done"] = False
        status["error"] = False

        file = flask.request.files.getlist('file')[0]
        giorno = flask.request.form.get('giorno')
        data = get_date_from_formatted(giorno)

        new_filename = 'Unimore'+giorno+".pdf"

        ok, error = save_pdf(file, data, new_filename)

        if not ok:
            print(error)
            status["done"] = True
            status["error"] = True
            return error, 400

        if not ok:
            print(error)
            status["done"] = True
            status["error"] = True
            return error, 400

        thread = threading.Thread(target=process_pdf, args=(new_filename, data, status))
        thread.daemon = False
        thread.start()

        return 'ok', 200
    except Exception as e:
        print(e)
        return "Errore nell'archiviazione dei dati", 400

@app.route('/index/all-rassegne', methods=["GET"])
def get_all_rassegne():
    rows = select_all_rassegne()
    return flask.jsonify([json.loads(dict(row)['risultato']) for row in rows])

@app.route('/index/all-rassegne-per-scala', methods=["GET"])
def get_all_rassegne_per_scala():
    rows = select_rassegne_per_scala()
    return flask.jsonify([json.loads(dict(row)['risultato']) for row in rows])

@app.route('/index/all-rassegne-per-testata', methods=["GET"])
def get_all_rassegne_per_testata():
    rows = select_rassegne_per_testata()
    print([json.loads(dict(row)['risultato']) for row in rows])
    return flask.jsonify([json.loads(dict(row)['risultato']) for row in rows])

@app.route('/index/all-temi', methods=["GET"])
def get_all_temi():
    rows = select_all_temi()
    return flask.jsonify([dict(row)['nome'] for row in rows])

@app.route('/index/all-scale', methods=["GET"])
def get_all_scale():
    rows = select_all_scale()
    return flask.jsonify([dict(row)['nome'] for row in rows])

@app.route('/index/all-testate-importanti', methods=["GET"])
def get_all_testate_importanti():
    rows = select_testate_importanti()
    return flask.jsonify([dict(row)['nome'] for row in rows])

@app.route('/index/search-rassegne', methods=["GET"])
def search():
    query = flask.request.args.get('q', '').strip()
    if not query:
        return flask.jsonify([])

    # FTS5 usa una sintassi speciale — caratteri come ( ) " vanno escaped
    # per evitare errori se l'utente digita qualcosa di strano
    safe_query = query.replace('"', '""')

    results = search_rassegne(f'"{safe_query}"')

    return flask.jsonify(results)

@app.route('/general/file', methods=["GET"])
def get_file():
    filename = flask.request.args.get('filename')
    data = get_date_from_formatted(flask.request.args.get('data'))

    try:
        print(data)
        path = os.path.join(get_pdf_folder(data), filename)
        return send_file(path, filename), 200
    except Exception as e:
        return str(e), 400

@app.route('/admin/delete', methods=["DELETE"])
def delete():
    dati = flask.request.json

    if dati["tipo"] == 'rassegna':
        ok, error = delete_rassegna(dati["giorno"])

        if not ok:
            print(error)
            return error, 400

        path = get_pdf_folder(get_date_from_formatted(dati["giorno"]))

        ok, error = delete_pdf(os.path.join(path, dati["nome"]))

        if not ok:
            print(error)
            return error, 400
    else:
        ok, error = delete_dato_social(dati["nome"], dati["giorno"])

        if not ok:
            print(error)
            return error, 400
    return '', 200

@app.route("/status")
def get_status():
    return flask.jsonify(status)

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=51852)
