from conexion import conexion

def contador_clientes():
    try:
        cn = conexion()
        if cn is None:
            cn = conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT COUNT(*) FROM clientes")
        resultado = cursor.fetchone()
        cursor.close()
        cn.close()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error en contador_clientes: {e}")
        return 0
    
def contador_equipos():
    try:
        cn = conexion()
        if cn is None:
            cn = conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT COUNT(*) FROM equipos")
        resultado = cursor.fetchone()
        cursor.close()
        cn.close()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error en contador_equipos: {e}")
        return 0
    
def contador_pagos():
    try:
        cn = conexion()
        if cn is None:
            cn = conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT COUNT(*) FROM pagos")
        resultado = cursor.fetchone()
        cursor.close()
        cn.close()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error en contador_pagos: {e}")
        return 0

def contador_mikrotik():
    try:
        cn = conexion()
        if cn is None:
            cn = conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT COUNT(*) FROM credenciales_microtik")
        resultado = cursor.fetchone()
        cursor.close()
        cn.close()
        return resultado[0] if resultado else 0
    except Exception as e:
        print(f"Error en contador_mikrotik: {e}")
        return 0
