from flask import Flask, redirect, url_for, render_template, request, session, jsonify
from datetime import timedelta
import mysql.connector


app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


@app.route('/')
def landing_page():  # put application's code here
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():  # put application's code here
    return render_template('home.html')


@app.route('/contact')
def contact_page():  # put application's code here
    return render_template('contact.html')


@app.route('/assignment3_1')
def assignment_page():  # put application's code here
    db_user_name = 'shay'  # change this to ted or something to see the if statement
    db_web_cost = 195354.45712
    db_subject = 'Songs'
    db_top4_songs = ('In The Beginning - knaan', 'Fix You - coldplay',
                     'Ill make a man - Mulan', 'Latinos - Proyecto Uno')
    db_rest_of_songs = ('macarena', 'thunderstruck', 'oops i did it again', 'sk8er boy',
                        'bye bye bye', 'i want it that way', 'ice ice baby')
    return render_template('assignment3_1.html',
                           user_name=db_user_name,
                           web_cost=db_web_cost,
                           subject=db_subject,
                           top4=db_top4_songs,
                           rest=db_rest_of_songs)


ppl = {
    "user1": {"name": "Yossi", "email": "yo@gmail.com", "user_name": "Yos"},
    "user2": {"name": "Ron", "email": "ron@gmail.com", "user_name": "Rono"},
    "user3": {"name": "Jim", "email": "tuna@gmail.com", "user_name": "Jimbo"},
    "user4": {"name": "Ryan", "email": "fire@gmail.com", "user_name": "Ryano"},
    "user5": {"name": "Creed", "email": "QA@gmail.com", "user_name": "Creedoo"}
}
user_dict = {
    'Yos': '1111',
    'Rono': '2222',
    'Jimbo': '3333',
    'Ryano': '4444',
    'Creedoo': '5555',
}


@app.route('/assignment3_2', methods=['GET', 'POST'])
def assignment2_page():  # put application's code here
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in user_dict:
            pas_in_dict = user_dict[username]
            if pas_in_dict == password:
                session['username'] = username
                session['logedin'] = True
                return render_template('assignment3_2.html',
                                       message='Success',
                                       username=username)
            else:
                return render_template('assignment3_2.html',
                                       message='Wrong password!')
        else:
            return render_template('assignment3_2.html',
                                   message='Please sign in!')

    if 'name' in request.args:
        name = request.args["name"]
        if name == '':
            return render_template('assignment3_2.html', ppl=ppl)
        chosen = None
        for user_name in ppl.values():
            if user_name['name'] == name:
                chosen = user_name
                break
        if chosen:
            return render_template('assignment3_2.html',
                                   name=chosen['name'],
                                   email=chosen['email'],
                                   user_name=chosen['user_name'])
        else:
            return render_template('assignment3_2.html',
                                   message2='No user found, sorry about that')
    return render_template('assignment3_2.html',
                           ppl=ppl)


@app.route('/log_out')
def logout_func():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('assignment2_page'))


@app.route('/session')
def session_func():
    # print(session['CHECK'])
    return jsonify(dict(session))


# assignment 4
from pages.assignment_4.assignment_4 import assignment_4
app.register_blueprint(assignment_4)




if __name__ == '__main__':
    app.run()
