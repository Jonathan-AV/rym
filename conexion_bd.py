import pymysql

def obtener_conexion():
    return pymysql.connect(host='localhost',
    user='user_rym',
    password='proyectoRYM',
    database='rym')