import flask

app = flask.Flask(__name__)

@app.route('/')
def root():  # put application's code here
    return flask.redirect('/admin')

@app.route('/social')
def social():
    return flask.render_template('social.html')

@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/admin')
def admin():
    return flask.render_template('admin.html')

@app.route('/admin_old')
def admin2():
    return flask.render_template('admin_old.html')

if __name__ == '__main__':
    app.run()
