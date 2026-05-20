import threading
from datetime import datetime

import flask
from flask import send_file, jsonify, request

from python.functions import *
from python.query import *

port = int(os.environ.get("PORT", 51852))
status = {"done": False, "error": False}

app = flask.Flask(__name__)

# Helper per ridurre la ripetizione jsonify + dict
def rows_to_json(rows, key=None):
    result = [dict(r) for r in rows]
    if key:
        return jsonify([r[key] for r in result])
    return jsonify(result)

def error(msg, code=400):
    return msg, code

# --- Pagine ---

@app.route('/')
@app.route('/admin')
@app.route('/social')
def root():
    return flask.render_template('index.html')

# --- Social ---

@app.route('/admin/add-dati-social', methods=['POST'])
def send_form_social():
    dati = flask.request.json

    if dati['social'] not in [r['nome'] for r in select_social()]:
        return error("Social media non valido")
    if int(dati['visualizzazioni']) < 0:
        return error("Numero di visualizzazioni non valido")
    if int(dati['interazioni']) < 0:
        return error("Numero di interazioni non valido")
    if int(dati['follower']) < 0:
        return error("Numero di followers non valido")

    try:
        giorno = datetime.strptime(dati['giorno'], '%Y-%m-%d').date()
    except ValueError:
        return error('Formato data non valido, usa yyyy-mm-dd')

    if giorno > date.today():
        return error('La data non può essere successiva ad oggi')

    ok, err = insert_dati(dati)
    if ok:
        return 'ok', 200
    else:
        app.logger.error(f"Errore nell'inserimento dei dati: {err}")
        return error(err)

@app.route('/social/<social_name>', methods=['GET'])
def get_dati_social(social_name):
    return rows_to_json(select_dati_social(social_name))

# --- Testate ---

@app.route('/admin/testate', methods=["GET"])
def get_controllo_testate():
    return rows_to_json(controllo_testate())

@app.route('/admin/conferma', methods=["PUT"])
def conferma():
    ok, err = conferma_testata(request.json)
    return ('', 200) if ok else error(err)

# --- Rassegne ---

@app.route('/admin/add-rassegna', methods=['POST'])
def send_form_rassegna():
    global status
    status = {"done": False, "error": False}

    try:
        file    = request.files.getlist('file')[0]
        giorno  = request.form.get('giorno')
        data    = get_date_from_formatted(giorno)
        nome    = get_pdf_name(giorno)

        ok, err = save_pdf(file, data, nome)
        if not ok:
            status = {"done": True, "error": True}
            app.logger.error(f"{err}")
            return error(err)

        threading.Thread(
            target=process_pdf,
            args=(nome, data, status),
            daemon=False
        ).start()

        return 'ok', 200
    except Exception as err:
        app.logger.error(f"Errore nell'archiviazione dei dati: {err}")
        return error("Errore nell'archiviazione dei dati")

@app.route('/admin/delete', methods=["DELETE"])
def delete():
    dati = request.json

    if dati["tipo"] == 'rassegna':
        ok, err = delete_rassegna(dati["giorno"])
        if not ok:
            app.logger.error(f"Errore nell'eliminazione della rassegna: {err}")
            return error(err)

        path = os.path.join(get_pdf_folder(get_date_from_formatted(dati["giorno"])), dati["nome"])
        ok, err = delete_pdf(path)
        if not ok:
            app.logger.error(f"{err}")
            return error(err)
    else:
        ok, err = delete_dato_social(dati["nome"], dati["giorno"])
        if not ok:
            app.logger.error(f"Errore nell'eliminazione dei dati social: {err}")
            return error(err)

    return '', 200

@app.route('/admin/latest', methods=['GET'])
def get_latest():
    return rows_to_json(select_latest())

# --- Index ---

@app.route('/index/all-rassegne')
def get_all_rassegne():
    return jsonify([json.loads(dict(r)['risultato']) for r in select_all_rassegne()])

@app.route('/index/all-rassegne-per-scala')
def get_all_rassegne_per_scala():
    return jsonify([json.loads(dict(r)['risultato']) for r in select_rassegne_per_scala()])

@app.route('/index/all-rassegne-per-testata')
def get_all_rassegne_per_testata():
    return jsonify([json.loads(dict(r)['risultato']) for r in select_rassegne_per_testata()])

@app.route('/index/all-temi')
def get_all_temi():
    return rows_to_json(select_all_temi(), key='nome')

@app.route('/index/all-scale')
def get_all_scale():
    return rows_to_json(select_all_scale(), key='nome')

@app.route('/index/all-testate-importanti')
def get_all_testate_importanti():
    return rows_to_json(select_testate_importanti(), key='nome')

@app.route('/index/search-rassegne')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    return jsonify(search_rassegne(f'"{query.replace(chr(34), chr(34)*2)}"'))

@app.route('/index/file')
def get_file():
    giorno = request.args.get('data')
    data   = get_date_from_formatted(giorno)
    path   = os.path.join(get_pdf_folder(data), get_pdf_name(giorno))
    try:
        return send_file(path)
    except Exception as err:
        app.logger.error(f"Errore nell'invio del file: {err}")
        return error(str(err))

# --- General ---

@app.route("/status")
def get_status():
    return flask.jsonify(status)

if __name__ == '__main__':
    app.run(host="0.0.0.0", threaded=True, port=port)
