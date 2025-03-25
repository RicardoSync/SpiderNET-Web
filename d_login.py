from conexion import conexion

def login(usernanme, password):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        
        cursor = cn.cursor()
        cursor.execute("SELECT usuario, password, rol FROM usuarios WHERE usuario = %s AND password = %s", (usernanme, password))
        resultado = cursor.fetchall()
        
        cursor.close()
        cn.close()
        
        return resultado
    
    except Exception as r:
        print(f"Error de sesion {r}")
        return False