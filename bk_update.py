from conexion import conexion

def editarServicio(nombre, descripcion, precio, id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "UPDATE serviciosplataforma SET nombre = %s, descripcion = %s, precio = %s WHERE idPlataformas = %s"
        cursor.execute(sql, (nombre, descripcion, precio, id))

        cn.commit()
        cn.close()
        cursor.close()

        return True
    
    except Exception as r:
        print(r)
        return False
    

def editarPaquete(nombre, velocidad, precio, id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "UPDATE paquetes SET nombre = %s, velocidad = %s, precio = %s WHERE id = %s"
        cursor.execute(sql, (nombre, velocidad, precio, id))
        cn.commit()
        cursor.close()
        cn.close()

        return True

    except Exception as r:
        print(r)
        return False
    

def editarAntena(nombre, modelo, usuario, password, ip, id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        sql = "UPDATE antenasap SET nombre = %s, modelo = %s, usuario = %s, password = %s, ip = %s WHERE idantenasAp = %s"
        cursor.execute(sql, (nombre, modelo, usuario, password,ip,id))

        cn.commit()
        cursor.close()
        cn.close()

        return True

    except Exception as r:
        print(r)
        return False