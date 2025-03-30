from conexion import conexion

def obtenerIdPaquete(nombre):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id FROM paquetes WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None  # ✅ Devuelve solo el ID

    except Exception as r:
        print(r)        
        return None
    
def obtenerIdAntena(nombreAntena):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT idantenasAp FROM antenasap WHERE nombre = %s", (nombreAntena,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None  # ✅ Devuelve solo el ID

    except Exception as r:
        print(r)        
        return None
    
def obtenerIdServicio(nombreServicio):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT idPlataformas FROM serviciosplataforma WHERE nombre = %s", (nombreServicio,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None  # ✅ Devuelve solo el ID

    except Exception as r:
        print(r)        
        return None

def obtenerIdMicrotik(nombreMicrotik):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id FROM credenciales_microtik WHERE nombre = %s", (nombreMicrotik,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None  # ✅ Devuelve solo el ID

    except Exception as r:
        print(r)        
        return None
    
def getIdUsuario(nombreUsuario):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE nombre = %s", (nombreUsuario,))
        resultado = cursor.fetchone()
        print(f"ID del usuario {resultado[0]}")
        return resultado[0]
    
    except Exception as r:
        print(f"Error en la consulta del id del usuario {r}")
        return []
    
def getIdCliente(nombre):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT id FROM clientes WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        cn.close()
        cursor.close()
        print(f"ID del cliente {resultado[0]}")
        return resultado[0]
    except Exception as r:
        print(f"Problemas en la consulta del id del cliente {r}")
        return []