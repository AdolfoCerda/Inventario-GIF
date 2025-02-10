from flask import Flask, request, jsonify, session
from flask_cors import CORS
from psycopg2 import connect, sql

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)  # Habilitar CORS para todas las rutas bajo /api

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

# Login usuario
@app.post('/api/login')
def login():
    datos = request.get_json()  # Obtener los datos JSON de la solicitud
    usuario = datos.get("usuario")
    password = datos.get("password")

    if not usuario or not password:
        return jsonify({"mensaje": "Usuario y contraseña requeridos", "status": "error"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("SELECT * FROM admin.usuarios WHERE vuser = %s AND vpassword = %s")
        cursor.execute(query, (usuario, password))
        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if resultado:
            session['vuser'] = usuario
            return jsonify({"mensaje": "Inicio de Sesión Exitoso", "status": "ok"}), 200
        else:
            return jsonify({"mensaje": "Datos Incorrectos", "status": "error"}), 401

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
    
@app.route('/check-session', methods=['GET'])
def check_session():
    if 'user' in session:  # Verifica si el usuario está en sesión
        return jsonify({"authenticated": True})
    return jsonify({"authenticated": False}), 401
    
@app.post('/api/activo')
def activo():
    datos = request.get_json()  # Obtener el serial para buscar activo
    serial = datos.get("serial")

    conn = get_connection()
    cursor = conn.cursor()
    query = sql.SQL("SELECT * FROM admin.equipos WHERE vserial = %s")
    cursor.execute(query, (serial))
    resultado = cursor.fetchall()
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)