from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2 import connect, sql

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Habilitar CORS para todas las rutas bajo /api

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
            return jsonify({"mensaje": "Inicio de Sesión Exitoso", "status": "ok"}), 200
        else:
            return jsonify({"mensaje": "Datos Incorrectos", "status": "error"}), 401

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
    
@app.post('/api/activo')
def activo():
    datos = request.get_json()
    serial = datos.get("serial")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            e.*,
            s.vNombre AS sitio_nombre,
            a.vNombre AS ambiente_nombre,
            t.vNombre AS tipo_nombre,
            m.vNombre AS marca_nombre,
            sv.vNombre AS servicio_nombre,
            d.vNombre AS dueño_nombre
        FROM admin.equipos e
        LEFT JOIN admin.sitios s ON e.iSitio = s.iId
        LEFT JOIN admin.ambientes a ON e.iAmbiente = a.iId
        LEFT JOIN admin.tipos t ON e.iTipo = t.iId
        LEFT JOIN admin.marcas m ON e.iMarca = m.iId
        LEFT JOIN admin.servicios sv ON e.iServicio = sv.iId
        LEFT JOIN admin.dueños d ON e.iDueño = d.iId
        WHERE e.vserial = %s
    """
    
    cursor.execute(query, (serial,))
    resultado = cursor.fetchall()
    return jsonify(resultado)

@app.route('/api/options/<tabla>', methods=['GET'])
def obtener_opciones(tabla):
    try:
        # Definir tablas permitidas explícitamente
        tablas_permitidas = {
            "Sitios": "sitios",
            "Ambientes": "ambientes",
            "Tipos": "tipos",
            "Marcas": "marcas",
            "Servicios": "servicios",
            "Dueños": "dueños"
        }

        # Validar si la tabla solicitada está permitida
        if tabla not in tablas_permitidas:
            return jsonify({"error": "Tabla no permitida"}), 400

        # Obtener el nombre de la tabla segura
        nombre_tabla = tablas_permitidas[tabla]

        # Conectar y ejecutar la consulta de manera segura
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("SELECT vNombre FROM admin.{}").format(sql.Identifier(nombre_tabla))
        cursor.execute(query)
        resultado = cursor.fetchall()
        cursor.close()
        conn.close()

        # Convierte el resultado a una lista de cadenas
        opciones = [fila[0] for fila in resultado]
        return jsonify(opciones)

    except Exception as e:
        print(f"Error al obtener opciones de {tabla}: {e}")  # Detalle de error en consola
        return jsonify({"error": "Error interno del servidor", "status": "error"}), 500
        return jsonify({"error": str(e), "status": "error"}), 500

if __name__ == '__main__':
    app.run(debug=True)