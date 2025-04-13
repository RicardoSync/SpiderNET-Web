from conexion import conexion

def login(usernanme, password):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        
        cursor = cn.cursor()
        cursor.execute("SELECT usuario, password, rol FROM usuarios WHERE usuario = %s AND password = %s", (usernanme, password))
        resultado = cursor.fetchone()
        
        cursor.close()
        cn.close()
        
        if resultado is not None:
            return resultado[2]  # 0=admin, 1=tecnico, 2=cliente
        else:
            return False  # usuario no encontrado o credenciales incorrectas

    except Exception as r:
        print(f"Error de sesion {r}")
        return False
