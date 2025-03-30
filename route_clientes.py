from flask import *
from d_insert import insertarCliente
from d_consultas import *
from d_update import *
from d_eliminar import *
from ssh_pcq import *
from bloqueos_bd import *

def crear_cliente():
    if request.method == "POST":
        nombre = request.form.get("nombreNuevo")
        paquete = request.form.get("lsita_paquetes")
        ip_cliente = request.form.get("direccionip")
        dia_corte = request.form.get("dia_corte")
        antena_ap = request.form.get("lista_antenas")
        servicio = request.form.get("servicios_bien_perrotes_alv")
        microtik = request.form.get("lista_microtik")

        print(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik)

        ok = insertarCliente(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik)
        if ok:
            return redirect(url_for("lista_clientes"))
        else:
            return render_template("error.html"), 500
        
def lista_clientes():
    cliente = consultarClientes()
    antenas = consutlarAntena()
    paquetes = consutlarPaquete()
    return render_template("lista_clientes.html", clientes=cliente, antens=antenas, paquetes=paquetes, servicios=consultarServicio(),
                           microtiks=consultarMicrotik(), queues_colas=consultarQeue())


def eidtar_cliente(id):
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

def eliminar_cliente(id):
    ok = eliminar_cliente_chido(id)    
    if ok:
        return redirect(url_for("lista_clientes"))
    else:
        return render_template("error.html"), 500
    
def bloquear_cliente_pcq(id):
    # Se obtienen los datos enviados desde el formulario del modal
    # Obtener valores individuales
    direccion_ip = request.form.get('direccion_addres_cliente')
    microtik = request.form.get('microtik')
    print(id)
    print(direccion_ip, microtik)
    
    # Se consultan las credenciales para el microtik indicado
    credenciales = consultarCredenciales(microtik)
    print(credenciales)
    if credenciales:
        # Ejecuta el comando de bloqueo
        ok = bloquear_cliente_address_list(credenciales, direccion_ip)
        if ok:
            estado_bloqueado(estado="Bloqueado", id=id)
            flash("Cliente bloqueado", "success")  # Tipo success para éxito
        else:
            flash("Tenemos problemas con el bloqueo", "danger")  # Tipo danger para error
    else:
        flash(f"No tenemos credenciales para ese MikroTik: {microtik}", "warning")  # Tipo warning para advertencia
    
    return redirect(url_for("lista_clientes"))