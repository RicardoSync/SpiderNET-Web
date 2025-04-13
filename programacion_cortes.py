from datetime import datetime, timedelta
import paramiko
import os

def get_fecha_corte_siguiente_mes(dia_corte: int) -> str:
    hoy = datetime.now()
    año = hoy.year
    mes = hoy.month + 1

    # Si pasa de diciembre
    if mes > 12:
        mes = 1
        año += 1

    # Obtener el último día del mes
    ultimo_dia = (datetime(año, mes % 12 + 1, 1) - timedelta(days=1)).day
    dia_final = min(dia_corte, ultimo_dia)

    fecha_corte = datetime(año, mes, dia_final)
    return fecha_corte.strftime('%b/%d/%Y').lower()  # ej: apr/15/2025



def create_task(name_cliente, address, username, password, host, dia_corte):
    try:
        fecha_corte = get_fecha_corte_siguiente_mes(dia_corte)
        comando = f'/system/scheduler/add name="{name_cliente}" start-date={fecha_corte} start-time=00:00:00 interval=1m on-event="/ip firewall address-list add list=corte address={address}"'

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command(comando)
        salida = stdout.read().decode()
        error = stderr.read().decode()

        print(f"[✅] Tarea de corte creada para: {fecha_corte}")
        if error:
            print(f"[⚠️] Advertencia al crear tarea: {error}")

        ssh.close()
        return True, f"Tarea creada para el {fecha_corte}"
    except Exception as e:
        print(f"[❌] Error al crear la tarea de corte: {e}")
        return False, str(e)
    

def eliminar_y_recrear_task(name_cliente, address, username, password, host, dia_corte):
    try:
        comando_eliminar = f'/system/scheduler/remove [find name="{name_cliente}"]'

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)

        stdin, stdout, stderr = ssh.exec_command(comando_eliminar)
        salida = stdout.read().decode()
        error = stderr.read().decode()

        print(f"[✅] Tarea anterior eliminada: {name_cliente}")
        if error:
            print(f"[⚠️] Error al eliminar (puede ser que no existía): {error}")

        ssh.close()
    except Exception as e:
        print(f"[⚠️] No se pudo eliminar la tarea anterior: {e}")
    
    # Crear nueva tarea de corte
    return create_task(name_cliente, address, username, password, host, dia_corte)