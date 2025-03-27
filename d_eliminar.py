from conexion import conexion

def eliminar_cliente_chido(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        cn.commit()
        cursor.close()
        cursor.close()

        return True
    except Exception as r:
        print(r)
        return False
    
def eliminarMicrotik(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("DELETE FROM credenciales_microtik WHERE id = %s", (id,))
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(r)
        return False

def eliminarPaquete(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("DELETE FROM paquetes WHERE id = %s", (id,))
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(r)
        return False

def eliminarServicio(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("DELETE FROM serviciosplataforma WHERE idPlataformas = %s", (id,))
        cn.commit()
        cursor.close()
        cn.close()
        return True
    except Exception as r:
        print(f"Error al eliminar {r}")
        return False
    
def eliminarEquipo(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("DELETE FROM equipos WHERE id = %s", (id,))
        cn.commit()
        cursor.close()
        cn.close()
        return True
    except Exception as r:
        print(f"Error al eliminar {r}")
        return False
    
def eliminarQueueBD(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("DELETE FROM queue_parent WHERE id = %s", (id,))
        cn.commit()
        cursor.close()
        cn.close()
        return True
    except Exception as r:
        print(f"Error al eliminar {r}")
        return False