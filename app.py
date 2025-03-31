from flask import Flask, render_template, redirect, session, request, url_for, flash, send_file, jsonify
from d_consultas import *
from d_insert import *
from d_eliminar import *
from d_update import *
from ssh_pcq import *
from d_login import login
from d_contador import *
from monitor import obtener_trafico_mikrotik
from dhcp_leases import get_dhcp_leases
from bloqueos_bd import estado_bloqueado
from ssh_pppoe import *
from get_pools import *
from pppoe import *
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

@app.route('/dashboard')
def dashboard():
    total_clientes = contador_clientes()  # Llamada a la función
    total_equipos = contador_equipos()
    total_pagos = contador_pagos()
    total_microtiks = contador_mikrotik()
    return render_template("dashboard.html",
                        total_clientes=total_clientes,
                        total_equipos=total_equipos,
                        total_pagos=total_pagos,
                        total_microtiks=total_microtiks)

@app.route("/iniciar_sesion", methods=["POST"])
def iniciar_sesion():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        ok = login(username, password)
        if ok:
            print(ok)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")
        

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

        if insertarCliente(nombre, paquete, ip_cliente, dia_corte, antena_ap, servicio, microtik):
            flash("Cliente registrado con exito", "success")
            return redirect(url_for("lista_clientes"))
        else:
            flash("El cliente no se registro", "danger")            
            return redirect(url_for("lista_clientes"))
            
@app.route("/lista_clientes")
def lista_clientes():
    cliente = consultarClientes()
    antenas = consutlarAntena()
    paquetes = consutlarPaquete()
    return render_template("lista_clientes.html", clientes=cliente, antens=antenas, paquetes=paquetes, servicios=consultarServicio(),
                           microtiks=consultarMicrotik(), queues_colas=consultarQeue())

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
    if eliminar_cliente_chido(id):
        flash("Cliente eliminado con exito", "succes")
        return redirect(url_for("lista_clientes"))
    else:
        flash("El cliente no se elimino", "danger")
        return redirect(url_for("lista_clientes"))



@app.route('/bloquear_cliente_pcq/<int:id>', methods=["POST"])
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
    

@app.route("/desbloquear_cliente_pcq/<int:id>", methods=["POST"])
def desbloquear_cliente_pcq(id):
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

@app.route("/clientes_bloqueados")
def clientes_bloqueados():
    clientes = consultar_clientes_bloqueados()
    return render_template("bloqueados.html", clientes=clientes)
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
    return render_template("microtik.html", microtiks=micro, queues_colas=consultarQeue())

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


@app.route("/consultar_interfaces_chido")
def consultar_interfaces_chido():
    # Se obtiene el nombre del Mikrotik desde el parámetro 'mikrotik'
    mikrotik = request.args.get("mikrotik")
    credenciales = consultarCredenciales(nombre=mikrotik)
    if credenciales:
        username = credenciales[0]
        password = credenciales[1]
        ip = credenciales[2]
        port = credenciales[3]
    
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

 
@app.route("/eliminar_queue_simple/<int:id>", methods=["POST"])
def eliminar_queue_simple(id):
    if request.method == "POST":
        microtik = request.form.get("microtik")
        direccion_ip = request.form.get("direccionIp")
        print(f"Datos capturados {microtik} con {direccion_ip}")

        credenciales = consultarCredenciales(nombre=microtik)

        if credenciales:
            if  eliminarSimpleQueue(credenciales, direccion_ip):
                flash("Queue eliminado con exito", "success")
                eliminar_cliente(id)
                return redirect(url_for("lista_clientes"))
            else:
                flash("No eliminamos el queue", "danger")
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


@app.route('/reiniciar_mikrotik/<int:id>', methods=["POST"])
def reiniciar_mikrotik(id):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        host = request.form.get("ip")
        port = request.form.get("port")
        reicniar_mikrotik(username, password, host, port)
        
    return redirect(url_for("lista_microtiks"))

        

@app.route("/dios_ayudame")
def dios_ayudame():
    microtiks = consultarMicrotik()
    return render_template("monitor.html", microtiks=microtiks)

@app.route('/monitor_traffic', methods=["POST"])
def monitor_traffic():
    if request.method == "POST":
        mikrotik = request.form.get("lista_microtik")
        # Obtén la interfaz seleccionada del formulario
        interface = request.form.get("interface", "ether1")
        credenciales = consultarCredenciales(nombre=mikrotik)

        if credenciales:
            username = credenciales[0]
            password = credenciales[1]
            host = credenciales[2]
            port = credenciales[3]
            
            try:
                output = obtener_trafico_mikrotik(host, port, username, password, interface)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

            # Procesa la salida para convertirla en un diccionario:
            data = {}
            for line in output.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
    
    return jsonify(data)

