from conexion import conexion

def eliminarServicio(id):
    try:
        cn = conexion()

        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "DELETE FROM serviciosplataforma WHERE idPlataformas = %s"
        cursor.execute(sql, (id,))
        cn.commit()
        cn.close()
        cursor.close()
        return True

    except Exception as r:
        print(r)
        return False