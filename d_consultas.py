from conexion import conexion

def consultarMicrotik():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM credenciales_microtik")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return [fila[0] for fila in resultado]

    except Exception as r:
        print(r)
        return False

def consultarMicrotikTodo():
    try:
        cn = conexion()
        if cn is None:
            cn = conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id, nombre, username, password, ip, port FROM credenciales_microtik")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return resultado  # Devolver la tupla completa para cada registro

    except Exception as r:
        print(r)
        return False
    

def consultarCredenciales(nombre):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT username, password, ip, port FROM credenciales_microtik WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        cursor.close()
        cn.close()

        return resultado

    except Exception as r:
        print(r)
        return False
    

def consutlarPaquete():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM paquetes")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return [fila[0] for fila in resultado]

    except Exception as r:
        print(r)
        return False
    
def consutlarAntena():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM antenasap")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return [fila[0] for fila in resultado]

    except Exception as r:
        print(r)
        return False
    
def consultarServicio():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM serviciosplataforma")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return [fila[0] for fila in resultado]

    except Exception as r:
        print(r)
        return False
    
def consultarClientes():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        #cursor = cn.cursor(dictionary=True)
        cursor = cn.cursor()
        sql = """
            SELECT 
                c.id,
                c.nombre,
                p.nombre AS paquete,  -- Obtener el nombre del paquete
                DATE_FORMAT(c.fecha_registro, '%d/%m/%Y') AS fecha_registro,  -- Formato de fecha
                c.ip_cliente,
                c.dia_corte,
                a.nombre AS antena_ap,  -- Obtener el nombre de la antena (si existe)
                sp.nombre AS servicio_plataforma,  -- Obtener el nombre del servicio de plataforma 
                cm.nombre AS microtik_nombre  -- Obtener el nombre del MikroTik
            FROM clientes c
            LEFT JOIN paquetes p ON c.id_paquete = p.id
            LEFT JOIN credenciales_microtik cm ON c.id_microtik = cm.id
            LEFT JOIN antenasap a ON c.id_antena_ap = a.idantenasAp
            LEFT JOIN serviciosplataforma sp ON c.id_servicio_plataforma = sp.idPlataformas;

            """
        cursor.execute(sql)  # Ahora ya no necesitas pasar un parámetro
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return resultado

    except Exception as r:
        print(r)
        return []  # Devuelve una lista vacía en caso de error

def consultarVelocidadPaquete(nombre):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT velocidad FROM paquetes WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()

        cursor.close()
        cn.close()

        return resultado
    except Exception as r:
        print(f"Error en consulta de paquete {r}")
        return False
    

def consultarPaquetes():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT id, nombre, velocidad, precio FROM paquetes")
        resultado = cursor.fetchall()

        cursor.close()
        cn.close()

        return resultado
    except Exception as r:
        print(f"Error en consulta de paquete {r}")
        return False
    

def consultarTodoServicios():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT idPlataformas, nombre, descripcion, precio FROM serviciosplataforma")
        resultado = cursor.fetchall()
        cn.close()
        cursor.close()
        
        return resultado
    except Exception as r:
        print(f"Error en la consulta de sercios {r}")
        return False
        