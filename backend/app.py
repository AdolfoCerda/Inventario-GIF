from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2 import connect, sql

app = Flask(__name__)
CORS(app) # Habilitar CORS para evitar problemas al conectar el frontend

# Variables para conexión a la base de datos
host = 'localhost'
dbname = 'InventarioGIF'
user = 'postgres'
password = '0000'
port = 5432

# Conexión a la base de datos
def get_connection():
    conn = connect(host=host, database=dbname, user=user, password=password, port=port)
    return conn

@app.get('/')
def home():
    # Probar conexion con una consulta a la bd
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin.usuarios")
    resultado = cursor.fetchall()
    return resultado

# Login usuario
@app.post('/api/login')
def login():
    datos = request.json
    usuario = datos.get("usuario")
    password = datos.get("password")

    if not usuario or not password:
        return jsonify({"mensaje": "Usuario y contraseña requeridos"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("SELECT * FROM usuarios WHERE vuser = %s AND vpassword = %s")
        cursor.execute(query, (usuario, password))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            return jsonify({"mensaje": "Inicio de Sesión Exitoso", "status": "ok"}), 200
        else:
            return jsonify({"mensaje": "Datos Incorrectos", "status": "error"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)