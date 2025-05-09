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
            d.vNombre AS dueño_nombre,
            p.vNombre AS procesador_nombre,
            u.vNombre AS unidadAlmac_nombre,
            si.vNombre AS sistema_nombre,
            r.vNombre AS rack_nombre
        FROM admin.equipos e
        LEFT JOIN admin.sitios s ON e.iSitio = s.iId
        LEFT JOIN admin.ambientes a ON e.iAmbiente = a.iId
        LEFT JOIN admin.tipos t ON e.iTipo = t.iId
        LEFT JOIN admin.marcas m ON e.iMarca = m.iId
        LEFT JOIN admin.servicios sv ON e.iServicio = sv.iId
        LEFT JOIN admin.dueños d ON e.iDueño = d.iId
        LEFT JOIN admin.procesadores p ON e.iProcesador = p.iId
        LEFT JOIN admin.unidadesalmac u ON e.iUnidadAlmac = u.iId
        LEFT JOIN admin.sisoperativos si ON e.iSistema = si.iId
        LEFT JOIN admin.racks r ON e.iRack = r.iId
        WHERE e.vserial = %s
    """
    
    cursor.execute(query, (serial,))
    resultado = cursor.fetchall()
    return jsonify(resultado)

@app.post('/api/servicios')
def obtener_servicios():
    datos = request.get_json()
    serial = datos.get("serial")

    # Inicializar valores para enviar al front
    servicios_estado = {
        "afore": False,
        "almacenamiento": False,
        "bancoppel": False,
        "biometrico": False,
        "cartera": False,
        "chassis": False,
        "etl": False,
        "fabric": False,
        "huellas": False,
        "hypervisor": False,
        "hvafore": False,
        "switchmds": False
    }

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Consulta para obtener iIdServicio
        query = """
            SELECT iIdServicio FROM admin.equiposervicio
            WHERE vserialequipo = %s
        """
        cursor.execute(query, (serial,))
        resultados = cursor.fetchall()

        # Para cada iIdServicio, busca vNombre en la tabla servicios y actualiza las variables
        for row in resultados:
            iIdServicio = row[0]
            query_servicio = "SELECT vNombre FROM admin.servicios WHERE iId = %s"
            cursor.execute(query_servicio, (iIdServicio,))
            servicio = cursor.fetchone()

            if servicio:
                vNombre = servicio[0].strip().lower()

                # Matching vNombre and updating boolean variables
                if vNombre == 'afore':
                    servicios_estado["afore"] = True
                elif vNombre == 'almacenamiento':
                    servicios_estado["almacenamiento"] = True
                elif vNombre == 'bancoppel':
                    servicios_estado["bancoppel"] = True
                elif vNombre == 'biometrico':
                    servicios_estado["biometrico"] = True
                elif vNombre == 'cartera en línea':
                    servicios_estado["cartera"] = True
                elif vNombre == 'chassis':
                    servicios_estado["chassis"] = True
                elif vNombre == 'etl':
                    servicios_estado["etl"] = True
                elif vNombre == 'fabric':
                    servicios_estado["fabric"] = True
                elif vNombre == 'huellas':
                    servicios_estado["huellas"] = True
                elif vNombre == 'hypervisor':
                    servicios_estado["hypervisor"] = True
                elif vNombre == 'hypervisor afore':
                    servicios_estado["hvafore"] = True
                elif vNombre == 'switch mds':
                    servicios_estado["switchmds"] = True

        cursor.close()
        conn.close()

        print(servicios_estado)

        # Retorna el JSON con los estados de los servicios
        return jsonify(servicios_estado)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    

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
            "Dueños": "dueños",
            # Nuevas tablas
            "Procesadores": "procesadores",
            "UnidadesAlmac": "unidadesalmac",
            "SisOperativos": "sisoperativos",
            "Racks": "racks"
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
    dFechaInicioSoporte = datos.get("fechaInicioSoporte")
    dFechaFinSoporte = datos.get("fechaFinSoporte")
    dFechaFinVida = datos.get("fechaFinVida")
    vIpRed = datos.get("ipRed")
    vIpILO = datos.get("ipILO")
    iCantCpus = datos.get("cantCpus")
    iCantUnidades = datos.get("cantUnidades")
    vCapacidadAlmac = datos.get("capacidadAlmac")
    iCantModulosRam = datos.get("cantModulosRam")
    vCapacidadRam = datos.get("capacidadRam")
    vTipoRam = datos.get("tipoRam")
    iUnidadRack = datos.get("unidadRack")

    #Valor booleano servicios
    afore = datos.get("afore")
    almacenamiento = datos.get("almacenamiento")
    bancoppel = datos.get("bancoppel")
    biometrico = datos.get("biometrico")
    cartera = datos.get("cartera")
    servchassis = datos.get("servchassis")
    etl = datos.get("ETL")
    fabric = datos.get("fabric")
    huellas = datos.get("huellas")
    hypervisor = datos.get("hypervisor")
    hvafore = datos.get("HVafore")
    switchmds = datos.get("switchMDS")

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
        # Catalogos nuevos
        iProcesador = get_catalog_id('procesadores', datos.get("procesador"))
        iUnidadAlmac = get_catalog_id('unidadesalmac', datos.get("unidadAlmac"))
        iSistema = get_catalog_id('sisoperativos', datos.get("sistema"))
        iRack = get_catalog_id('racks', datos.get("rack"))

        # Verificar que todos los IDs hayan sido recuperados correctamente
        if None in (iSitio, iAmbiente, iTipo, iMarca, iServicio, iDueño, iProcesador, iUnidadAlmac, iSistema, iRack):
            return jsonify({"mensaje": "Datos de catálogo inválidos", "status": "error"}), 400

        # Query para agregar
        query = """
            INSERT INTO admin.Equipos (
                iSitio, vNombre, bEncendido, vEstatus, dFechaEstatus, 
                iAmbiente, iTipo, vCluster, vChassis, vBahia, 
                iMarca, vModelo, vSerial, iServicio,
                dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida,
                vIpRed, vIpILO, iDueño,
                iProcesador, iCantCpus, iNucleos, iUnidadAlmac, iCantUnidades, vCapacidadAlmac,
                iCantModulosRam, vCapacidadRam, vTipoRam, iSistema, iRack, iUnidadRack
            ) VALUES (
                %s, %s, %s, 'Activo', %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s, %s,
                %s, %s, %s, 
                %s, %s, %s, 
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s
            )
        """
        cursor.execute(query, (
            iSitio, vNombre, bEncendido, dFechaEstatus, 
            iAmbiente, iTipo, vCluster, vChassis, vBahia, 
            iMarca, vModelo, vSerial, iServicio, 
            dFechaInicioSoporte, dFechaFinSoporte, dFechaFinVida, 
            vIpRed, vIpILO, iDueño,
            iProcesador, iCantCpus, iNucleos, iUnidadAlmac, iCantUnidades, vCapacidadAlmac,
            iCantModulosRam, vCapacidadRam, vTipoRam, iSistema, iRack, iUnidadRack
        ))

        # Registrar servicios si el valor es true
        if afore:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 1); """
            cursor.execute(queryservicios, (vSerial,))
        if almacenamiento:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 2); """
            cursor.execute(queryservicios, (vSerial,))
        if bancoppel:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 3); """
            cursor.execute(queryservicios, (vSerial,))
        if biometrico:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 4); """
            cursor.execute(queryservicios, (vSerial,))
        if cartera:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 5); """
            cursor.execute(queryservicios, (vSerial,))
        if servchassis:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 6); """
            cursor.execute(queryservicios, (vSerial,))
        if etl:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 7); """
            cursor.execute(queryservicios, (vSerial,))
        if fabric:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 8); """
            cursor.execute(queryservicios, (vSerial,))
        if huellas:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 9); """
            cursor.execute(queryservicios, (vSerial,))
        if hypervisor:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 10); """
            cursor.execute(queryservicios, (vSerial,))
        if hvafore:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 11); """
            cursor.execute(queryservicios, (vSerial,))
        if switchmds:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 12); """
            cursor.execute(queryservicios, (vSerial,))
        
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
    dFechaInicioSoporte = datos.get("fechaInicioSoporte")
    dFechaFinSoporte = datos.get("fechaFinSoporte")
    dFechaFinVida = datos.get("fechaFinVida")
    vIpRed = datos.get("ipRed")
    vIpILO = datos.get("ipILO")
    iCantCpus = datos.get("cantCpus")
    iCantUnidades = datos.get("cantUnidades")
    vCapacidadAlmac = datos.get("capacidadAlmac")
    iCantModulosRam = datos.get("cantModulosRam")
    vCapacidadRam = datos.get("capacidadRam")
    vTipoRam = datos.get("tipoRam")
    iUnidadRack = datos.get("unidadRack")

    #Valor booleano servicios
    afore = datos.get("afore")
    almacenamiento = datos.get("almacenamiento")
    bancoppel = datos.get("bancoppel")
    biometrico = datos.get("biometrico")
    cartera = datos.get("cartera")
    servchassis = datos.get("servchassis")
    etl = datos.get("ETL")
    fabric = datos.get("fabric")
    huellas = datos.get("huellas")
    hypervisor = datos.get("hypervisor")
    hvafore = datos.get("HVafore")
    switchmds = datos.get("switchMDS")

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
        # Catalogos nuevos
        iProcesador = get_catalog_id('procesadores', datos.get("procesador"))
        iUnidadAlmac = get_catalog_id('unidadesalmac', datos.get("unidadAlmac"))
        iSistema = get_catalog_id('sisoperativos', datos.get("sistema"))
        iRack = get_catalog_id('racks', datos.get("rack"))

        # Verificar que todos los IDs hayan sido recuperados correctamente
        if None in (iSitio, iAmbiente, iTipo, iMarca, iServicio, iDueño, iProcesador, iUnidadAlmac, iSistema, iRack):
            return jsonify({"mensaje": "Datos de catálogo inválidos", "status": "error"}), 400

        # Query para actualizar
        query = """
            UPDATE admin.Equipos SET
                iSitio = %s, vNombre = %s, bEncendido = %s, 
                iAmbiente = %s, iTipo = %s, vCluster = %s, 
                vChassis = %s, vBahia = %s, iMarca = %s, 
                vModelo = %s, 
                iServicio = %s, dFechaInicioSoporte = %s, 
                dFechaFinSoporte = %s, dFechaFinVida = %s, 
                vIpRed = %s, vIpILO = %s, iDueño = %s,
                iProcesador = %s, iCantCpus = %s, iNucleos = %s, iUnidadAlmac = %s, iCantUnidades = %s, vCapacidadAlmac = %s,
                iCantModulosRam = %s, vCapacidadRam = %s, vTipoRam = %s, iSistema = %s, iRack = %s, iUnidadRack = %s
            WHERE vSerial = %s
        """
        cursor.execute(query, (
            iSitio, vNombre, bEncendido, 
            iAmbiente, iTipo, vCluster, 
            vChassis, vBahia, iMarca, 
            vModelo, 
            iServicio, dFechaInicioSoporte, 
            dFechaFinSoporte, dFechaFinVida, 
            vIpRed, vIpILO, iDueño,
            iProcesador, iCantCpus, iNucleos, iUnidadAlmac, iCantUnidades, vCapacidadAlmac,
            iCantModulosRam, vCapacidadRam, vTipoRam, iSistema, iRack, iUnidadRack,
            vSerial
        ))

        # Si es verdadero registrar servicio si no existe, si no eliminar posible registro de servicio
        if afore:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 1)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 1; """
            cursor.execute(queryservicios, (vSerial,))
        if almacenamiento:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 2)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 2; """
            cursor.execute(queryservicios, (vSerial,))
        if bancoppel:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 3)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 3; """
            cursor.execute(queryservicios, (vSerial,))
        if biometrico:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 4)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 4; """
            cursor.execute(queryservicios, (vSerial,))
        if cartera:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 5)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 5; """
            cursor.execute(queryservicios, (vSerial,))
        if servchassis:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 6)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 6; """
            cursor.execute(queryservicios, (vSerial,))
        if etl:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 7)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 7; """
            cursor.execute(queryservicios, (vSerial,))
        if fabric:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 8)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 8; """
            cursor.execute(queryservicios, (vSerial,))
        if huellas:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 9)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 9; """
            cursor.execute(queryservicios, (vSerial,))
        if hypervisor:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 10)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 10; """
            cursor.execute(queryservicios, (vSerial,))
        if hvafore:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 11)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 11; """
            cursor.execute(queryservicios, (vSerial,))
        if switchmds:
            queryservicios = """ INSERT INTO admin.EquipoServicio (vSerialEquipo, iIdServicio) VALUES (%s, 12)
            ON CONFLICT (vSerialEquipo, iIdServicio) DO NOTHING; """
            cursor.execute(queryservicios, (vSerial,))
        else:
            queryservicios = """ DELETE FROM admin.EquipoServicio WHERE vSerialEquipo = %s AND iIdServicio = 12; """
            cursor.execute(queryservicios, (vSerial,))
        
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Equipo actualizado correctamente", "status": "ok"}), 200

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
            commits += 1
            
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

