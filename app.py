from flask import Flask, render_template, request, redirect, url_for, flash
from bk_login import validacion_usuario
from bk_insert_elements import almacenarServicio
from bk_consultas import consultarServicios
from bk_delete import eliminarServicio
from bk_update import editarServicio

app = Flask(__name__)

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
            print("error")

    return render_template("login.html")


#ruta para el dashboard que estamos llamando 
@app.route("/dashboard")
def dashboard():
    return render_template("home.html")


#ruta de servicios html llamado desde html
@app.route("/servicios")
def servicios():
    serviciosAlmacenados = consultarServicios()
    return render_template("servicios.html", pkg=serviciosAlmacenados)


#------------------------------------------------CRUD DE LOS SERVICIOS----------------------------------
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
            return render_template("home.html")


@app.route("/eliminar_servicio/<int:id>", methods=["POST"])
def eliminar_servicio(id):
    print(id)
    ok = eliminarServicio(id)

    if ok:
        return redirect(url_for("servicios"))
    else:
        return render_template("home.html")

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
        return redirect(url_for("home")) #si es false te manda a login.html


#------------------------------------------------CRUD DE LOS SERVICIOS----------------------------------


app.run(debug=True)