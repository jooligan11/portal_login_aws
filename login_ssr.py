from flask import Flask, render_template, request, redirect, session, flash
import pymysql
import boto3
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_segura")  # Necesaria para usar sesiones

def get_db_config():
    secret_name = "rds/loginapp"   # nombre de tu secreto en Secrets Manager
    region_name = "eu-north-1"     # región donde lo guardaste

    client = boto3.client("secretsmanager", region_name=region_name)
    secret = client.get_secret_value(SecretId=secret_name)
    secret_dict = json.loads(secret["SecretString"])

    return {
        "host": secret_dict["host"],
        "port": int(secret_dict.get("port", 3306)),
        "user": secret_dict["username"],
        "password": secret_dict["password"],
        "database": secret_dict["dbname"]
    }

# Configuración de la base de datos desde Secrets Manager
db_config = get_db_config()

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
