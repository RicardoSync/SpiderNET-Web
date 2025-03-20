from conexion import conexion

def validacion_usuario(username, password):
    try:
        cn = conexion()
        
        if cn is None:
            conexion().reconnect()
        
        cursor = cn.cursor()
        sql = "SELECT usuario, password, id FROM usuarios WHERE usuario = %s AND password = %s"
        valores = (username, password)
        cursor.execute(sql, valores)

        resultado = cursor.fetchone()

        cn.close()
        cursor.close()

        return resultado
    
    except Exception as r:
        print(r)
        return None