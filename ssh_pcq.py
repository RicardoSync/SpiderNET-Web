import paramiko
import re
from ip_pool import generar_rango_ips, obtener_subred

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

        stdin, stout, stderr = cliente_ssh.exec_command(f"/ip/firewall/address-list/add list=corte address={ip_cliente}")

        salida = stout.read().decode()
        errores = stderr.read().decode()

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

        comando = f"/ip/firewall/address-list/remove [find address={ip_cliente} list=corte]"

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


#"/ip/dhcp-server/add name="+name + " interface="+interfaz + " address-pool=" + pool +" disabled=no comment="+comentario;