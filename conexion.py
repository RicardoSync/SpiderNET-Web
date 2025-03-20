import mysql.connector

def conexion():
    try:
        con = mysql.connector.Connect(
            host="localhost",
            port="3306",
            user="root",
            password="zerocuatro04",
            database="spidernet"
        )
        return con
    
    except Exception as r:
        print(r)
        return None