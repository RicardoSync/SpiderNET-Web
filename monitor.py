import paramiko

def obtener_trafico_mikrotik(host, port, username, password, interface):
    # Creamos el cliente SSH
    client = paramiko.SSHClient()
    # Acepta la clave del host automáticamente (no recomendado en producción)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        # Ejecuta el comando. Se agrega "once" para obtener una única lectura.
        comando = f"/interface/monitor-traffic {interface} once"
        stdin, stdout, stderr = client.exec_command(comando)
        salida = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            raise Exception(f"Error en la ejecución del comando: {error}")
    finally:
        client.close()
    return salida



def obtener_trafico_queue_cliente(host, port, username, password, interface):
    """
    [admin@MikroTik] > /queue/simple/print stats interval=1  where target=172.168.10.0/24    
    Flags: X - disabled, I - invalid; D - dynamic 
    0    name="Lap" target=172.168.10.0/24 rate=2.0Mbps/15.0Mbps total-rate=0bps packet-rate=734/1751 total-packet-rate=0 queued-bytes=0/0 total-queued-bytes=0 queued-packets=0/0 
        total-queued-packets=0 bytes=6520205850/123042156517 total-bytes=0 packets=40608346/99203744 total-packets=0 dropped=0/1195 total-dropped=0 


    """
    # Creamos el cliente SSH
    client = paramiko.SSHClient()
    # Acepta la clave del host automáticamente (no recomendado en producción)
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=host, port=port, username=username, password=password, timeout=10)
        # Ejecuta el comando. Se agrega "once" para obtener una única lectura.
        comando = f"/interface/monitor-traffic {interface} once"
        stdin, stdout, stderr = client.exec_command(comando)
        salida = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        if error:
            raise Exception(f"Error en la ejecución del comando: {error}")
    finally:
        client.close()
    return salida