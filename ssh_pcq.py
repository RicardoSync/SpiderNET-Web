import paramiko
import re
from ip_pool import generar_rango_ips, obtener_subred
from d_insert import insertar_queue_parent
from d_consultas import consultarCredenciales

def consultarClientesDHCP(credenciales):
    username = credenciales[0]
    password = credenciales[1]
    host = credenciales[2]
    port = int(credenciales[3])  # Asegurar que es un número

    try:
        print(f"Intentando conectar a {host} en el puerto {port}...")

        # Creación de instancia SSH
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Conexión al MikroTik
        cliente_ssh.connect(host, port=port, username=username, password=password)

        # Ejecutamos el comando
        stdin, stdout, stderr = cliente_ssh.exec_command("/ip/dhcp-server/lease/print")

        # Leer la salida
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error SSH: {errores}")       
            return None

        cliente_ssh.close()
        return salida

    except Exception as e:
        print(f"Error en la conexión SSH: {e}")
        return None

def bloquear_cliente_address_list(credenciales, ip_cliente):
    username = credenciales[0]
    password = credenciales[1]
    host = credenciales[2]
    port = int(credenciales[3])  # Asegurar que es un número   


    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)
        #poner un comando en queue que diga bloqueado
        comentario = '"Cliente bloqueado"'
        sub_red = "/32"
        comandos = [
            f"/ip/firewall/address-list/add list=corte address={ip_cliente}",
            f"/queue/simple/set comment={comentario} [find where target={ip_cliente}{sub_red}]"

        ]
        for comando in comandos:

            stdin, stout, stderr = cliente_ssh.exec_command(comando)

            salida = stout.read().decode()
            errores = stderr.read().decode()
            print(f"comandos enviados {comando}")
            if errores:
                print(f"errores en ssh {errores}")
                return False
        
        cliente_ssh.close()
        return True
    
    except Exception as r:
        print(f"Error en la conexion SSH: {r}")
        return False
    

def desbloqueo_mantecoso(credenciales, ip_cliente):
    username = credenciales[0]
    password = credenciales[1]
    host = credenciales[2]
    port = int(credenciales[3])  # Asegurar que es un número
    print(f"usuario: {username} password {password} host {host} port {port} con objetivo {ip_cliente}")

    try:
        # Establece la conexión SSH con MikroTik
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)
        comentario = '""'
        sub_red = "/32"
        lista_comandos = [
            f"/ip/firewall/address-list/remove [find address={ip_cliente} list=corte]",
            f"/queue/simple/set comment={comentario} [find where target={ip_cliente}{sub_red}]"
        ]
        for comando in lista_comandos:
            stdin, stout, stderr = cliente_ssh.exec_command(comando)

            # Leer la salida y errores
            salida = stout.read().decode()
            errores = stderr.read().decode()
            print(f"Salida del comando {salida}")

            if errores:
                print(f"Errores en la ejecución del comando: {errores}")
                cliente_ssh.close()

            # Si se encuentra la IP, eliminarla de la lista de corte
            if not salida:
                print(f"No se encontró la IP {ip_cliente} en la lista de bloqueo.")
            
        # Cierra la conexión SSH
        cliente_ssh.close()
        return True

    except Exception as e:
        print(f"Error en la conexión SSH: {e}")
        return False


def get_interfaces(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=int(port), username=username, password=password)
        
        stdin, stdout, stderr = client.exec_command("/interface/print")
        output = stdout.read().decode('utf-8')
        client.close()

        # Procesamos la salida para extraer el nombre de la interfaz.
        # Por ejemplo, buscamos líneas que contengan un número seguido de "R" (opcional) y el nombre.
        # La expresión regular puede ajustarse según el formato exacto.
        interfaces = []
        for line in output.splitlines():
            # Evitamos cabecera y líneas vacías
            if line.strip() == "" or "NAME" in line or "Flags" in line:
                continue
            # Suponiendo que el formato es: <número> [R] nombre ...
            match = re.match(r"\s*\d+\s+(?:R\s+)?(\S+)", line)
            if match:
                interfaces.append(match.group(1))
        return interfaces

    except Exception as e:
        print("Error al obtener interfaces:", e)
        return []
    

