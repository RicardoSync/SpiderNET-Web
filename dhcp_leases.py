import paramiko
import re
def get_dhcp_leases(username, password, hostname, port):
    command = '/ip/dhcp-server/lease/print'
    
    # Conexión SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)
    
    # Ejecuta el comando
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    ssh.close()
    
    leases = []
    # Divide la salida en líneas
    lines = output.splitlines()
    # Utiliza una expresión regular para detectar líneas de leases
    for line in lines:
        if re.match(r'^\s*\d+\s+D', line):
            # Se asume que los campos están separados por 2 o más espacios
            parts = re.split(r'\s{2,}', line.strip())
            # Se espera tener al menos 7 elementos:
            # [índice, ADDRESS, MAC-ADDRESS, HOST-NAME, SERVER, STATUS, LAST-SEEN]
            if len(parts) >= 7:
                lease = {
                    'address': parts[1],
                    'mac': parts[2],
                    'host': parts[3],
                    'server': parts[4],
                    'status': parts[5],
                    'last_seen': parts[6]
                }
                leases.append(lease)
    return leases