from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='employee_db',
        user='root',
        password='suneel123'
    )
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employee ORDER BY id DESC')
    employees = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address= request.form['address']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO employee (name, email, phone, address) VALUES (%s, %s, %s, %s)', (name, email, phone, address))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employee WHERE id = %s', (id,))
    employee = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address= request.form['address']

        cursor = connection.cursor()
        cursor.execute('UPDATE employee SET name = %s, email = %s, phone = %s, address = %s WHERE id = %s', (name, email, phone, address, id))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    connection.close()
    return render_template('update.html', employee=employee)

@app.route('/delete/<int:id>', methods=['DELETE', 'GET'])
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM employee WHERE id = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    
    if request.method == 'DELETE':
        return jsonify({'success': True})
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
