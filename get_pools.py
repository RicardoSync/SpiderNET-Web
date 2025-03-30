import paramiko
import re
def get_pool_list_nuevo(host, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=int(port), username=username, password=password)
        
        # Ejecuta el comando para obtener las IP Pools
        stdin, stdout, stderr = client.exec_command("/ip/pool/print")
        output = stdout.read().decode('utf-8')
        client.close()

        # Procesamos la salida para extraer el nombre de la pool.
        pools = []
        for line in output.splitlines():
            # Evitamos cabecera y líneas vacías
            if line.strip() == "" or "NAME" in line or "Columns:" in line:
                continue
            # Suponiendo que el formato es: <número> pool_name ranges...
            match = re.match(r"\s*\d+\s+\S+\s+(\S+)", line)
            if match:
                pools.append(match.group(1))
        return pools

    except Exception as e:
        print("Error al obtener IP Pools:", e)
        return []
