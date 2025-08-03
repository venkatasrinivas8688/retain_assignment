from flask import Flask, request, jsonify
import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

#previous:keeping global connection
#current:This creates a fresh, isolated connection for each request.
def get_db_connection():
    connection=sqlite3.connect('users.db')
    connection.row_factory=sqlite3.Row 
    return connection 


@app.route('/')
def home():
    #added jsonify and http status code
    return jsonify(message="User Management System"),200

@app.route('/users', methods=['GET'])
def get_all_users():
    #added try catch block and http status codes
    try:
        conn=get_db_connection()
        users=conn.execute("SELECT * FROM users").fetchall()
        conn.close()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    #added http status codes
    conn=get_db_connection()
    user=conn.execute("SELECT * FROM users WHERE id = ?", (user_id)).fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user)),200
    else:
        return jsonify(message="User not found"), 400

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name=data.get('name')
    email=data.get("email")
    password=data.get('password')

    #check if all fields are their or not
    if not all([name,email,password]):
        return jsonify(message='All fields are required'), 400

    #hashing the password 
    hashed_password=generate_password_hash(password)
    try:
        conn=get_db_connection()
        conn.execute('INSERT INTO users (name, email, password) VALUES (?,?,?)',(name,email,hashed_password))
        conn.commit() #saves all the changes made in the current database
        conn.close()
        return jsonify(message="User created successfully!"), 201
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        return jsonify(message="Invalid data, name and email are required"), 400
    try:
        conn=get_db_connection() #The connection to the database (like opening a file)
        cursor=conn.cursor() #The interpreter that runs SQL commands (like a pen writing into the file)
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()
        if cursor.rowcount==0:
            return jsonify(message="User not found"), 400
        return jsonify(message="User updated successfully"),200

    except Exception as e:
        return jsonify(error=str(e)),500


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn=get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify(message="User not found"), 404

        return jsonify(message=f"User {user_id} deleted"), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/search', methods=['GET'])
def search_users():
    name = request.args.get('name')

    if not name:
        return jsonify(message="Please provide a name to search"), 400

    try:
        conn=get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email FROM users WHERE name LIKE ?", ('%' + name + '%',))
        users = cursor.fetchall()
        return jsonify([dict(user) for user in users]), 200
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return jsonify(status="success", user_id=user['id']), 200
    else:
        return jsonify(status="failed", message="Invalid credentials"), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)