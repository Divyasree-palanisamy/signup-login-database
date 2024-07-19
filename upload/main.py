
import mysql.connector
from flask import Flask, render_template, request, redirect, flash, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Divya@2004",
    database="dd"
)
mycursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/available', methods=['GET', 'POST'])
def available():
    return render_template('available_internships.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    return render_template('recommended_internships.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        
        mycursor.execute(sql, values)
        result = mycursor.fetchone()

        if result:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password. Please try again.", 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql_check_user = "SELECT * FROM users WHERE username = %s"
        mycursor.execute(sql_check_user, (username,))
        existing_user = mycursor.fetchone()

        if existing_user:
            flash("Username already exists. Please choose a different username.", 'error')
            return redirect(url_for('signup'))

        sql_insert_user = "INSERT INTO users (username, password) VALUES (%s, %s)"
        mycursor.execute(sql_insert_user, (username, password))
        mydb.commit()

        flash("Signup successful! Please login with your credentials.", 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        flash('You are not logged in. Please log in first.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('You have been logged out successfully.')
    else:
        flash('You are not logged in.')

    return redirect(url_for('login'))





if __name__ == '__main__':
    app.run(debug=True)
