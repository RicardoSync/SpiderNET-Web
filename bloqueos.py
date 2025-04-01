from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from ssh_pcq import *
from ssh_pppoe import *
from flask import *
from bloqueos_bd import *

def procesar_bloqueo_clinete(id):
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

def procesar_desbloqueo_cliente(id):
     # Se obtienen los datos enviados desde el formulario del modal
    # Obtener valores individuales
    ip_cliente = request.form.get('direccion_addres_cliente')
    microtik = request.form.get('microtik')

    print(f"La ip del cliente es {ip_cliente} con microtik asociado {microtik} desde el model")    
    # Se consultan las credenciales para el microtik indicado
    credenciales = consultarCredenciales(microtik)
    if credenciales:
        ok = desbloqueo_mantecoso(credenciales, ip_cliente)
        if ok:
            estado_bloqueado(estado="Activo", id=id)
            flash("Cliente desbloqueado", "success")  # Tipo success para éxito
        else:
            flash("Tenemos problemas con el desbloqueo", "danger")  # Tipo danger para error
    else:
        flash(f"No tenemos credenciales para ese MikroTik: {microtik}", "warning")  # Tipo warning para advertencia
    
    return redirect(url_for("clientes_bloqueados"))

def procesar_lista_bloqueados():
    clientes = consultar_clientes_bloqueados()
    return render_template("bloqueados.html", clientes=clientes)
