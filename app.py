from flask import Flask, session, render_template, request, redirect, g, url_for, flash, make_response
import requests
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
                    flash("You've successfully logged in!")
                    # print(request.cookies['session'])
                    # ses = request.cookies['session']
                    # res = make_response("Setting a cookie")
                    # res.set_cookie('demo', value=ses, path='/protected')

                    return redirect(url_for('protected'))

    if g.user:
        return redirect(url_for('protected'))

    return render_template('index.html')


@app.route('/protected')
def protected():
    # print(request.cookies)
    if g.user:
        return render_template('protected.html', user=session['user'])
    return redirect(url_for('index'))


@app.route('/drop_session')
def dropsession():
    session.pop('user', None)
    return redirect('/')


@app.route('/show_memes')
def show():
    # print(session['user'])
    if g.user:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = "UPDATE users SET consent=1 WHERE username=?"
        cursor.execute(update_query, (session['user'],))
        connection.commit()
        connection.close()

        response = requests.get('https://api.imgflip.com/get_memes')
        json_data = []
        json_data.append(response.json())
    # print(json_data[0]['data']['memes'])
        use_data = []
        use_data = json_data[0]['data']['memes'][:10]
        keys_to_remove = ["id", "width", "height", "box_count", "name"]
        for dict in use_data:
            for key in keys_to_remove:
                del dict[key]

        print(use_data)
    # print(len(use_data))

    # print(type(response.json()))

        return render_template('memes.html', memes=use_data)
    return redirect(url_for('index'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
