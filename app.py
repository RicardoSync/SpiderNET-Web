from flask import Flask, render_template, redirect, session, request, url_for, flash
from d_consultas import consutlarPaquete, consutlarAntena, consultarServicio, consultarMicrotik, consultarClientes, consultarCredenciales, consultarMicrotikTodo
from d_insert import insertarCliente
from d_eliminar import eliminar_cliente_chido
from d_update import actualizarCliete
from ssh_pcq import bloquear_cliente_address_list, desbloqueo_mantecoso
app = Flask(__name__)
app.secret_key = 'zerocuatro04/2025'  # Necesario para usar flash
#------------------------------------------------RUTAS CUANDO OCURRE UN ERROR----------------------------------

# Error 404 (Página no encontrada)
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("error.html"), 404

# Error 500 (Error interno del servidor)
@app.errorhandler(500)
def error_interno(error):
    return render_template("error.html"), 500
#------------------------------------------------RUTAS CUANDO OCURRE UN ERROR----------------------------------



#------------------------------------------------RUTA DE LOS CLIENTES CRUD----------------------------------
@app.route("/crear_cliente", methods=["POST"]) #sirve para obtener al cliente y almacenarlo
def crear_cliente():
    if request.method == "POST":
        nombre = request.form.get("nombreNuevo")
        paquete = request.form.get("lsita_paquetes")
        ip_cliente = request.form.get("direccionip")
        dia_corte = request.form.get("dia_corte")
        antena_ap = request.form.get("lista_perrona_de_las_antenas_dios_mio")
        servicio = request.form.get("servicios_disponibles_chidotes")
        microtik = request.form.get("lista_microtik")

        ok = insertarCliente(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik)
        print(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik)
        if ok:
            return redirect(url_for("lista_clientes"))
        else:
            return render_template("error.html"), 500

@app.route("/lista_clientes")
def lista_clientes():
    cliente = consultarClientes()
    antenas = consutlarAntena()
    paquetes = consutlarPaquete()
    return render_template("lista_clientes.html", clientes=cliente, antens=antenas, paquetes=paquetes, servicios=consultarServicio(), microtiks=consultarMicrotik())

@app.route("/eidtar_cliente<int:id>", methods=["POST"])
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


@app.route("/eliminar_cliente<int:id>", methods=["POST"])
def eliminar_cliente(id):
    ok = eliminar_cliente_chido(id)    
    if ok:
        return redirect(url_for("lista_clientes"))
    else:
        return render_template("error.html"), 500


@app.route('/bloquear_cliente_pcq', methods=["POST"])
def bloquear_cliente_pcq():
    # Se obtienen los datos enviados desde el formulario del modal
    # Obtener valores individuales
    direccion_ip = request.form.get('direccion_addres_cliente')
    microtik = request.form.get('microtik')

    print(direccion_ip, microtik)
    
    # Se consultan las credenciales para el microtik indicado
    credenciales = consultarCredenciales(microtik)
    print(credenciales)
    if credenciales:
        # Ejecuta el comando de bloqueo
        ok = bloquear_cliente_address_list(credenciales, direccion_ip)
        if ok:
            flash("Cliente bloqueado", "success")  # Tipo success para éxito
        else:
            flash("Tenemos problemas con el bloqueo", "danger")  # Tipo danger para error
    else:
        flash(f"No tenemos credenciales para ese MikroTik: {microtik}", "warning")  # Tipo warning para advertencia
    
    return redirect(url_for("lista_clientes"))
    

@app.route("/desbloquear_cliente_pcq", methods=["POST"])
def desbloquear_cliente_pcq():
     # Se obtienen los datos enviados desde el formulario del modal
    # Obtener valores individuales
    ip_cliente = request.form.get('direccion_addres_cliente')
    microtik = request.form.get('microtik')

    print(f"La ip del cliente es {ip_cliente} con microtik asociado {microtik} desde el model")    
    # Se consultan las credenciales para el microtik indicado
    credenciales = consultarCredenciales(microtik)
    if credenciales:
        # Ejecuta el comando de bloqueo
        ok = desbloqueo_mantecoso(credenciales, ip_cliente)
        if ok:
            flash("Cliente desbloqueado", "success")  # Tipo success para éxito
        else:
            flash("Tenemos problemas con el desbloqueo", "danger")  # Tipo danger para error
    else:
        flash(f"No tenemos credenciales para ese MikroTik: {microtik}", "warning")  # Tipo warning para advertencia
    
    return redirect(url_for("lista_clientes"))
#------------------------------------------------RUTA DE LOS CLIENTES CRUD----------------------------------

#------------------------------------------------RUTA DE LOS MICROTIKS CRUD----------------------------------
@app.route("/crear_mikrotik", methods=["POST"])
def crear_mikrotik():
    if request.method == "POST":
        nombre = request.form.get("nombreNuevo")
    return redirect(url_for("lista_microtiks"))

@app.route("/lista_microtiks")
def lista_microtiks():
    return render_template("microtik.html", microtiks=consultarMicrotikTodo())

@app.route("/editar_mikrotik<int:id>", methods=["POST"])
def editar_mikrotik(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")

    return redirect(url_for("lista_microtiks"))

@app.route("/eliminar_mikrotik<int:id>", methods=["POST"])
def eliminar_mikrotik(id):
    print("eliminado")

    return redirect(url_for("lista_microtiks"))

app.run(debug=True)