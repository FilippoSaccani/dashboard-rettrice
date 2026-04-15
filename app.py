import flask
from query import *
from datetime import datetime, date

app = flask.Flask(__name__)


@app.route('/')
@app.route('/admin')
@app.route('/social')
def root():
    return flask.render_template('index.html')

@app.route('/admin/social', methods=['POST'])
def admin_form():
    dati = flask.request.json

    if dati['social'] not in [row['nome'] for row in get_social()]:
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


@app.route('/social/<social_name>')
def social(social_name):
    rows = get_dati(social_name)
    return flask.jsonify([dict(row) for row in rows])

@app.route('/rassegne')
def rassegne():
    rows = get_rassegne()
    return flask.jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=51852)