def creacionAddressList(username, password, host, port, direccion_ip, ether):
    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)

        sub_red = "/24"
        comando = f"/ip/address/add address={direccion_ip}{sub_red} interface={ether}"
        print(f"Comando enviado: {comando}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error al ejecutar el comando: {errores}")
            cliente_ssh.close()
            return False

        # Generar el rango de IPs basado en la dirección ingresada
        rango = generar_rango_ips(ip_base=direccion_ip)
        comando_pool = f"/ip/pool/add name={ether} ranges={rango}"
        print(f"Comando de pool: {comando_pool}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando_pool)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error con el comando de pool: {errores}")
            cliente_ssh.close()
            return False

        # Generar la subred con la dirección IP y configurar gateway y DNS
        address = obtener_subred(direccion_ip)
        comando_network = f"/ip/dhcp-server/network/add address={address} gateway={direccion_ip} dns-server=8.8.8.8"
        print(f"Comando de network: {comando_network}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando_network)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error al ejecutar el comando de network: {errores}")
            cliente_ssh.close()
            return False

        # Crear el servidor DHCP
        comando_dhcp_server = f"/ip/dhcp-server/add name={ether} interface={ether} address-pool={ether} disabled=no comment=SpiderNET_{ether}"
        print(f"Comando DHCP Server: {comando_dhcp_server}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando_dhcp_server)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error al ejecutar el comando DHCP Server: {errores}")
            cliente_ssh.close()
            return False

        cliente_ssh.close()
        return True

    except Exception as error:
        print(f"Error en la conexión SSH: {error}")
        return False

def crearQueueParent(name, direccion_ip, max_limit, host, port, username, password, mikrotik):
    try:
        # Eliminar espacios al inicio y final, y quitar todos los espacios intermedios
        name = name.strip()            # elimina espacios al inicio y final
        name = re.sub(r'\s+', '', name) # elimina todos los espacios

        # Opcionalmente, eliminar cualquier carácter que no sea una letra (mayúsculas o minúsculas)
        name = re.sub(r'[^A-Za-z]', '', name)

        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)
        address = obtener_subred(direccion_ip)
        comando = f"/queue/simple/add name={name} target={address} max-limit={max_limit}"

        print(f"Comando enviado: {comando}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()
    
        if errores:
            print(f"Errores con el comando SSH {errores}")
            cliente_ssh.close()
            return False
        insertar_queue_parent(nombre=name, subred=address, max_limit=max_limit, mikrotik=mikrotik)
        cliente_ssh.close()
        return True
    
    except Exception as r:
        print(f"Error en conexion SSH {r}")
        return False
    

def extract_number(s):
    """Extrae el valor numérico de una cadena, por ejemplo, '15M' → 15.0"""
    match = re.search(r"(\d+(?:\.\d+)?)", s)
    if match:
        return float(match.group(1))
    return 0.0

def crearQueueSimple(nombre, direccion_ip, max_limit, credenciales, parent, tiempo):
        # Eliminar espacios al inicio y final, y quitar todos los espacios intermedios
    nombre = nombre.strip()            # elimina espacios al inicio y final
    nombre = re.sub(r'\s+', '', nombre) # elimina todos los espacios

        # Opcionalmente, eliminar cualquier carácter que no sea una letra (mayúsculas o minúsculas)
    nombre = re.sub(r'[^A-Za-z]', '', nombre)   
        # Eliminar espacios al inicio y final, y quitar todos los espacios intermedios
    parent = parent.strip()            # elimina espacios al inicio y final
    parent = re.sub(r'\s+', '', parent) # elimina todos los espacios

        # Opcionalmente, eliminar cualquier carácter que no sea una letra (mayúsculas o minúsculas)
    parent = re.sub(r'[^A-Za-z]', '', parent)   
    """
    Crea un cliente en queue simple con rafaga.
    
    Parámetros:
      - nombre: nombre del cliente.
      - direccion_ip: target IP del cliente.
      - max_limit: string con el formato "15M/15M" (subida/bajada).
      - credenciales: tupla con (username, password, host, port).
      - parent: nombre del queue parent.
      - tiempo: burst time.
    """
    username, password, host, port = credenciales

    # Extraer valores numéricos de max_limit
    parts = max_limit.split('/')
    max_upload = extract_number(parts[0])   # Ej.: "15M" → 15.0
    max_download = extract_number(parts[1]) # Ej.: "15M" → 15.0

    # Calcular Burst Limit (1.5x del Max Limit)
    burst_upload = max_upload * 1.5
    burst_download = max_download * 1.5

    # Calcular Burst Threshold (75% del Max Limit) - Ahora redondeamos a enteros
    threshold_upload = int(max_upload * 0.75)
    threshold_download = int(max_download * 0.75)

    # Formatear los valores agregando la "M" al final
    burst_limit = f"{burst_upload:.0f}M/{burst_download:.0f}M"
    burst_threshold = f"{threshold_upload}M/{threshold_download}M"

    try:
        # Conexión SSH a MikroTik
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=int(port), username=username, password=password)

        # Construir el comando
        comando = (
            f"/queue/simple/add name={nombre} target={direccion_ip} max-limit={max_limit} "
            f"parent={parent} burst-limit={burst_limit} burst-threshold={burst_threshold} burst-time={tiempo}"
        )
        print(f"Comando enviado: {comando}")

        stdin, stdout, stderr = cliente_ssh.exec_command(comando)
        stdin.flush()
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Errores con el comando SSH: {errores}")
            cliente_ssh.close()
            return False

        cliente_ssh.close()
        return True

    except Exception as e:
        print(f"Error en conexión SSH: {e}")
        return False


