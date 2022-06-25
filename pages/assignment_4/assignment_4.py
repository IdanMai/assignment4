import mysql.connector
from flask import Blueprint, render_template, request, redirect, jsonify
import requests

assignment_4 = Blueprint('assignment_4', __name__,
                         static_folder='static',
                         template_folder='templates')


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root1234',
                                         database='flaskDB')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)
    #

    if query_type == 'commit':
        # Use for INSERT, UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment_4.route('/assignment_4')
def main():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)


@assignment_4.route('/insert_user', methods=['GET', 'POST'])
def index():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    for user in users_list:
        if name == user.name:
            return render_template('assignment_4.html', users=users_list)

    query = "INSERT INTO users(user_name, name, email, password) VALUES ('%s','%s', '%s', '%s')" % (username, name,
                                                                                                    email, password)
    interact_db(query=query, query_type='commit')
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment_4.html', users=users_list)



@assignment_4.route('/update_user', methods=['GET', 'POST'])
def update_user():
    username = request.form['username']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    id = request.form['id']
    query = "UPDATE users SET name ='%s',email ='%s',password='%s', user_name='%s' WHERE id='%s';" % (name, email, password, username, id)
    print(query)
    interact_db(query=query, query_type='commit')
    return redirect('/assignment_4')


@assignment_4.route('/update_userS', methods=['GET','POST'])
def update_userS():
    id = request.form['id']
    print(id)
    return render_template('updateusers.html',id=id)


@assignment_4.route('/delete_user', methods=['GET', 'POST'])
def delete_user_func():
    user_id = request.form['id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    interact_db(query, query_type='commit')
    return redirect('/assignment_4')


@assignment_4.route('/users', methods=['GET'])
def get_users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    users_array = []
    for user in users_list:
        users_array.append({
            'username': user.user_name,
            'email': user.email,
            'name': user.name
        })
    return jsonify(users_array)


@assignment_4.route('/outer_source', methods=['GET', 'POST'])
def outer_source():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    user_id = request.form['id']
    result = requests.get('https://reqres.in/api/users/' + user_id)
    return render_template('assignment_4.html', user_from_api=result.json()['data'],users=users_list)


@assignment_4.route('/restapi_users/', methods=['GET'])
def get_default_user():
    query = 'select * from users where id=1'
    user = interact_db(query, query_type='fetch')
    return jsonify(user)


@assignment_4.route('/restapi_users/<int:USER_ID>', methods=['GET'])
def get_user(USER_ID):
    query = "select * from users where id='%s'" % USER_ID
    user = interact_db(query, query_type='fetch')
    if user:
        return jsonify(user)
    return jsonify({
        'error': '404',
        'message': 'User not found!!'
    })
#
#
# # ------------------------------------------------- #
# # ------------------------------------------------- #
#
# def up_user():
#     id = request.form['id']
#     name = request.form['name']
#     email = request.form['email']
#     password = request.form['password']
#     query = "UPDATE users SET name ='%s',email ='%s',password='%s'WHERE id='%s';" % (name, email, password,id)
#     interact_db(query=query, query_type='commit')
#     return redirect('/users')
#
#
# def update_user():
#     user_id = request.form['id']
#     return render_template('updateusers.html',username=user_id)
#
# # ------------------------------------------------- #
# # -------------------- DELETE --------------------- #
# # ------------------------------------------------- #
#
# def delete_user_func():
#     user_id = request.form['user_id']
#     query = "DELETE FROM users WHERE id='%s';" % user_id
#     # print(query)
#     interact_db(query, query_type='commit')
#     return redirect('/users')
#
#
# # @app.route('/delete_user', methods=['POST'])
# # def delete_user():
# #     user_id = request.form['id']
# #     query = "DELETE FROM users WHERE id='%s';" % user_id
# #     interact_db(query, query_type='commit')
# #     return redirect('/users')
#
#
# # ------------------------------------------------- #
# # ------------------------------------------------- #
