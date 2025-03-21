from conexion import conexion

def consultarServicios():
    try:
        cn = conexion()

        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "SELECT  idPlataformas, nombre, descripcion, precio FROM serviciosplataforma"
        cursor.execute(sql)

        resultado = cursor.fetchall()

        return resultado

    except Exception as r:
        print(r)
        return None
    

def consultarPaquetes():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id, nombre, velocidad, precio FROM paquetes")
        
        resultado = cursor.fetchall()

        cn.close()
        cursor.close()
        return resultado

    except Exception as r:
        print(r)
        return False
    

def consultarAntenas():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "SELECT idAntenasAp, nombre, modelo, usuario, password, ip FROM antenasap"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cn.close()
        cursor.close()
        return resultado

    except Exception as r:
        print(r)
        return False
    
def consultarUsuarios():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        sql = "SELECT id, nombre, usuario, password FROM usuarios"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cn.close()
        cursor.close()
        return resultado
    
    except Exception as r:
        print(r)
        return False