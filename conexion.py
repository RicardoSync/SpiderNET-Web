import mysql.connector

def conexion():
    try:
        con = mysql.connector.Connect(
            host="localhost",
            port="3306",
            username="spidernet",
            password="spidernet",
            database="spidernet_web"
        )
        return con
    
    except Exception as r:
        print(r)
        return False