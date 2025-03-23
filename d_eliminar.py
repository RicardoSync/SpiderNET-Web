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