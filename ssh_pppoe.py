import paramiko
import re
from d_consultas import *
import ipaddress
from flask import flash, redirect, url_for


def get_pppoe_profiles(hostname, port, username, password):
    command = '/ppp/profile/print'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    ssh.close()
    
    profiles = []
    # Separa la salida en bloques usando líneas en blanco
    blocks = output.strip().split("\n\n")
    idx = 0
    for block in blocks:
        if "name=" not in block:
            continue  # Omite bloques sin perfil
        # Extraer los campos mediante expresiones regulares
        name_match = re.search(r'name="([^"]+)"', block)
        local_match = re.search(r'local-address=([^ ]+)', block)
        remote_match = re.search(r'remote-address=([^ ]+)', block)
        rate_match = re.search(r'rate-limit="([^"]+)"', block)
        
        name = name_match.group(1) if name_match else ""
        local_address = local_match.group(1) if local_match else ""
        remote_address = remote_match.group(1) if remote_match else ""
        max_limit = rate_match.group(1) if rate_match else ""
        
        # Se asume que "remote_address" es el nombre de la pool en este caso.
        profiles.append({
            'id': idx,
            'name': name,
            'local_address': local_address,
            'remote_address': remote_address,
            'pool': remote_address,  # Puedes ajustar si la pool se obtiene de otro campo
            'max_limit': max_limit
        })
        idx += 1
    return profiles

# Función para obtener las IP pools vía Paramiko (se ejecuta en el Mikrotik seleccionado)
def get_ip_pools(microtik):
    credenciales = consultarCredenciales(microtik)
    if not credenciales:
        return []
    username, password, host, port = credenciales
    command = '/ip/pool/print'
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port=port, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    ssh.close()
    
    pools = []
    lines = output.splitlines()
    for line in lines:
        if not line.strip() or "NAME" in line or "RANGES" in line:
            continue
        parts = re.split(r'\s+', line.strip())
        if len(parts) >= 3:
            pool = {
                'name': parts[1],
                'ranges': parts[2]
            }
            pools.append(pool)
    return pools


def get_pool_ranges(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=int(port), username=username, password=password)
        
        # Ejecutar el comando para obtener las IP Pools
        stdin, stdout, stderr = client.exec_command("/ip/pool/print")
        output = stdout.read().decode('utf-8')
        client.close()

        # Procesar salida para extraer solo los rangos
        ranges = []
        for line in output.splitlines():
            if line.strip() == "" or "NAME" in line or "Columns:" in line:
                continue
            
            # Buscar solo el rango de IPs en la línea
            match = re.search(r"(\d+\.\d+\.\d+\.\d+[-/]\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ranges.append(match.group(1))

        return ranges

    except Exception as e:
        print("Error al obtener IP Pools:", e)
        return []
    
def buscar_pool_por_local_address(host, port, username, password, local_address):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=int(port), username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("/ip/pool/print")
        output = stdout.read().decode('utf-8')
        ssh.close()

        # Recorremos las líneas obtenidas y buscamos la pool que coincida con el local_address
        for line in output.splitlines():
            if line.strip() == "" or "NAME" in line or "Columns:" in line:
                continue
            # Suponemos un formato como: <número>  pool_name   pool_ranges ...
            match = re.match(r"\s*\d+\s+(\S+)\s+(\S+)", line)
            if match:
                pool_name = match.group(1)
                pool_ranges = match.group(2)
                try:
                    # Extraemos la primera IP del rango y restamos 1
                    first_ip = pool_ranges.split('-')[0]
                    ip_obj = ipaddress.ip_address(first_ip)
                    expected_local = str(ip_obj - 1)
                    if expected_local == local_address:
                        return pool_name
                except Exception as e:
                    continue
        return None
    except Exception as e:
        print("Error buscando pool:", e)
        return None


def creacion_profile(nombre, ippool_value, max_limit, username, password, host, port, queue_parent):
    # Calcular la dirección local: se toma la primera IP del rango y se le resta 1
    try:
        first_ip = ippool_value.split('-')[0]
        ip_obj = ipaddress.ip_address(first_ip)
        local_address = str(ip_obj - 1)
    except Exception as e:
        flash("Error al procesar la IP Pool seleccionada", "danger")
        return

    # Buscar en el MikroTik el nombre de la pool utilizando el local_address calculado
    pool_name = buscar_pool_por_local_address(host, port, username, password, local_address)
    if not pool_name:
        flash("No se encontró la pool para la dirección local calculada", "danger")
        return

    remote_address = pool_name  # Se asigna el nombre de la pool obtenida

    # Calcular la ráfaga basada en el max_limit
    try:
        # Construir el comando para crear el PPP Profile con ráfaga
        command = f'/ppp/profile/add name="{nombre}" local-address="{local_address}" remote-address="{remote_address}" address-list=Internet rate-limit={max_limit} parent-queue={queue_parent}'
        print(f"Comando enviado: {command}")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=int(port), username=username, password=password)
        ssh.exec_command(command)
        ssh.close()
        return True
    except Exception as e:
        flash(f"Error al procesar límites o crear perfil: {e}", "danger")
        return False

def reicniar_mikrotik(username, password, host, port):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        ssh.exec_command("/system/reboot")
        ssh.close()
        flash("Mikrotik reiniciado", "success")
    except Exception as r:
        flash(f"Error con el comando de reinicio {r}", "danger")