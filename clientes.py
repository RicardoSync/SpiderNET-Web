from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *

def procesar_cliente_creacion():
    if request.method == "POST":
        nombre = request.form.get("nombreNuevo")
        paquete = request.form.get("lsita_paquetes")
        ip_cliente = request.form.get("direccionip")
        dia_corte = request.form.get("dia_corte")
        antena_ap = request.form.get("lista_antenas")
        servicio = request.form.get("servicios_bien_perrotes_alv")
        microtik = request.form.get("lista_microtik")

        print(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik)

        if insertarCliente(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik):
            flash("Cliente registrado con exito", "success")
            return redirect(url_for("lista_clientes"))
        else:
            flash("El cliente no se registro", "danger")            
            return redirect(url_for("lista_clientes"))
        
def procesar_lista_clientes():
    cliente = consultarClientes()
    antenas = consutlarAntena()
    paquetes = consutlarPaquete()
    return render_template("lista_clientes.html", clientes=cliente, antens=antenas, paquetes=paquetes, servicios=consultarServicio(),
                           microtiks=consultarMicrotik(), queues_colas=consultarQeue())

def procesar_edicion_del_cliente(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        paquete = request.form.get("lsita_paquetes")
        ip_cliente = request.form.get("direccionIp")
        dia_corte = request.form.get("dia_corte")
        antena_ap = request.form.get("lista_antenas")
        servicio = request.form.get("lista_servicio")
        microtik = request.form.get("lista_microtik")

        ok = actualizarCliete(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik, id)
        if ok:
            return redirect(url_for("lista_clientes"))
        else:
            return render_template("error.html"), 500

def procesar_elimiacion_del_cliente(id):
    if eliminar_cliente_chido(id):
        flash("Cliente eliminado con exito", "succes")
        return redirect(url_for("lista_clientes"))
    else:
        flash("El cliente no se elimino", "danger")
        return redirect(url_for("lista_clientes"))