@app.route("/consultar_ip_pools")
def consultar_ip_pools():
    # Obtiene los parámetros de la consulta
    mikrotik_id = request.args.get('id')
    username = request.args.get('username')
    password = request.args.get('password')
    host = request.args.get('host')
    port = request.args.get('port')
    print(f"Uusaiors obtenidos {username, password, host, port}")
    # Llama a la función para obtener las IP pools
    pools = get_pool_list_nuevo(host, port, username, password)
    print(f"Pool obtenidas en backend {pools}")
    
    # Devuelve un fragmento de HTML con el select de pools
    return render_template("ippools_partial.html", pools=pools)

@app.route("/crear_ppp_profile/<int:id>", methods=["POST"])
def crear_ppp_profile(id):
    # Se obtienen los datos enviados desde el modal
    username = request.form.get('username')
    password = request.form.get('password')
    host = request.form.get('host')
    port = request.form.get('port')
    ippool = request.form.get('ippool')
    ppp_profile = request.form.get('ppp_profile')
    max_limit = request.form.get('max_limit')
    queue_parent = request.form.get('queueParent')


    if creacion_profile(ppp_profile, ippool, max_limit, username, password, host, port, queue_parent):
        if insertar_profile_pppoe(nombre=ppp_profile, local_address=ippool,remote_address=ippool, address_list="Internet", limit=max_limit, id_mikrotik=id):
            flash("PPP Profile creado en MikroTik y almacenado en el sistema", "success")
            return redirect(url_for("lista_microtiks"))
        else:
            flash("PPP Profile no se creo en el sistema")
            return redirect(url_for("lista_microtiks"))
    else:
        flash("PPP Profile no se creo en el MikroTik", "success")
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

#=======================================ASIGNACION DE LOS EQUIPOS==============================
# Ruta para procesar la asignación del equipo
@app.route('/asignar_equipo/<int:id>', methods=['POST'])
def asignar_equipo(id):
    if request.method == "POST":
        nombre_equipo = request.form.get("nombre_equipo")
        tipo_equipo = request.form.get("tipo_equipo")
        marca_equipo = request.form.get("marca_equipo")
        modelo_equipo = request.form.get("modelo_equipo")
        estado_equipo = request.form.get("estado_equipo")
        
        ok = insertarEquipo(nombre_equipo, tipo_equipo, marca_equipo, modelo_equipo, estado_equipo, id)
        if ok:
            flash("Equipo asignado con exito", "success")
            return redirect(url_for("lista_clientes"))
        else:
            flash("No asignamos el equipo al cliente", "danger")
            return redirect(url_for("lista_clientes"))

@app.route("/consultar_equipos")
def consultar_equipos():
    dedos = consultarEquipos()
    return render_template("equipos.html", equipos=dedos)

@app.route("/editar_equipo/<int:id>", methods=["POST"])
def editar_equipo(id):
    if request.method == "POST":
        nombre = request.form.get("nombre")
        tipo = request.form.get("tipo_equipo")
        marca = request.form.get("marca")
        modelo = request.form.get("modelo")
        estado_equipo = request.form.get("estado_equipo")
        
        ok = actualizarEquipo(nombre, tipo, marca, modelo, estado_equipo, id)
        if ok:
            flash("El equipo se actualizo", "success")
            return redirect(url_for("consultar_equipos"))
        else:
            flash("No actualizamos el equipo", "danger")
            return redirect(url_for("consultar_equipos"))

@app.route("/eliminar_equipo/<int:id>")
def eliminar_equipo(id):
    ok = eliminarEquipo(id)
    if ok:
        flash("Equipo eliminado", "success")
        return redirect(url_for("consultar_equipos"))
    else:
        flash("Equipo no eliminado", "danger")
        return redirect(url_for("consultar_equipos"))
#=======================================ASIGNACION DE LOS EQUIPOS==============================

#=======================================FUNCION DE QUEUE PARENT==============================
@app.route("/creacion_queue_parent", methods=["POST"])
def creacion_queue_parent():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        segmento = request.form.get("segmento")
        max_limit = request.form.get("max_limit")
        mikrotik = request.form.get("lista_microtik")

        credenciales = consultarCredenciales(nombre=mikrotik)


        if credenciales:
            username = credenciales[0]
            password = credenciales[1]
            host = credenciales[2]
            port = credenciales[3]
            ok = crearQueueParent(nombre, segmento, max_limit, host, port, username, password, mikrotik)
            if ok:
                flash(f"Queue creado con exito en el mikroitk {mikrotik}", "success")
                return redirect(url_for("lista_queue"))
            else:
                flash("No logramos crear el Queue Parent", "danger")
                return redirect(url_for("lista_queue"))
        else:
            flash("No encontramos credenciales para ese mirotik", "danger")


@app.route("/lista_queue")
def lista_queue():
    queues_lista = consultar_queue()
    return render_template("queue_parent.html", queue_parents=queues_lista, microtiks=consultarMicrotik(), queues_colas=consultarQeue())

