from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *
from ssh_pcq import *

def procesar_configuracion_pcq():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("ip")
        direccion_ip = request.form.get("address")
        ether = request.form.get("interface")
        port = request.form.get("port")
        ok = creacionAddressList(username, password, host, port, direccion_ip, ether)
        if ok:
            flash("Creacion de Addres y pol con exito", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("Tenemos problemas con su creacion", "danger")
            return redirect(url_for("lista_microtiks"))
        
