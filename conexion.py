import mysql.connector

def conexion():
    try:
        con = mysql.connector.Connect(
            host="localhost",
            port="3306",
            username="root",
            password="zerocuatro04",
            database="spidernet"
        )
        return con
    
    except Exception as r:
        print(r)
        return False