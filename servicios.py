from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *


def procesar_creacion_servicio():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        
        ok = insertarServicio(nombre, descripcion, precio)
        if ok:
            flash("Servicio registrado", "success")
            return redirect(url_for("lista_servicios"))
        else:
            flash("No insertarmos el servicio", "danger")
            return redirect(url_for("lista_servicios"))
        
def procesar_lista_servicios():
    servicio = consultarTodoServicios()
    return render_template("servicios.html", servicios=servicio)

def procesar_edicion_servicios(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        precio = request.form.get("precio")
        
        ok = actualizarServicio(nombre, descripcion, precio, id)
        if ok:
            flash("Servicio actualizado", "success")
            return redirect(url_for("lista_servicios"))
        else:
            flash("Servicio no actualizado", "danger")
            return redirect(url_for("lista_servicios"))
    
def procesar_eliminar_servicio(id):
    ok = eliminarServicio(id)    
    if ok:
        flash("Servicio eliminado", "success")
        return redirect(url_for("lista_servicios"))
    else:
        flash("No eliminamos el servicio", "danger")
        return redirect(url_for("lista_servicios"))
    