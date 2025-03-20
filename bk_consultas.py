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