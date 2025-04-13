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
        cursor.execute(sql) 
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return resultado

    except Exception as r:
        print(f"Tenemos problemas con la consulta de los clientes {r}")
        

def consultar_queue():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        sql = """SELECT q.id, q.nombre, q.subred, q.max_limit, c.nombre AS nombre_mikrotik
                    FROM queue_parent q
                LEFT JOIN credenciales_microtik c ON q.id_mikrotik = c.id"""
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        return resultado
    
    except Exception as r:
        print(f"Error en consulta {r}")
        return False

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

def consultarEquipos():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("""
                        SELECT e.id, c.nombre, e.nombre, e.tipo, e.marca, e.modelo, e.estado AS nombre_cliente
                        FROM equipos e LEFT JOIN clientes c ON e.id_cliente = c.id;
                        """)
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        
        return resultado
    except Exception as r:
        print(f"Error en la consulta de los equipos {r}")
        return False
    
def consultarQeue():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM queue_parent")
        resultado = cursor.fetchall()
        cn.close()
        cursor.close()
        
        return [fila[0] for fila in resultado]
    except Exception as r:
        print(f"Error en la consulta de sercios {r}")
        return []
    

def consultar_clientes_bloqueados():
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
            LEFT JOIN serviciosplataforma sp ON c.id_servicio_plataforma = sp.idPlataformas
            WHERE estado = "Bloqueado";
            """
        cursor.execute(sql) 
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return resultado

    except Exception as r:
        print(f"Tenemos problemas con la consulta de los clientes {r}")


def consularNombreClientes():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        
        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM clientes")
        resultado = cursor.fetchall()

        cursor.close()
        cn.close()

        return [fila[0] for fila in resultado]
    
    except Exception as r:
        print(f"Error en consulta de los nombres {r}")
        return []
    

def consultarUsuarios():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT nombre FROM usuarios")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()

        return [filas[0] for filas in resultado]
    except Exception as r:
        print(f"Error en consulta de los usuarios {r}")
        return []
    
def consultar_tickets():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("""
                        SELECT 
                            f.id, 
                            c.nombre AS cliente, 
                            f.categoria, 
                            f.descripcion, 
                            f.estado, 
                            f.fecha_creacion, 
                            f.fecha_cierre, 
                            u.nombre AS responsable
                        FROM tickets f
                        LEFT JOIN clientes c ON f.id_cliente = c.id  -- Relacionando los tickets con los clientes
                        LEFT JOIN usuarios u ON f.id_responsable = u.id; -- Relacionando los tickets con los usuarios responsables
                    """)
        resultado = cursor.fetchall()
        cn.close()
        cursor.close()
        return resultado
    except Exception as r:
        print(f"Error en consulta de tickets {r}")
        return []
    

def obtener_credenciales(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT ip, username, password, port FROM credenciales_microtik WHERE id = %s", (id,))
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        if resultado:
            return resultado
        else:
            return []
    except Exception as r:
        print(f"Error en credenciales de MikroTik por id {r}")
        return []
    
def consultar_usuarios():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT id, nombre, usuario, password, rol FROM usuarios")
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        
        if resultado:
            return resultado
        else:
            return []
        
    except Exception as r:
        print(f"Error en consulta de usuarios {r}")
        return []
    
def obtener_credenciales_mikrotik_con_id(id):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT nombre, ip, username, password, port FROM credenciales_microtik WHERE id = %s", (id,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado
        else:
            return []
        cursor.close()
        cn.close()
    except Exception as r:
        print(f"Error en las credenciales del mikrotik {r}")
        return []
    
def obtener_precio_paquete(nombre):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("SELECT precio FROM paquetes WHERE nombre = %s", (nombre,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado
        else:
            return []
        cursor.close()
        cn.close()
    except Exception as r:
        print(f"Error en las credenciales del mikrotik {r}")
        return []
    
def consultar_pagos_registrados():
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("""
                        SELECT c.nombre, p.monto, p.fecha_pago, p.metodo_pago
                            FROM pagos p
                        LEFT JOIN clientes c ON p.id_cliente = c.id;
                    """)
        resultado = cursor.fetchall()
        cursor.close()
        cn.close()
        
        return resultado
    except Exception as r:
        print(f"Error en la consulta de los pagos {r}")
        return []