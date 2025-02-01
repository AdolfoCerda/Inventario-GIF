from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)