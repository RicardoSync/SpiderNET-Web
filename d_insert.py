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
    

def insertarCliente(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik):
    try:
        id_paquete = int(obtenerIdPaquete(paquete)) if obtenerIdPaquete(paquete) is not None else None
        id_antena = int(obtenerIdAntena(antena_ap)) if obtenerIdAntena(antena_ap) is not None else None
        id_servicio = int(obtenerIdServicio(servicio)) if obtenerIdServicio(servicio) is not None else None
        id_microtik = int(obtenerIdMicrotik(microtik)) if obtenerIdMicrotik(microtik) is not None else None

        cn = conexion()
        if cn is None:
            cn = conexion()
            cn.reconnect()

        cursor = cn.cursor()
        sql = """INSERT INTO clientes (nombre, id_paquete, ip_cliente, dia_corte, id_antena_ap, id_servicio_plataforma, id_microtik)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(sql, (nombre, id_paquete, ip_cliente, dia_corte, id_antena, id_servicio, id_microtik))

        cn.commit()
        cursor.close()
        cn.close()

        return True
    
    except Exception as r:
        print(f"Error al insertar cliente: {r}")
        return False


def insertMicrotik(nombre, ip, username, password, port):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "INSERT INTO credenciales_microtik (nombre, ip, username, password, port) VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (nombre, ip, username, password, port))

        cn.commit()
        cursor.close()
        cn.close()
        return True
    
    except Exception as r:
        print(r)
        return False

def insertarPauqete(nombre, velocidad, precio):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = "INSERT INTO paquetes (nombre, velocidad, precio) VALUES (%s,%s,%s)"
        cursor.execute(sql, (nombre, velocidad, precio))
                       
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(f"Error de insert {r}")
        return False
    
def insertarServicio(nombre, descripcion, precio):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
            
        cursor = cn.cursor()
        cursor.execute("""INSERT INTO serviciosplataforma (nombre, descripcion, precio)
                       VALUES (%s,%s,%s)""", (nombre, descripcion,precio))
        
        cn.commit()
        cursor.close()
        cn.close()
        return True
    
    except Exception as r:
        print(f"Tenemos un error al insertar el servicio {r}")
        return False