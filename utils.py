import subprocess
import paramiko
from flask import *

def verificar_conexion_mikrotik(ip):
    try:
        resultado = subprocess.run(
            ["ping", "-c", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error al verificar conexión con MikroTik {ip}: {e}")
        return False
def verificar_ssh_mikrotik(ip, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=ip,
            port=int(port),
            username=username,
            password=password,
            timeout=5
        )

        ssh.close()
        return True

    except Exception as e:
        flash(f"Error: {e}", "danger")
        return False