from flask import Flask, request, jsonify
from flask_cors import CORS
from psycopg2 import connect, sql
from datetime import date
import os
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Habilitar CORS para todas las rutas bajo /api
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Ruta para archivo temporal

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

# "Eliminar" activo, es decir cambiar estatus a inactivo y actualizar fecha de estatus  
@app.put('/api/activo/eliminar')
def eliminar_activo():
    datos = request.get_json()
    serial = datos.get("serial")

    if not serial:
        return jsonify({"mensaje": "Serial requerido", "status": "error"}), 400

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Actualizar los campos vEstatus y dFechaEstatus
        query = """
            UPDATE admin.equipos
            SET vEstatus = 'Inactivo', dFechaEstatus = %s
            WHERE vSerial = %s
        """
        cursor.execute(query, (date.today(), serial))
        conn.commit()

        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"mensaje": "Activo eliminado correctamente", "status": "ok"}), 200
        else:
            return jsonify({"mensaje": "Activo no encontrado", "status": "error"}), 404

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
    
@app.post('/api/activos/agregar')
def agregar_activo():
    datos = request.get_json()
    
    # Extraer datos de la petición
    vSerial = datos.get("serial")
    vNombre = datos.get("nombre")
    if datos.get("encendido") == "Si":
        bEncendido = True
    else:
        bEncendido = False
    dFechaEstatus = date.today()
    vCluster = datos.get("cluster")
    vChassis = datos.get("chassis")
    vBahia = datos.get("bahia")
    vModelo = datos.get("modelo")
    iNucleos = datos.get("nucleos")
    iMemoria = datos.get("memoria")
    dFechaInicioSoporte = datos.get("fechaInicioSoporte")
    dFechaFinSoporte = datos.get("fechaFinSoporte")
    dFechaFinVida = datos.get("fechaFinVida")
    vIpRed = datos.get("ipRed")
    vIpILO = datos.get("ipILO")
    iHDD = datos.get("hdd")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Obtener ID a partir del texto en catalogos
        def get_catalog_id(table, name):
            query = sql.SQL("SELECT iId FROM admin.{} WHERE vNombre = %s").format(sql.Identifier(table))
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None

        iSitio = get_catalog_id('sitios', datos.get("sitio"))
        iAmbiente = get_catalog_id('ambientes', datos.get("ambiente"))
        iTipo = get_catalog_id('tipos', datos.get("tipo"))
        iMarca = get_catalog_id('marcas', datos.get("marca"))
        iServicio = get_catalog_id('servicios', datos.get("servicio"))
        iDueño = get_catalog_id('dueños', datos.get("dueño"))

        # Verificar que todos los IDs hayan sido recuperados correctamente
        if None in (iSitio, iAmbiente, iTipo, iMarca, iServicio, iDueño):
            return jsonify({"mensaje": "Datos de catálogo inválidos", "status": "error"}), 400

        # Query para agregar
        query = """
            INSERT INTO admin.equipos (
                iSitio, vNombre, bEncendido, vEstatus, dFechaEstatus, 
                iAmbiente, iTipo, vCluster, vChassis, vBahia, 
                iMarca, vModelo, vSerial, iNucleos, iMemoria, 
                iServicio, dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida, 
                vIpRed, vIpILO, iDueño, iHDD
            ) VALUES (
                %s, %s, %s, 'Activo', %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
        """
        cursor.execute(query, (
            iSitio, vNombre, bEncendido, dFechaEstatus, 
            iAmbiente, iTipo, vCluster, vChassis, vBahia, 
            iMarca, vModelo, vSerial, iNucleos, iMemoria, 
            iServicio, dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida, 
            vIpRed, vIpILO, iDueño, iHDD
        ))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Equipo agregado correctamente", "status": "ok"}), 201

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
    