def eliminarSimpleQueue(credenciales, direccion_ip):
    """_summary_

    Args:
        credenciales (string): una tupla con las credenciales
        direccion_ip (strind): un string con la direccion ip

    Returns:
        bool : retorna false si falla la ejecucion del comando o true en su exitp
    """
    sub_red = "/32"
    username = credenciales[0]
    password = credenciales[1]
    host = credenciales[2]
    port = credenciales[3]
    comando = f"/queue/simple/remove [find where target={direccion_ip}{sub_red}]"    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        stdin, stdout, stderr = ssh.exec_command(comando)

        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Errores en ejecucion del comando {errores}")
            ssh.close()
        
        ssh.close()
        return True
    
    except Exception as r:
        print(f"Error en conexion SSH {r}")
        return False
    
def aplicarFirewall(host, port, username, password):
    comandos = [
        "/ip/firewall/filter/add chain=forward action=drop src-address-list=corte comment=corteDeInternet",
        "/ip/firewall/filter/add chain=forward action=drop dst-address-list=corte comment=corteDeInternet",
        "/ip/firewall/nat/add chain=srcnat action=masquerade src-address-list=Internet",
        "/ip/firewall/nat/add chain=srcnat action=masquerade dst-address-list=Internet",
        "/system/ntp/client/set enabled=yes servers=162.159.200.1,216.239.35.0",
        "/system/clock/set time-zone-name=America/Mexico_City time-zone-autodetect=no"
    ]

    # Crear cliente SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Aceptar claves automáticamente

    try:
        print(f"Conectando a {host}:{port}...")
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)

        for comando in comandos:
            print(f"Ejecutando: {comando}")
            stdin, stdout, stderr = client.exec_command(comando)
            
            salida = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if salida:
                print(f"✔️ Salida: {salida}")

            if error:
                print(f"❌ Error: {error}")
        
        client.close()

    except Exception as e:
        print(f"⚠️ Error al conectar o ejecutar comandos: {e}")
        return False

    finally:
        client.close()
        print("Conexión cerrada.")
        return True

def eliminarQueueParent(username, password, host, port, segmento_red):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #aceptamos las llaves

    try:
        ssh.connect(host, port, username, password, timeout=10)
        comando = f"/queue/simple/remove [find where target={segmento_red}]"
        stdin, stdout, stderr = ssh.exec_command(comando)

        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"Error en ejecutar el comando {errores}")
        else:
            print(f"Comando ejecuato {salida}")
    
        ssh.close()
        return True
    
    except Exception as r:
        print(f"Error en conexion SSH {r}")
        return False
    
def actualizarQueue(username, password, host, port, segmento_red, nombre, max_limit):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Conectar con MikroTik
        ssh.connect(hostname=host, port=port, username=username, password=password, timeout=10)

        # Comando para actualizar la queue
        comando = f'/queue/simple/set [find where target={segmento_red}] name="{nombre}" max-limit={max_limit}'
        stdin, stdout, stderr = ssh.exec_command(comando)

        # Leer salida y errores
        salida = stdout.read().decode()
        errores = stderr.read().decode()  # Aquí estaba el error, estabas leyendo stdout en lugar de stderr

        if errores:
            print(f"Error al ejecutar el comando: {errores}")
        else:
            print(f"Comando ejecutado correctamente: {salida}")

        ssh.close()
        return True
    except Exception as e:
        print(f"Error en comando SSH: {e}")
        return False
