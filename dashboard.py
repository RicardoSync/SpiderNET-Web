from flask import *
from d_contador import *
from d_login import *

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
                        total_tickets=contador_tickets())

def procesar_dashboard_inicio_sesion():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        tipo_usuario = login(username, password)  # retorna 0, 1, 2 o False

        if tipo_usuario == 0:
            return redirect(url_for("dashboard"))

        elif tipo_usuario == 1:
            print("Inicio sesión un TÉCNICO")
            return render_template("tecnico_inicio.html")

        elif tipo_usuario == 2:
            print("Inicio sesión un CLIENTE")
            return render_template("cliente_inicio.html")

        else:
            flash("Usuario o contraseña incorrectos.")
            return render_template("login.html")
