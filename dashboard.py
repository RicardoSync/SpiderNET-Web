from flask import *
from d_contador import *
from d_login import *
from d_consultas import *
from datetime import timedelta

def procesar_dashboard_raiz():
    total_clientes = contador_clientes()  # Llamada a la función
    total_equipos = contador_equipos()
    total_pagos = contador_pagos()
    total_microtiks = contador_mikrotik()
    return render_template("dashboard.html",
                        total_clientes=total_clientes,
                        total_equipos=total_equipos,
                        total_pagos=total_pagos,
                        total_microtiks=total_microtiks,
                        total_instalaciones=contado_instalaciones(),
                        total_soporte=contador_soporte(),
                        total_tickets=contador_tickets(),
                        pago=consultar_pagos_registrados())

def procesar_dashboard_inicio_sesion():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        tipo_usuario = login(username, password)

        if tipo_usuario is False:
            flash("❌ Usuario o contraseña incorrectos.")
            return render_template("login.html")

        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=15)
        session['usuario'] = username
        session['rol'] = tipo_usuario

        if tipo_usuario == 0:
            return redirect(url_for("dashboard"))
        elif tipo_usuario == 1:
            return render_template("tecnico_inicio.html")
        elif tipo_usuario == 2:
            return redirect(url_for("cliente_panel", id_cliente=username))

def procesar_el_cliente(id_cliente):
    cliente = obtener_info_cliente(id_cliente)
    pagos = obtener_pagos_cliente(id_cliente)
    paquete = obtener_nombre_paquete(cliente["id_paquete"]) if cliente else "Desconocido"
    return render_template("cliente_inicio.html", cliente=cliente, pagos=pagos, paquete=paquete)