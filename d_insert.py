from conexion import conexion
from get_ids import *
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
    
def insertarEquipo(nombre, tipo, marca, modelo, estado, id_cliente):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("""INSERT INTO equipos (nombre, tipo, marca, modelo, estado, id_cliente)
                        VALUES (%s,%s,%s,%s,%s,%s)""", (nombre, tipo, marca, modelo, estado, id_cliente))
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(f"Tenemos un error al insertar el equipo {r}")
        return False
    
def insertar_queue_parent(nombre, subred, max_limit, mikrotik):
    mikrotik = obtenerIdMicrotik(mikrotik)
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("""INSERT INTO queue_parent (nombre, subred, max_limit, id_mikrotik) VALUES (%s,%s,%s,%s)""",
                       (nombre, subred, max_limit, mikrotik))
        cn.commit()
        cursor.close()
        cn.close()

        return True
    except Exception as r:
        print(f"Error en crear un queue {r}")
        return False
    
def insertar_ticket(cliente, categoria, descripcion, usuario):
    id_usuario = getIdUsuario(nombreUsuario=usuario)
    id_cliente = getIdCliente(nombre=cliente)

    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
        cursor = cn.cursor()
        cursor.execute("INSERT INTO tickets (id_cliente, categoria, descripcion, estado, id_responsable) VALUES (%s,%s,%s,%s,%s)",
                       (id_cliente, categoria, descripcion, "Pendiente", id_usuario))
        cn.commit()
        cursor.close()
        cn.close()
        return True
    except Exception as r:
        print(f"Error en la creacion del ticket {r}")
        return False
    

def insertar_profile_pppoe(nombre, local_address, remote_address ,address_list, limit, id_mikrotik):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()
            
        cursor = cn.cursor()
        cursor.execute("INSERT INTO profile (nombre, local_address, remote_address, address_list, max_limit, id_mikrotik) VALUES (%s,%s,%s,%s,%s,%s)",
                       (nombre, local_address, remote_address, address_list, limit, id_mikrotik))
        cn.commit()
        cursor.close()
        cn.close()
        return True
    except Exception as r:
        print(f"Error en la creacion de profile en bd {r}")
        return False