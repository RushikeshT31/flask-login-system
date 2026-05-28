from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)

app.secret_key = "secretkey"


# DATABASE CONNECTION
def connect_db():

    conn = psycopg2.connect(

        host="dpg-d8btmht7vvec73c64460-a.oregon-postgres.render.com",

        database="login_system_pnqk",

        user="login_system_pnqk_user",

        password="YOUR_RENDER_PASSWORD",

        port="5432",

        sslmode="require"
    )

    return conn


# CREATE TABLE
conn = connect_db()

cur = conn.cursor()

cur.execute('''

CREATE TABLE IF NOT EXISTS users(

    id SERIAL PRIMARY KEY,

    name VARCHAR(100),

    email VARCHAR(100) UNIQUE,

    password VARCHAR(100)
)

''')

conn.commit()

cur.close()

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

    cur = conn.cursor()

    try:

        cur.execute(

            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",

            (name, email, password)
        )

        conn.commit()

        cur.close()

        conn.close()

        return redirect('/')

    except:

        cur.close()

        conn.close()

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

        ⚠ Email Already Exists

        </h1>

        <p>

        Please Use Another Email

        </p>

        <a href="/register">

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


# LOGIN USER
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']

    password = request.form['password']

    conn = connect_db()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM users WHERE email=%s AND password=%s",

        (email, password)

    )

    user = cur.fetchone()

    cur.close()

    conn.close()

    if user:

        session['user'] = user[1]

        return redirect('/dashboard')

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


# VIEW USERS
@app.route('/users')
def users():

    conn = connect_db()

    cur = conn.cursor()

    cur.execute("SELECT * FROM users")

    data = cur.fetchall()

    cur.close()

    conn.close()

    return render_template(

        'users.html',

        users=data
    )


# CLEAR DATABASE
@app.route('/clear')
def clear_database():

    conn = connect_db()

    cur = conn.cursor()

    cur.execute("DELETE FROM users")

    conn.commit()

    cur.close()

    conn.close()

    return redirect('/users')


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