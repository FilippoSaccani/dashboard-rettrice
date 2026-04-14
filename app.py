import flask

app = flask.Flask(__name__)


@app.route('/')
@app.route('/admin')
@app.route('/social')
def root():  # put application's code here
    return flask.render_template('index.html')

@app.route('/admin', methods=['POST'])
def admin():
    return flask.redirect('/admin')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