@app.route("/editar_queue_parent/<int:id>", methods=["POST"])
def editar_queue_parent(id):
    nombre = request.form.get("nombre")
    max_limint = request.form.get("max_limint")
    mikrotik = request.form.get("mirotik")
    segmento_red = request.form.get("segmento_red")
    credenciales = consultarCredenciales(mikrotik)

    if credenciales:
        username = credenciales[0]
        password = credenciales[1]
        host = credenciales[2]
        port = credenciales[3]
        print(username, password, host, port, segmento_red, nombre, max_limint)
        ok = actualizarQueue(username, password, host, port, segmento_red, nombre, max_limint)
        if ok:
            yes = actualiar_queue_bd(nombre, max_limint, mikrotik, id)
            if yes:
                flash("Queue actualizado en sistema y MikroTik", "success")
                return redirect(url_for("lista_queue"))
            else:
                flash("No actualimas la queue en sistema", "danger")
                return redirect(url_for("lista_queue"))
        else:
            flash("No actualizamos la Queue en MikroTik", "danger")
            return redirect(url_for("lista_queue"))
    else:
        flash("No encontramos credenciales para el MikroTik", "danger")


@app.route("/eliminar_queue_parent/<int:id>", methods=["POST"])
def eliminar_queue_parent(id):
    if request.method == "POST":
        microtik = request.form.get("mirotik")
        segmento_red = request.form.get("segmento")

        credenciales = consultarCredenciales(microtik)

        if not credenciales:
            flash("Sin credenciales, en ese mikrotik", "danger")
            return redirect(url_for("lista_queue"))

        username, password, host, port = credenciales

        if not eliminarQueueParent(username, password, host, port, segmento_red):
            flash("No eliminamos el QueueParent de Mikrotik", "danger")
            return redirect(url_for("lista_queue"))

        if not eliminarQueueBD(id):
            flash("Queue no se eliminó de la base de datos", "danger")
            return redirect(url_for("lista_queue"))

        flash("Queue eliminado del sistema", "success")
        return redirect(url_for("lista_queue"))

    return redirect(url_for("lista_queue"))        
#=======================================FUNCION DE QUEUE PARENT==============================



#=======================================FUNCION DE DHCP LEASES==============================

# Ruta para renderizar la página de perfiles PPPoE
@app.route("/pppoe_profiles")
def pppoe_profiles():
    # En este ejemplo, se asume que 'microtiks' y 'pools' se obtienen previamente.
    # Podrías obtener la lista de mikrotiks desde una BD.
    microtiks = consultarMicrotik()
    # Por defecto, para mostrar pools, se utiliza el primer mikrotik seleccionado.

    pools = get_ip_pools(microtiks[0])
    profiles = []
    return render_template("monitor_profiles.html", microtiks=microtiks, pools=pools, profiles=profiles)

# Ruta para crear un nuevo perfil PPPoE
@app.route("/crear_profile", methods=["POST"])
def crear_profile():
    lista_microtik = request.form.get("lista_microtik")
    nombre = request.form.get("nombre")
    pool = request.form.get("pool")
    pool_ranges = request.form.get("pool_ranges")
    max_limit = request.form.get("max_limit")
    
    creacion_profile(pool_ranges, pool, lista_microtik, nombre, max_limit)
    
    return redirect(url_for("pppoe_profiles"))

#=======================================FUNCION DE DHCP LEASES==============================


#=======================================FUNCION DE DHCP LEASES==============================
@app.route("/crear_ticket", methods=["POST"])
def crear_ticket():
    if request.method == "POST":
        cliente = request.form.get("lista_clientes")
        tipo = request.form.get("lista_categorias")
        descripcion = request.form.get("ticket")
        usuario = request.form.get("lista_usuarios")
        
        if insertar_ticket(cliente, tipo, descripcion, usuario):
            flash("Ticket generado de manera exitosa", "success")
            return redirect(url_for("fallas"))
        else:
            flash("Ocurrio un error, no generado", "danger")
            return redirect(url_for("fallas"))      
        
@app.route("/fallas")
def fallas():
    categoria = ["Soporte técnico",
                 "Facturación",
                 "Instalación",
                 "Otro"]
    
    return render_template("fallas.html", clientes=consularNombreClientes(), reportes=categoria,
                           usuarios=consultarUsuarios(), tickets=consultar_tickets())

@app.route("/editar_ticket/<int:id>", methods=["POST"])
def editar_ticket(id):
    if request.method == "POST":
        tipo = request.form.get("lista_categorias")
        descripcion = request.form.get("ticket")        
        usuario = request.form.get("lista_usuarios")
        if actualizar_ticket(tipo, descripcion, usuario, id):
            flash("Ticket actualizado con éxito", "success")
            return redirect(url_for("fallas"))
        else:
            flash("No actualizamos el ticket", "danger")
            return redirect(url_for("fallas"))
        
    return redirect(url_for("fallas"))

@app.route("/actualizar_finalizado/<int:id>", methods=["POST"])
def actualizar_finalizado(id):
    if actualizar_ticket_finalizado(id):
        flash("Ticket finalizado", "success")
        return redirect(url_for("fallas"))
    else:
        flash("Ocurrio un error en la finalizacion", "danger")
        return redirect(url_for("fallas"))
#================================""=======FUNCION DE DHCP LEASES==============================

app.run(debug=True)
