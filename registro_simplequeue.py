import re
import paramiko
from get_ids import *
from d_consultas import *
from flask import flash, request, render_template, redirect, url_for, session
from conexion import conexion
from conexion import conexion

def obtener_datos_mikrotik_cargar_simple_queue(id):
    credenciales = obtener_credenciales_mikrotik_con_id(id)
    if credenciales:
        host =credenciales[1]
        username = credenciales[2]
        pasword = credenciales[3]
        port = credenciales[4]
        print(f"Usuarios obtenidos son: {host, username, pasword, port}")
        importar_simple_queues(username, pasword, host, port, id)
    else:
        flash("No encontramos datos de este mikrotik", "danger")
    return redirect(url_for("lista_microtiks"))
    
def importar_simple_queues(username, password, host, port, id_microtik):
    try:
        # Conexión SSH a MikroTik
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)

        # Ejecutar el comando para obtener las simple queues
        stdin, stdout, stderr = ssh.exec_command('/queue/simple/print without-paging')
        output = stdout.read().decode('utf-8')
        ssh.close()

        cn = conexion()
        cursor = cn.cursor()

        for line in output.splitlines():
            # Extraer name="Nombre con Espacios" y target=IP
            match_name = re.search(r'name="([^"]+)"', line)
            match_target = re.search(r'target=([\d\.]+)/?', line)

            if match_name and match_target:
                nombre = match_name.group(1).strip()
                ip_cliente = match_target.group(1).strip()

                cursor.execute("""
                    INSERT INTO clientes (nombre, ip_cliente, id_microtik)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE ip_cliente=VALUES(ip_cliente)
                """, (nombre, ip_cliente, id_microtik))

        cn.commit()
        cursor.close()
        cn.close()
        print("importacion")
        flash("Importacion de clientes exitosa!", "success")

    except Exception as e:
        print(f"Error durante la importación: {e}")