from flask import Flask, render_template, redirect, session, request, url_for, flash
from d_consultas import consutlarPaquete, consutlarAntena, consultarServicio, consultarMicrotik, consultarClientes, consultarCredenciales, consultarMicrotikTodo, consultarVelocidadPaquete, consultarPaquetes, consultarTodoServicios
from d_insert import insertarCliente, insertMicrotik, insertarPauqete, insertarServicio
from d_eliminar import eliminar_cliente_chido, eliminarMicrotik, eliminarPaquete, eliminarServicio
from d_update import actualizarCliete, actualizarMicrotik, acualizarPaquete, actualizarServicio
from ssh_pcq import bloquear_cliente_address_list, desbloqueo_mantecoso, get_interfaces, creacionAddressList, crearQueueParent, crearQueueSimple, eliminarSimpleQueue, aplicarFirewall
from d_login import login
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

#AQUI ES A DONDE NOS VAMOS CUANDO SE ENTRA AL SERVIDOR
@app.route("/")
def raiz():
    return render_template("login.html")

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        ok = login(username, password)
        
        if ok:
            print(ok)
            return redirect(url_for("lista_clientes"))
        else:
            return render_template("error.html"), 500
        

#------------------------------------------------RUTA DE LOS CLIENTES CRUD----------------------------------
@app.route("/crear_cliente", methods=["POST"])
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
        username = request.form.get("usernameNuevo")
        password = request.form.get("passwordNuevo")
        ip = request.form.get("ipNuevo")
        port = request.form.get("portNuevo")

        ok = insertMicrotik(nombre, ip, username, password, port)
        if ok:
            flash("Microtik registrado con exito", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("No se registro el microtik", "danger")
            return redirect(url_for("lista_microtiks"))


    return redirect(url_for("lista_microtiks"))

@app.route("/lista_microtiks")
def lista_microtiks():
    micro = consultarMicrotikTodo()
    print(micro)
    return render_template("microtik.html", microtiks=micro)

@app.route("/editar_mikrotik<int:id>", methods=["POST"])
def editar_mikrotik(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        username = request.form.get("username")
        password = request.form.get("password")
        ip = request.form.get("ip")
        port = request.form.get("port")

        ok = actualizarMicrotik(nombre, ip, username, password, port, id)
        if ok:
            flash("Microtik actualizado exitosamente", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("Microtik no actualizado", "danger")
            return redirect(url_for("lista_microtiks"))


    return redirect(url_for("lista_microtiks"))

@app.route("/eliminar_mikrotik<int:id>", methods=["POST"])
def eliminar_mikrotik(id):
    ok = eliminarMicrotik(id)

    if ok:
        flash("Microtik eliminado de manera exitosa", "success")
        return redirect(url_for("lista_microtiks"))
    else:
        flash("No se logro eliminar el microtik", "danger")
        return redirect(url_for("lista_microtiks"))

@app.route("/consultar_interfaces")
def consultar_interfaces():
    # Obtiene los parámetros de la consulta
    mikrotik_id = request.args.get('id')
    username = request.args.get('username')
    password = request.args.get('password')
    ip = request.args.get('ip')
    port = request.args.get('port')
    
    # Llama a la función para obtener las interfaces
    interfaces = get_interfaces(ip, port, username, password)
    
    # Devuelve un fragmento de HTML (por ejemplo, un select) con las interfaces
    return render_template("interfaces_partial.html", interfaces=interfaces)

@app.route("/configuracion_pcq", methods=["POST"])
def configuracion_pcq():
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
        

@app.route("/crear_queue_parent", methods=["POST"])
def crear_queue_parent():

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

@app.route("/cargar_queue", methods=["POST"])
def cargar_queue():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        direccion_ip = request.form.get("direccionIp")
        paquete = request.form.get("paquete")
        microtik = request.form.get("microtik")
        parent = request.form.get("queueParent")

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

 
@app.route("/eliminar_queue_simple", methods=["POST"])
def eliminar_queue_simple():
    if request.method == "POST":
        microtik = request.form.get("microtik")
        direccion_ip = request.form.get("direccionIp")
        print(f"Datos capturados {microtik} con {direccion_ip}")

        credenciales = consultarCredenciales(nombre=microtik)

        if credenciales:
            delete = eliminarSimpleQueue(credenciales, direccion_ip)
            if delete:
                flash("Queue eliminado con exito", "success")
                return redirect(url_for("lista_clientes"))
            else:
                flash("No eliminar el queue", "danger")
                return redirect(url_for("lista_clientes"))
            
        else:
            flash(f"No encontramos credenciales para el mcirotiks {microtik}", "danger")
            return redirect(url_for("lista_clientes"))

@app.route("/aplicar_reglas", methods=["POST"])
def aplicar_reglas():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("direccion_ip")
        port = request.form.get("port")
        
        ok = aplicarFirewall(host, port, username, password)
        if ok:
            flash("Reglas aplicadas con exito", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("No logramos aplicar las reglas", "danger")
            return redirect(url_for("lista_microtiks"))

#------------------------------------------------RUTA DE LOS MICROTIKS CRUD----------------------------------



#------------------------------------------------RUTA DE LOS PAQUETES CRUD----------------------------------
@app.route('/lista_paquetes')
def lista_paquetes():
    paquetaxo = consultarPaquetes()
    return render_template('paquetes_internet.html', paquetes=paquetaxo)

@app.route('/crear_paquete', methods=['POST'])
def crear_paquete():
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


@app.route('/editar_paquete/<int:id>', methods=['POST'])
def editar_paquete(id):
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
        

@app.route('/eliminar_paquete/<int:id>')
def eliminar_paquete(id):
    ok = eliminarPaquete(id)
    print(id)
    if ok:
        flash("Paquete eliminado de manera exitosa", "success")
        return redirect(url_for("lista_paquetes"))
    else:
        flash("No se elimino el paquete", "danger")
        return redirect(url_for("lista_paquetes"))

#------------------------------------------------RUTA DE LOS PAQUETES CRUD----------------------------------


#------------------------------------------------RUTA DE LOS SERVICIOS CRUD----------------------------------
@app.route("/creacion_servicio", methods=["POST"])
def creacion_servicio():
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
        

@app.route("/lista_servicios")
def lista_servicios():
    servicio = consultarTodoServicios()
    return render_template("servicios.html", servicios=servicio)

@app.route("/editar_servicio/<int:id>", methods=["POST"])
def editar_servicio(id):
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
    

@app.route("/eliminar_servicio/<int:id>")
def eliminar_servicio(id):
    ok = eliminarServicio(id)    
    if ok:
        flash("Servicio eliminado", "success")
        return redirect(url_for("lista_servicios"))
    else:
        flash("No eliminamos el servicio", "danger")
        return redirect(url_for("lista_servicios"))
    
#------------------------------------------------RUTA DE LOS SERVICIOS CRUD----------------------------------
app.run(debug=True)
