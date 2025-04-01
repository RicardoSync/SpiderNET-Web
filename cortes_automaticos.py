import mysql.connector
import paramiko
import schedule
import time
import datetime

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_password',
    'database': 'spidernet_web'
}

def obtener_clientes_sin_pago(cursor):
    # Consulta para obtener clientes con corte hoy y sin registro de pago en el día actual
    query = ("""
        SELECT c.id, c.nombre, c.ip_cliente, c.id_microtik
        FROM clientes c
        LEFT JOIN pagos p ON c.id = p.id_cliente 
            AND DAY(p.fecha_pago) = DAY(CURDATE())
            AND MONTH(p.fecha_pago) = MONTH(CURDATE())
        WHERE c.dia_corte = DAY(CURDATE()) 
            AND p.id_cliente IS NULL;
    """)
    cursor.execute(query)
    return cursor.fetchall()

def obtener_credenciales_mikrotik(cursor, id_microtik):
    # Consulta para obtener credenciales del dispositivo Mikrotik
    query = "SELECT ip, username, password, port FROM credenciales_microtik WHERE id = %s"
    cursor.execute(query, (id_microtik,))
    return cursor.fetchone()

def bloquear_cliente_en_mikrotik(credenciales, ip_cliente):
    """
    Se conecta al dispositivo Mikrotik usando SSH y envía el comando para bloquear al cliente.
    El comando es un ejemplo y puede ajustarse según tus necesidades y la configuración del dispositivo.
    """
    ip, username, password, port = credenciales
    try:
        # Configuración y conexión SSH con Paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=int(port) if port else 22, username=username, password=password, timeout=10)
        
        # Comando de ejemplo para agregar la IP del cliente a una lista de bloqueo
        comando = f'/ip firewall address-list add address={ip_cliente} list=blocked comment="Bloqueo automático por falta de pago"'
        stdin, stdout, stderr = ssh.exec_command(comando)
        
        # Se puede leer stdout y stderr para fines de log o depuración
        salida = stdout.read().decode()
        errores = stderr.read().decode()
        if errores:
            print(f"Error al ejecutar comando en Mikrotik {ip}: {errores}")
        else:
            print(f"Cliente con IP {ip_cliente} bloqueado en Mikrotik {ip}.")
        ssh.close()
    except Exception as e:
        print(f"Error conectando a Mikrotik {ip}: {e}")

def run_cut():
    print(f"\n[{datetime.datetime.now()}] Inicio del proceso de corte automático")
    
    try:
        # Conexión a la base de datos
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor(dictionary=True)
        
        # Obtener clientes que deben ser bloqueados
        clientes = obtener_clientes_sin_pago(cursor)
        print(f"Clientes sin pago hoy: {len(clientes)}")
        
        for cliente in clientes:
            id_cliente = cliente['id']
            nombre_cliente = cliente['nombre']
            ip_cliente = cliente['ip_cliente']
            id_microtik = cliente['id_microtik']
            
            # Obtener credenciales de Mikrotik
            credenciales = obtener_credenciales_mikrotik(cursor, id_microtik)
            if credenciales is None:
                print(f"No se encontraron credenciales para el Mikrotik del cliente {nombre_cliente} (ID: {id_cliente}).")
                continue
            
            # Bloquear el cliente en el Mikrotik correspondiente
            bloquear_cliente_en_mikrotik(credenciales, ip_cliente)
        
        cursor.close()
        db.close()
        print(f"[{datetime.datetime.now()}] Proceso finalizado.\n")
    
    except mysql.connector.Error as err:
        print("Error en la conexión a la base de datos: {}".format(err))
    except Exception as e:
        print("Ocurrió un error: ", e)

# Programar la ejecución diaria a las 05:00 PM
schedule.every().day.at("17:00").do(run_cut)

if __name__ == '__main__':
    print("Servicio de corte automático iniciado. Esperando a la siguiente ejecución programada...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Revisa cada 60 segundos
