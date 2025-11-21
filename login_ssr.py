from flask import Flask, render_template, request, redirect, session, flash
import pymysql
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_segura")  # Necesaria para usar sesiones

# Configuración de la base de datos
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')

        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Verifica si el usuario existe y la contraseña coincide
        sql = "SELECT * FROM users WHERE user = %s AND password = %s"
        cursor.execute(sql, (usuario, contrasena))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            session['usuario'] = usuario
            return redirect('/dashboard')
        else:
            flash('Credenciales incorrectas. Intenta de nuevo.')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' in session:
        return f"Bienvenido, {session['usuario']}!"
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect('/')
