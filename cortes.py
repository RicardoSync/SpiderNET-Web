#!/usr/bin/env python3

import mysql.connector
import paramiko
import requests
import urllib.parse
import time
from datetime import date

def bloquear_cliente_address_list(credenciales, ip_cliente, nombre_cliente):
    username, password, host, port = credenciales
    port = int(port) if port else 22

    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)

        comentario = f'"{nombre_cliente}"'
        comandos = [
            f'/ip/firewall/address-list/add list=corte address={ip_cliente} comment={comentario}'
        ]

        for comando in comandos:
            stdin, stdout, stderr = cliente_ssh.exec_command(comando)
            salida = stdout.read().decode()
            errores = stderr.read().decode()
            if errores:
                print(f"⚠️ Error SSH en comando: {comando}\n{errores}")

        cliente_ssh.close()
        print(f"✅ IP {ip_cliente} bloqueada y comentada como {nombre_cliente}")
        return True

    except Exception as e:
        print(f"❌ Error SSH para {ip_cliente}: {e}")
        return False

def verificar_address_list(credenciales, ip_cliente, nombre_cliente):
    username, password, host, port = credenciales
    port = int(port) if port else 22

    try:
        cliente_ssh = paramiko.SSHClient()
        cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        cliente_ssh.connect(host, port=port, username=username, password=password)

        comando_check = f'/ip/firewall/address-list/print where list=corte and address={ip_cliente}'
        stdin, stdout, stderr = cliente_ssh.exec_command(comando_check)
        salida = stdout.read().decode()
        errores = stderr.read().decode()

        if errores:
            print(f"⚠️ Error verificando IP {ip_cliente}: {errores}")
            cliente_ssh.close()
            return False

        if ip_cliente in salida:
            cliente_ssh.close()
            return True
        else:
            comentario = f'"{nombre_cliente}"'
            comando_add = f'/ip/firewall/address-list/add list=corte address={ip_cliente} comment={comentario}'
            cliente_ssh.exec_command(comando_add)
            cliente_ssh.close()
            print(f"🔄 IP {ip_cliente} re-agregada a address-list 'corte'")
            return True

    except Exception as e:
        print(f"❌ Error SSH al verificar {ip_cliente}: {e}")
        return False

def enviar_mensaje_whatsapp(numero, apikey, nombre, empresa, direccion, telefono_empresa):
    mensaje = f"👋 ¡Hola {nombre}!\n\n🚫 Tu servicio ha sido *suspendido automáticamente* por el sistema de *{empresa}*.\n\n📍 Dirección registrada: {direccion}\n\n⚠️ Este es un mensaje automático enviado por nuestro 🤖 bot.\n❗ *Por favor no respondas a este mensaje.*\n📞 Contacto: *{telefono_empresa}*\n\nGracias por tu comprensión 🙏"
    texto = urllib.parse.quote(mensaje)
    url = f"https://api.callmebot.com/whatsapp.php?phone={numero}&text={texto}&apikey={apikey}"

    try:
        r = requests.get(url)
        if r.status_code == 200:
            print(url)
            print(f"✅ WhatsApp enviado a {nombre}")
        else:
            print(f"⚠️ Error al enviar WhatsApp a {nombre}: {r.status_code}")
            print(url)
    except Exception as e:
        print(f"❌ Error al enviar WhatsApp a {nombre}: {e}")

def ejecutar_cortes():
    while True:
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="adminet",
                password="zerocuatro04",
                database="adminet_test_vps"
            )
            cursor = conn.cursor(dictionary=True)

            hoy = date.today()
            dia_actual = hoy.day

            # 1. Verificar que los bloqueados sigan en Address List
            cursor.execute("""
            SELECT c.id, c.nombre, c.ip_cliente, c.id_microtik,
                   m.username, m.password, m.ip AS host, m.port
            FROM clientes c
            JOIN credenciales_microtik m ON c.id_microtik = m.id
            WHERE c.estado = 'Bloqueado' AND c.ip_cliente IS NOT NULL
            """)
            bloqueados = cursor.fetchall()

            print(f"🔍 Verificando que {len(bloqueados)} clientes bloqueados sigan en Address List...")

            for cliente in bloqueados:
                credenciales = (cliente['username'], cliente['password'], cliente['host'], cliente['port'])
                verificar_address_list(credenciales, cliente['ip_cliente'], cliente['nombre'])

            # 2. Procesar cortes de clientes activos
            query = """
            SELECT c.id, c.nombre, c.telefono, c.direccion, c.ip_cliente, c.dia_corte, c.id_microtik,
                   d.nombreWisp AS nombre_empresa, d.telefono AS telefono_empresa,
                   m.username, m.password, m.ip AS host, m.port,
                   a.apikey,
                   (SELECT COUNT(*) FROM pagos p WHERE p.id_cliente = c.id AND MONTH(p.fecha_pago) = MONTH(CURDATE()) AND YEAR(p.fecha_pago) = YEAR(CURDATE())) AS pagos_mes
            FROM clientes c
            JOIN datosEmpresa d ON d.id = 1
            JOIN credenciales_microtik m ON c.id_microtik = m.id
            LEFT JOIN clientes_apikeys a ON c.id = a.id_cliente AND a.activo = 1
            WHERE c.estado = 'Activo'
            """ # ⚡ CAMBIO AQUI

            cursor.execute(query)
            clientes = cursor.fetchall()

            for cliente in clientes:
                if cliente['pagos_mes'] == 0 and dia_actual >= cliente['dia_corte']: # ⚡ CAMBIO AQUI
                    id_cliente = cliente['id']
                    print(f"🔒 Suspendiendo a: {cliente['nombre']}")

                    # Actualizar estado
                    cursor.execute("UPDATE clientes SET estado = 'Bloqueado' WHERE id = %s", (id_cliente,))
                    conn.commit()

                    # Enviar WhatsApp si tiene datos
                    if cliente['telefono'] and cliente['apikey']:
                        enviar_mensaje_whatsapp(cliente['telefono'], cliente['apikey'], cliente['nombre'],
                                                cliente['nombre_empresa'], cliente['direccion'], cliente['telefono_empresa'])

                    # Bloquear IP en MikroTik
                    credenciales = (cliente['username'], cliente['password'], cliente['host'], cliente['port'])
                    bloquear_cliente_address_list(credenciales, cliente['ip_cliente'], cliente['nombre'])

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"❌ Error de MySQL: {err}")

        except Exception as e:
            print(f"❌ Error general: {e}")

        print("🕐 Esperando 5 minutos para volver a verificar...\n")
        time.sleep(300)  # 5 minutos

if __name__ == "__main__":
    try:
        print("🚀 Script de cortes automáticos iniciado. Presiona Ctrl+C para detener.")
        ejecutar_cortes()
    except KeyboardInterrupt:
        print("\n🛑 Script detenido manualmente por el usuario.")
