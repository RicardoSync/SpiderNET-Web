from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *

def procesar_lista_paquetes():
    paquetaxo = consultarPaquetes()
    return render_template('paquetes_internet.html', paquetes=paquetaxo)


def procesar_creacion_paquete():
    nombre = request.form.get('nombre')
    velocidad = request.form.get('velocidad')
    precio = request.form.get('precio')

    print(f"Obtenidos {nombre} {velocidad} {precio}")
    ok = insertarPauqete(nombre, velocidad, precio)
    if ok:
        flash("Paquete registrado", "success")
        return redirect(url_for("lista_paquetes"))
    else:
        flash("No se pudo registrar", "danger")
        return redirect(url_for("lista_paquetes"))
    
def procesar_editar_paquete(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        velocidad = request.form.get("velocidad")
        precio = request.form.get("precio")

        ok = acualizarPaquete(nombre, velocidad, precio, id)
        if ok:
            flash("Paquete actualizado", "success")
            return redirect(url_for("lista_paquetes"))
        else:
            flash(f"No actualizar el paquete {nombre}", "danger")
            return redirect(url_for("lista_paquetes"))
        
def procesar_eliminar_paquete(id):
    ok = eliminarPaquete(id)
    print(id)
    if ok:
        flash("Paquete eliminado de manera exitosa", "success")
        return redirect(url_for("lista_paquetes"))
    else:
        flash("No se elimino el paquete", "danger")
        return redirect(url_for("lista_paquetes"))
