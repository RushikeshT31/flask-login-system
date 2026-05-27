from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)

app.secret_key = "secretkey"


# DATABASE CONNECTION
def connect_db():

    conn = sqlite3.connect('users.db')

    conn.row_factory = sqlite3.Row

    return conn


# CREATE TABLE
conn = connect_db()

conn.execute('''

CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT,

    password TEXT
)

''')

conn.commit()

conn.close()


# HOME PAGE
@app.route('/')
def home():

    return render_template('index.html')


# REGISTER PAGE
@app.route('/register')
def register_page():

    return render_template('register.html')


# REGISTER USER
@app.route('/register_user', methods=['POST'])
def register_user():

    name = request.form['name']

    email = request.form['email']

    password = request.form['password']

    conn = connect_db()

    conn.execute(

        "INSERT INTO users(name,email,password) VALUES(?,?,?)",

        (name, email, password)
    )

    conn.commit()

    conn.close()

    return '''

    <script>

    alert("✅ Registration Successful");

    window.location.href="/";

    </script>

    '''


# LOGIN USER
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']

    password = request.form['password']

    conn = connect_db()

    user = conn.execute(

        "SELECT * FROM users WHERE email=? AND password=?",

        (email, password)

    ).fetchone()

    conn.close()

    if user:

        session['user'] = user['name']

        return '''

        <script>

        alert("✅ Login Successful");

        window.location.href="/dashboard";

        </script>

        '''

    return '''

    <body style="

    background: linear-gradient(to right,#ff0000,#8b0000);

    font-family:Arial;

    display:flex;

    justify-content:center;

    align-items:center;

    height:100vh;">

    <div style="

    background:rgba(255,255,255,0.15);

    backdrop-filter:blur(12px);

    padding:50px;

    border-radius:20px;

    text-align:center;

    color:white;

    border:1px solid rgba(255,255,255,0.3);

    box-shadow:0px 10px 30px rgba(0,0,0,0.4);">

    <h1>

    ❌ Login Failed

    </h1>

    <h2>

    Incorrect Email or Password

    </h2>

    <p>

    Please Try Again

    </p>

    <a href="/">

    <button style="

    padding:15px 30px;

    background:#1877f2;

    color:white;

    border:none;

    border-radius:10px;

    cursor:pointer;

    font-size:18px;">

    Try Again

    </button>

    </a>

    </div>

    </body>

    '''


# DASHBOARD
@app.route('/dashboard')
def dashboard():

    if 'user' in session:

        return render_template(

            'dashboard.html',

            name=session['user']
        )

    return redirect('/')


# VIEW ALL USERS
@app.route('/users')
def users():

    conn = connect_db()

    data = conn.execute(

        "SELECT * FROM users"

    ).fetchall()

    conn.close()

    return render_template(

        'users.html',

        users=data
    )

# LOGOUT
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/')


# RUN APP
if __name__ == '__main__':

    app.run(

        host='0.0.0.0',

        port=5000,

        debug=True
    )

