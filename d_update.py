from d_insert import obtenerIdPaquete, obtenerIdAntena, obtenerIdServicio, obtenerIdMicrotik
from conexion import conexion

def actualizarCliete(nombre, paquete, direccion_ip, dia_corte, ap, servicio, microtik, id):
    try:
        id_paquete = int(obtenerIdPaquete(paquete)) if obtenerIdPaquete(paquete) is not None else None
        id_antena = int(obtenerIdAntena(ap)) if obtenerIdAntena(ap) is not None else None
        id_servicio = int(obtenerIdServicio(servicio)) if obtenerIdServicio(servicio) is not None else None
        id_microtik = int(obtenerIdMicrotik(microtik)) if obtenerIdMicrotik(microtik) is not None else None

        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        sql = """UPDATE clientes SET nombre = %s, id_paquete = %s, ip_cliente = %s, dia_corte = %s, id_antena_ap = %s,
                id_servicio_plataforma = %s, id_microtik = %s WHERE id = %s"""
        
        cursor.execute(sql, (nombre, id_paquete, direccion_ip, dia_corte, id_antena, id_servicio, id_microtik, id))

        cn.commit()
        cursor.close()
        cn.close()

        return True
    
    except Exception as r:
        print(r)
        return False