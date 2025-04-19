import paramiko
from d_consultas import consultarCredenciales

def obtener_leases_por_nombre(nombre_mikrotik):
    try:
        cred = consultarCredenciales(nombre_mikrotik)
        if not cred:
            return []

        username, password, ip, port = cred

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=int(port), username=username, password=password, timeout=5)

        comando = '/ip dhcp-server lease print detail without-paging'
        stdin, stdout, stderr = ssh.exec_command(comando)
        salida = stdout.read().decode('utf-8')

        ssh.close()

        return parsear_leases(salida)

    except Exception as e:
        print(f"❌ Error al obtener leases: {e}")
        return []

def parsear_leases(salida):
    leases = []
    lease_actual = {}

    for linea in salida.splitlines():
        if linea.strip() == "":
            continue

        if "address=" in linea and lease_actual:
            if lease_actual.get("address") and lease_actual.get("mac-address"):
                leases.append(lease_actual)
            lease_actual = {}

        partes = linea.strip().split(" ")
        for p in partes:
            if "=" in p:
                clave, valor = p.split("=", 1)
                lease_actual[clave.strip()] = valor.strip().strip('"')

    if lease_actual.get("address") and lease_actual.get("mac-address"):
        leases.append(lease_actual)

    # Asegurar que todas las claves estén presentes
    claves = ["address", "mac-address", "host-name", "expires-after", "status"]
    leases_limpios = []
    for l in leases:
        leases_limpios.append({clave: l.get(clave, "") for clave in claves})

    return leases_limpios

def hacer_estatico(nombre_mikrotik, ip):
    try:
        cred = consultarCredenciales(nombre_mikrotik)
        if not cred:
            return False

        username, password, host, port = cred

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=int(port), username=username, password=password, timeout=5)

        comando = f"/ip dhcp-server lease make-static [find address={ip}]"
        ssh.exec_command(comando)
        ssh.close()
        return True

    except Exception as e:
        print(f"❌ Error al hacer lease estático: {e}")
        return False