@app.post('/api/activos/actualizar')
def actualizar_activo():
    datos = request.get_json()
    
    # Extraer datos de la petición
    vSerial = datos.get("serial")
    vNombre = datos.get("nombre")
    if datos.get("encendido") == "Si":
        bEncendido = True
    else:
        bEncendido = False
    vCluster = datos.get("cluster")
    vChassis = datos.get("chassis")
    vBahia = datos.get("bahia")
    vModelo = datos.get("modelo")
    iNucleos = datos.get("nucleos")
    iMemoria = datos.get("memoria")
    dFechaInicioSoporte = datos.get("fechaInicioSoporte")
    dFechaFinSoporte = datos.get("fechaFinSoporte")
    dFechaFinVida = datos.get("fechaFinVida")
    vIpRed = datos.get("ipRed")
    vIpILO = datos.get("ipILO")
    iHDD = datos.get("hdd")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Obtener ID a partir del texto en catalogos
        def get_catalog_id(table, name):
            query = sql.SQL("SELECT iId FROM admin.{} WHERE vNombre = %s").format(sql.Identifier(table))
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None

        iSitio = get_catalog_id('sitios', datos.get("sitio"))
        iAmbiente = get_catalog_id('ambientes', datos.get("ambiente"))
        iTipo = get_catalog_id('tipos', datos.get("tipo"))
        iMarca = get_catalog_id('marcas', datos.get("marca"))
        iServicio = get_catalog_id('servicios', datos.get("servicio"))
        iDueño = get_catalog_id('dueños', datos.get("dueño"))

        # Verificar que todos los IDs hayan sido recuperados correctamente
        if None in (iSitio, iAmbiente, iTipo, iMarca, iServicio, iDueño):
            return jsonify({"mensaje": "Datos de catálogo inválidos", "status": "error"}), 400

        # Query para actualizar
        query = """
            UPDATE admin.equipos SET
                iSitio = %s, vNombre = %s, bEncendido = %s, 
                iAmbiente = %s, iTipo = %s, vCluster = %s, 
                vChassis = %s, vBahia = %s, iMarca = %s, 
                vModelo = %s, iNucleos = %s, iMemoria = %s, 
                iServicio = %s, dFechaInicioSoporte = %s, 
                dFechaFinSoporte = %s, dFechaFinVida = %s, 
                vIpRed = %s, vIpILO = %s, iDueño = %s, iHDD = %s
            WHERE vSerial = %s
        """
        cursor.execute(query, (
            iSitio, vNombre, bEncendido, 
            iAmbiente, iTipo, vCluster, 
            vChassis, vBahia, iMarca, 
            vModelo, iNucleos, iMemoria, 
            iServicio, dFechaInicioSoporte, 
            dFechaFinSoporte, dFechaFinVida, 
            vIpRed, vIpILO, iDueño, iHDD, vSerial
        ))
        
        conn.commit()
        cursor.close()
        conn.close()

        if cursor.rowcount > 0:
            return jsonify({"mensaje": "Equipo actualizado correctamente", "status": "ok"}), 200
        else:
            return jsonify({"mensaje": "Equipo no encontrado para actualizar", "status": "error"}), 404

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

# Carga masiva de activos
@app.post('/api/upload')
def upload_file():
    file = request.files['file']
    commits = 0

    # Guardar el archivo temporalmente
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        # Leer el archivo Excel
        dataframe = pd.read_excel(file_path)
        
        conn = get_connection()
        cursor = conn.cursor()

        # Function to get the ID from a name in a catalog table
        def get_catalog_id(table, name):
            query = sql.SQL("SELECT iId FROM admin.{} WHERE vNombre = %s").format(sql.Identifier(table))
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None

        # Iterar sobre las filas del DataFrame
        for index, row in dataframe.iterrows():

            # Si el campo 'sitio' (primera columna) está vacío, detener el proceso
            if pd.isna(row.iloc[1]):
                break

            # Mapear y validar los datos
            sitio = get_catalog_id('sitios', row.iloc[1])
            ambiente = get_catalog_id('ambientes', row.iloc[4])
            tipo = get_catalog_id('tipos', row.iloc[5])
            marca = get_catalog_id('marcas', row.iloc[9])
            servicio = get_catalog_id('servicios', row.iloc[14])
            dueño = get_catalog_id('dueños', row.iloc[20])

            if None in [sitio, ambiente, tipo, marca, servicio, dueño]:
                return jsonify({'error': 'Valor no incluido en los catálogos'}), 400

            # Preparar los datos para la inserción
            iSitio = sitio
            vNombre = row.iloc[2]
            bEncendido = True if row.iloc[3].strip().lower() == 'on' else False
            dFechaEstatus = date.today()
            iAmbiente = ambiente
            iTipo = tipo
            vCluster = row.iloc[6]
            vChassis = row.iloc[7]
            vBahia = row.iloc[8]
            iMarca = marca
            vModelo = row.iloc[10]
            vSerial = row.iloc[11]
            iNucleos = row.iloc[12]
            iMemoria = row.iloc[13]
            iServicio = servicio
            dFechaInicioSoporte = row.iloc[15].strftime('%Y-%m-%d')
            dFechaFinSoporte = row.iloc[16].strftime('%Y-%m-%d')
            dFechaFinVida = row.iloc[17].strftime('%Y-%m-%d')
            vIpRed = row.iloc[18]
            vIpILO = row.iloc[19]
            iDueño = dueño
            iHDD = row.iloc[21]

            # Insertar el equipo en la base de datos
            query = """
            INSERT INTO admin.equipos (
                iSitio, vNombre, bEncendido, vEstatus, dFechaEstatus, 
                iAmbiente, iTipo, vCluster, vChassis, vBahia, 
                iMarca, vModelo, vSerial, iNucleos, iMemoria, 
                iServicio, dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida, 
                vIpRed, vIpILO, iDueño, iHDD
            ) VALUES (
                %s, %s, %s, 'Activo', %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                %s, %s, %s, %s
            )
            """
            cursor.execute(query, (
            iSitio, vNombre, bEncendido, dFechaEstatus, 
            iAmbiente, iTipo, vCluster, vChassis, vBahia, 
            iMarca, vModelo, vSerial, iNucleos, iMemoria, 
            iServicio, dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida, 
            vIpRed, vIpILO, iDueño, iHDD
            ))
            conn.commit()
            commits + 1
            
        cursor.close()
        conn.close()

        if (commits>0):
            return jsonify({'message': 'Carga masiva completada exitosamente'}), 200
        else:
            return jsonify({'error': str(e)}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Eliminar el archivo temporal
        os.remove(file_path)
    
if __name__ == '__main__':
    app.run(debug=True)