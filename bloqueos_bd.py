from conexion import conexion

def estado_bloqueado(estado, id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        sql = "UPDATE clientes SET estado = %s WHERE id = %s"
        cursor.execute(sql, (estado, id))
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(f"Error en actualizar el estado {r}")
        return False
    