@app.post('/api/activos')
def obtener_activos():

    filtros = request.get_json()
    
    serial = filtros.get("serial")
    nombre = filtros.get("nombre")
    estatus = filtros.get("estatus")
    sitio = filtros.get("sitio")
    tipo = filtros.get("tipo")
    soporte = filtros.get("soporte")
    vida = filtros.get("vida")
    orden = filtros.get("orden")
    direccion = filtros.get("direccion")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Obtener ID Sitio y Tipo partir del texto en filtros
        def get_catalog_id(table, name):
            query = sql.SQL("SELECT iId FROM admin.{} WHERE vNombre = %s").format(sql.Identifier(table))
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        
        iSitio = 0
        iTipo = 0
        
        iSitio = get_catalog_id('sitios', sitio)
        print(iSitio)
        iTipo = get_catalog_id('tipos', tipo)
        print(iTipo)

        consulta = "SELECT e.*, s.vNombre AS sitio_nombre, t.vNombre AS tipo_nombre, m.vNombre AS marca_nombre FROM admin.equipos e LEFT JOIN admin.sitios s ON e.iSitio = s.iId LEFT JOIN admin.tipos t ON e.iTipo = t.iId LEFT JOIN admin.marcas m ON e.iMarca = m.iId"

        contFiltros = 0

        # Validar si hay filtros
        # Serial
        if (serial != "" and contFiltros == 0):
            consulta += " WHERE e.vSerial LIKE '"+serial+"%'"
            contFiltros += 1
        elif (serial != "" and contFiltros != 0):
            consulta += " AND e.vSerial LIKE '"+serial+"%'"
            contFiltros += 1

        # Nombre
        if (nombre != "" and contFiltros == 0):
            consulta += " WHERE e.vNombre LIKE '"+nombre+"%'"
            contFiltros += 1
        elif (nombre != "" and contFiltros != 0):
            consulta += " AND e.vNombre LIKE '"+nombre+"%'"
            contFiltros += 1

        # Estatus
        if (estatus != "" and contFiltros == 0):
            consulta += " WHERE e.vEstatus = '"+estatus+"'"
            contFiltros += 1
        elif (estatus != "" and contFiltros != 0):
            consulta += " AND e.vEstatus = '"+estatus+"'"
            contFiltros += 1

        # Sitio
        if (sitio != "" and contFiltros == 0):
            consulta += " WHERE e.iSitio = "+str(iSitio)
            contFiltros += 1
        elif (sitio != "" and contFiltros != 0):
            consulta += " AND e.iSitio = "+str(iSitio)
            contFiltros += 1

        # Tipo
        if (tipo != "" and contFiltros == 0):
            consulta += " WHERE e.iTipo = "+str(iTipo)
            contFiltros += 1
        elif (tipo != "" and contFiltros != 0):
            consulta += " AND e.iTipo = "+str(iTipo)
            contFiltros += 1

        # Soporte
        if (soporte != "" and contFiltros == 0):
            consulta += " WHERE e.dFechaFinSoporte <= '"+soporte+"'"
            contFiltros += 1
        elif (soporte != "" and contFiltros != 0):
            consulta += " AND e.dFechaFinSoporte <= '"+soporte+"'"
            contFiltros += 1

        # Vida
        if (vida != "" and contFiltros == 0):
            consulta += " WHERE e.dFechaFinVida <= '"+vida+"'"
            contFiltros += 1
        elif (vida != "" and contFiltros != 0):
            consulta += " AND e.dFechaFinVida <= '"+vida+"'"
            contFiltros += 1

        if (direccion):
            consulta += " ORDER BY "+orden+" ASC"
        else:
            consulta += " ORDER BY "+orden+" DESC"

        print(consulta)

        query = consulta
        
        cursor.execute(query)
        activos = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(activos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Prueba para view Configuraciones
# Endpoint genérico para manejar catálogos
@app.route('/api/catalogos/<tabla>', methods=['GET', 'POST', 'DELETE'])
def gestionar_catalogo(tabla):
    # Validar tabla permitida
    tablas_permitidas = {
        'sitios': 'Sitios',
        'ambientes': 'Ambientes',
        'tipos': 'Tipos',
        'marcas': 'Marcas',
        'servicios': 'Servicios',
        'duenos': 'Dueños',
        'procesadores': 'Procesadores',
        'unidadesalmac': 'UnidadesAlmac',
        'sisoperativos': 'SisOperativos',
        'racks': 'Racks'
    }
    
    if tabla not in tablas_permitidas:
        return jsonify({"error": "Catálogo no válido"}), 400
    
    nombre_tabla = tablas_permitidas[tabla]
    conn = None
    cursor = None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if request.method == 'GET':
            # Obtener todas las opciones del catálogo
            cursor.execute(f"SELECT * FROM admin.{nombre_tabla} ORDER BY vNombre")
            columnas = [desc[0] for desc in cursor.description]
            opciones = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
            return jsonify(opciones)

        elif request.method == 'POST':
            # Agregar nueva opción al catálogo
            datos = request.get_json()
            nombre = datos.get('nombre')
            
            if not nombre:
                return jsonify({"error": "Nombre requerido"}), 400
                
            cursor.execute(
                f"INSERT INTO admin.{nombre_tabla} (vNombre) VALUES (%s) RETURNING iId, vNombre",
                (nombre,)
            )
            nueva_opcion = cursor.fetchone()
            conn.commit()
            
            return jsonify({
                "iId": nueva_opcion[0],
                "vNombre": nueva_opcion[1]
            }), 201

        elif request.method == 'DELETE':
            # Eliminar opción del catálogo
            id_opcion = request.args.get('id')
            
            if not id_opcion:
                return jsonify({"error": "ID requerido"}), 400
                
            # Verificar si la opción está en uso
            if nombre_tabla in ['Sitios', 'Ambientes', 'Tipos', 'Marcas', 'Servicios', 'Dueños']:
                cursor.execute(
                    f"SELECT COUNT(*) FROM admin.Equipos WHERE i{nombre_tabla[:-1]} = %s",
                    (id_opcion,)
                )
                en_uso = cursor.fetchone()[0] > 0
                
                if en_uso:
                    return jsonify({
                        "error": f"No se puede eliminar, hay equipos asociados a esta opción"
                    }), 400
            
            cursor.execute(
                f"DELETE FROM admin.{nombre_tabla} WHERE iId = %s RETURNING vNombre",
                (id_opcion,)
            )
            eliminado = cursor.fetchone()
            
            if not eliminado:
                return jsonify({"error": "Opción no encontrada"}), 404
                
            conn.commit()
            return jsonify({"mensaje": f"'{eliminado[0]}' eliminado correctamente"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)