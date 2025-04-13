from flask import *
from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from ssh_pcq import desbloqueo_mantecoso
from programacion_cortes import *
from bloqueos_bd import *

def procesar_lista_de_pagos():
    nombre = request.args.get("nombre", "").strip()
    fecha_inicio = request.args.get("fecha_inicio", "")
    fecha_fin = request.args.get("fecha_fin", "")

    todos_los_pagos = consultar_pagos_registrados()
    
    # Filtrado
    pagos_filtrados = []
    for pago in todos_los_pagos:
        nombre_cliente, monto, fecha_pago, metodo = pago
        coincide_nombre = nombre.lower() in nombre_cliente.lower() if nombre else True
        coincide_fecha = True
        if fecha_inicio and fecha_fin:
            coincide_fecha = fecha_inicio <= fecha_pago.strftime("%Y-%m-%d") <= fecha_fin
        elif fecha_inicio:
            coincide_fecha = fecha_pago.strftime("%Y-%m-%d") >= fecha_inicio
        elif fecha_fin:
            coincide_fecha = fecha_pago.strftime("%Y-%m-%d") <= fecha_fin

        if coincide_nombre and coincide_fecha:
            pagos_filtrados.append(pago)

    return render_template("pagos.html", pagos=pagos_filtrados)

def procesar_registro_pago(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        paquete = request.form["paquete_cliente"]
        ip = request.form["direccion_ip"]
        mikrotik = request.form["mikrotik"]
        metodo = request.form["metodo_pago"]
        cantidad = int(request.form["cantidad_pago"])  # conversión a número
        dia_corte = int(request.form["dia_cote"])
        
        print(f"Nombre: {nombre}")
        print(f"Paquete: {paquete}")
        print(f"IP: {ip}")
        print(f"Mikrotik: {mikrotik}")
        print(f"Metodo de pago: {metodo}")
        print(f"Cantidad: {cantidad}")

        precio = obtener_precio_paquete(paquete)
        if precio is None:
            return "Error: Paquete no encontrado", 404
        if isinstance(precio, tuple):
            precio = precio[0]

        cambio = cantidad - precio
        if cambio < 0:
            flash ("Error: El monto ingresado es menor al precio del paquete", "danger")
            return redirect(url_for("lista_clientes"))
        
        if not insertar_pago_cliente(id, precio, metodo, cantidad, cambio):
            flash("Error: No se pudo registrar el pago", "danger")
            return redirect(url_for("lista_clientes"))
        

        credenciales = consultarCredenciales(mikrotik)
        if credenciales is None:
            flash("Error: Mikrotik no encontrado", "danger")
            return redirect(url_for("lista_clientes"))
        
        username = credenciales[0]
        password = credenciales[1]
        host = credenciales[2]
        port = credenciales[3]

        if not eliminar_y_recrear_task(nombre, ip, username, password, host, dia_corte):
            flash("Error: No se pudo programar el corte", "danger")
            return redirect(url_for("lista_clientes"))
        
        if not desbloqueo_mantecoso(credenciales, ip):
            flash("Error: No se pudo desbloquear el cliente", "danger")
            return redirect(url_for("lista_clientes"))

        if not estado_bloqueado("Activo", id):
            flash("Error: No se pudo actualizar el estado del cliente", "danger")
            return redirect(url_for("lista_clientes"))
        

        flash("Pago registrado exitosamente", "success")
        return redirect(url_for("lista_clientes"))
    

    
    """Lo primero es obtener el precio del paquete, despues con los datos
    id cliente, monto (precio), fecha es automaticoa, metodo de pago lo vamos insertar
    Despues de eso actualizamos el scheduler en mikrotik y desbloqueamos en caso de estar bloqueado"""