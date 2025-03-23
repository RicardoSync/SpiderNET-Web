import paramiko

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