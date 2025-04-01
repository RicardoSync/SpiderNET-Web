from flask import *
from d_insert import *
from ssh_pcq import *
from d_consultas import *
from d_eliminar import *

def procesar_creacion_queue_parent_del_bueno():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("ip")
        direccion_ip = request.form.get("address")
        ether = request.form.get("interface")
        port = request.form.get("port") 
        name = request.form.get("nameParent")
        max_limit = request.form.get("max_limit")

        ok = crearQueueParent(name, direccion_ip, max_limit, host,
                              port, username, password)

        if ok:
            flash("Creacion de cola exitoso!", "success")        
            return redirect(url_for("lista_microtiks"))
        else:
            flash("No logramos crear la cola", "danger")
            return redirect(url_for("lista_microtiks"))

def procesar_cargar_queue():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion_ip = request.form.get("direccionIp")
        paquete = request.form.get("paquete")
        microtik = request.form.get("microtik")
        parent = request.form.get("queueParent")

        print(nombre, direccion_ip, paquete, microtik, parent)

        credenciales = consultarCredenciales(nombre=microtik)

        if credenciales:
            max_limit = consultarVelocidadPaquete(nombre=paquete)
            if max_limit:
                ok = crearQueueSimple(nombre, direccion_ip, max_limit=max_limit[0], credenciales=credenciales, parent=parent, tiempo="20s/20s")
                if ok:
                    flash(f"Queue Simple integrada para {nombre} con su rafaga", "success")
                    return redirect(url_for("lista_clientes"))
                else:
                    flash("No logramos crear el Queue hija", "danger")
            else:
                flash("No tenemos velocidad en el paquete", "danger")
                return redirect(url_for("lista_clientes"))
        else:
            flash("No encontramos las credenciales del mcirotik", "danger")
            return redirect(url_for("lista_clientes"))


def procesar_eliminar_queue_simple(id):
    if request.method == "POST":
        microtik = request.form.get("microtik")
        direccion_ip = request.form.get("direccionIp")
        print(f"Datos capturados {microtik} con {direccion_ip}")

        credenciales = consultarCredenciales(nombre=microtik)

        if credenciales:
            if  eliminarSimpleQueue(credenciales, direccion_ip):
                flash("Queue eliminado con exito", "success")
                eliminar_cliente_chido(id)
                return redirect(url_for("lista_clientes"))
            else:
                flash("No eliminamos el queue", "danger")
                return redirect(url_for("lista_clientes"))
            
        else:
            flash(f"No encontramos credenciales para el mcirotiks {microtik}", "danger")
            return redirect(url_for("lista_clientes"))