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
    

