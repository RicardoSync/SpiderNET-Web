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

        ok = login(username, password)
        if ok:
            print(ok)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")
        
