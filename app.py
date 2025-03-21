from flask import Flask, render_template, request, redirect, url_for, flash
from bk_login import validacion_usuario
from bk_insert_elements import almacenarServicio, almacenarPaquetes, almacenarAntenas
from bk_consultas import consultarServicios, consultarPaquetes, consultarAntenas
from bk_delete import eliminarServicio, eliminarPaquete, eliminarAntena
from bk_update import editarServicio, editarPaquete, editarAntena

app = Flask(__name__)

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

#------------------------------------------------INICIO DEL SISTEMA----------------------------------
#ruta raiz a donde se dirigue el usuario al entrar
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        username = request.form.get("username") #obtenemos la informacion de los campos
        password = request.form.get("password")

        rol = validacion_usuario(username, password) #hacemos la comprobacion
        if rol:
            return redirect(url_for("dashboard"))
        else:
            return render_template("error.html"), 500

    return render_template("login.html")


#ruta para el dashboard que estamos llamando 
@app.route("/dashboard")
def dashboard():
    return render_template("home.html")
#------------------------------------------------INICIO DEL SISTEMA----------------------------------



#------------------------------------------------CRUD DE LOS SERVICIOS----------------------------------
#ruta de servicios html llamado desde html
@app.route("/servicios")
def servicios():
    serviciosAlmacenados = consultarServicios()
    return render_template("servicios.html", pkg=serviciosAlmacenados)


#ruta para poder obtener los datos con get, y almacenarlos
@app.route("/almacenar", methods=["POST"])
def almacenar_servicios():
    if request.method == "POST":
        nombreServicio = request.form.get("nombre")
        descripcionServicio = request.form.get("descripcion")
        precioServicio = request.form.get("precio")

        ok = almacenarServicio(nombreServicio, descripcionServicio, precioServicio)

        if ok:
            return redirect(url_for("servicios"))
        else:
            return render_template("error.html"), 500


@app.route("/eliminar_servicio/<int:id>", methods=["POST"])
def eliminar_servicio(id):
    print(id)
    ok = eliminarServicio(id)

    if ok:
        return redirect(url_for("servicios"))
    else:
        return render_template("error.html"), 500

@app.route("/editar_servicio/<int:id>", methods=["POST"])
def editar_servicio(id):
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]

    ok = editarServicio(nombre, descripcion, precio, id)

    print(nombre, descripcion, precio, id)
    if ok:
        return redirect(url_for("servicios"))  # si es true recarga la pagina
    else:
        return render_template("error.html"), 500
#------------------------------------------------CRUD DE LOS SERVICIOS----------------------------------



#------------------------------------------------CRUD DE LOS PAQUETES----------------------------------
@app.route("/paquetes")
def paquetes():
    paqueteAlma = consultarPaquetes()
    return render_template("paquetes.html", paquetesAlmace=paqueteAlma)

#ruta para obtener los datos con POST y almacenarlos
@app.route("/almacenar_paquete", methods=["POST"])
def almacenar_paquete():
    if request.method == "POST":
        nombrePaquete = request.form.get("nombre")
        velocidadPaqute = request.form.get("velocidad")
        precioPaquete = request.form.get("precio")

        ok = almacenarPaquetes(nombrePaquete, velocidadPaqute, precioPaquete)
        if ok:
            return redirect(url_for("paquetes"))
        else:
            return render_template("error.html"), 500

@app.route("/editar_paquete/<int:id>", methods=["POST"])
def editar_paquete(id):
    nombrePaquete = request.form.get("nombre")
    velocidadPaquete = request.form.get("velocidad")
    precioPaquete = request.form.get("precio")

    ok = editarPaquete(nombrePaquete, velocidadPaquete, precioPaquete, id)
    if ok:
        return redirect(url_for("paquetes"))
    else:
        return render_template("error.html"), 500


@app.route("/eliminar_paquete/<int:id>", methods=["POST"])
def eliminar_paquete(id):
    ok = eliminarPaquete(id)

    if ok:
        return redirect(url_for("paquetes"))
    else:
        return render_template("error.html"), 500
#------------------------------------------------CRUD DE LOS PAQUETES----------------------------------

#------------------------------------------------CRUD DE ANTENAS----------------------------------
@app.route("/antenas")
def antenas():
    anteAlma = consultarAntenas()
    return render_template("antenas.html", antenassAlmace=anteAlma)

@app.route("/almacenar_antena", methods=["POST"])
def almacenar_antena():
    if request.method == "POST":
        nombreAntena = request.form.get("nombre")
        modeloAntena = request.form.get("modelo")
        usuarioAtena = request.form.get("usuario")
        passwordAntena = request.form.get("password")
        ipAntena = request.form.get("direccionIp")

        ok = almacenarAntenas(nombreAntena, modeloAntena, usuarioAtena, passwordAntena, ipAntena)
        if ok:
            return redirect(url_for("antenas"))
        else:
            return render_template("error.html"), 500
        

@app.route("/editar_antena/<int:id>", methods=["POST"])
def editar_antena(id):
    nombre = request.form.get("nombre")
    modelo = request.form.get("modelo")
    usuario = request.form.get("usuario")
    password = request.form.get("password")
    ip = request.form.get("direccionIp")

    ok = editarAntena(nombre, modelo, usuario, password, ip, id)

    if ok:
        return redirect(url_for("antenas"))
    else:
        return render_template("error.html"), 500
    
@app.route("/eliminar_antena<int:id>", methods=["POST"])
def eliminar_antena(id):
    ok = eliminarAntena(id)
    if ok:
        return redirect(url_for("antenas"))
    else:
        return render_template("error.html"), 500

#------------------------------------------------CRUD DE ANTENAS----------------------------------

app.run(debug=True)