from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                name TEXT,
                phone TEXT,
                password TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                date TEXT,
                time_slot TEXT
            )''')

 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            session['user'] = user[1]
            return redirect(url_for('userview'))
        else:
            return render_template('login.html', message='Invalid username or password.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        
        # Check if the email address already exists in the users table
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        existing_user = c.fetchone()
        if existing_user:
            return render_template('signup.html', message='Email address already exists. Please choose a different one.')

        
        c.execute("INSERT INTO users (username, email, name, phone, password) VALUES (?, ?, ?, ?, ?)",
                  (username, email, name, phone, password))
        conn.commit()
         
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/userview')
def userview():
    if 'user' in session:
        username = session['user']
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        return render_template('userview.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/contact')
def contact():
    return render_template('contactus.html')

@app.route('/submitcontact', methods=['GET', 'POST'])
def contactus():
    return render_template('submitcontact.html')

@app.route('/book_appointment', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time_slot = request.form['time_slot']   
        new_appointment = (name, email, date, time_slot)
        c.execute("INSERT INTO appointments (name, email, date, time_slot) VALUES (?, ?, ?, ?)", new_appointment)
        conn.commit()
        #return redirect(url_for('index'))
    return render_template('bookanAppointment.html')
@app.route('/appointments')
def appointments():
    c.execute("SELECT * FROM appointments")
    appointments = c.fetchall()
    numbered_appointments = [(i + 1, *appointment) for i, appointment in enumerate(appointments)]
    return render_template('bookedAppointments.html', appointments=numbered_appointments)
if __name__ == '__main__':
    app.run(debug=True)
