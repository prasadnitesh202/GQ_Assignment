from flask import Flask, session, render_template, request, redirect, g, url_for
import sqlite3
import os
app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == 'POST'):
        # Drop the session
        session.pop('user', 'None')

        if request.form['username']:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            retrieve_query = "Select password from users WHERE username=?"
            cursor.execute(retrieve_query, (request.form['username'],))
            rows = cursor.fetchone()
            if(rows):
                password = rows[0]
            connection.commit()
            connection.close()

            if(rows):
                if request.form['password'] == password:
                    session['user'] = request.form['username']
                    return redirect(url_for('protected'))

    return render_template('index.html')


@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html', user=session['user'])
    return redirect(url_for('index'))


@app.route('/drop_session')
def dropsession():
    session.pop('user', None)
    return redirect('/')


@app.route('/show_memes')
def show():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    update_query = "UPDATE users SET consent=1 WHERE username=?"
    cursor.execute(update_query, (session['user'],))
    connection.commit()
    connection.close()
    return render_template('memes.html')


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


app.run(port='5000', debug=True)
