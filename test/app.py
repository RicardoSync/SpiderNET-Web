from flask import Flask, render_template, request, redirect, url_for, session
from d_consultas import consultarMicrotik, consultarCredenciales
from ssh_pcq import consultarClientesDHCP
import re

app = Flask(__name__)
app.secret_key = "zerocuatro04"  # Necesario para usar session


#===================================MICROTIK PCQ==================================
@app.route("/pcq")
def pcq():
    microtiks = consultarMicrotik()
    #obtenemos los datos si existen, caso contrario queda vacio
    clientes = session.get("dhcp_clientes", [])

    return render_template("pcq.html", nombres=microtiks, dhcp_clientes=clientes)



@app.route("/consultar_dhcp_leases", methods=["POST"])
def consultar_dhcp_leases():
    if request.method == "POST":
        nombre = request.form.get("lista_microtik")
        credenciales = consultarCredenciales(nombre)

        print(f"Credenciales obtenidas: {credenciales}")

        clientes = consultarClientesDHCP(credenciales)
        print(f"Clientes DHCP: {clientes}")

        if clientes:
            # Simulación de parseo de la salida de MikroTik
            clientes_lista = parsear_salida_dhcp(clientes)

            # Guardar en session antes de redirigir
            session["dhcp_clientes"] = clientes_lista

    return redirect(url_for("pcq"))




def parsear_salida_dhcp(salida):
    """
    Parsea la salida del comando SSH de MikroTik para obtener clientes DHCP correctamente formateados.
    """
    lineas = salida.strip().split("\n")
    clientes = []

    for linea in lineas:
        linea = linea.strip()

        # Ignorar encabezados y líneas no deseadas
        if linea.startswith("Columns:") or linea.startswith("#") or linea.startswith("ADDRESS"):
            continue  

        # Dividir la línea en columnas correctamente
        datos = re.split(r'\s{2,}', linea)  # Divide cuando hay 2 o más espacios seguidos

        if len(datos) >= 5:  # Asegurar que hay al menos 5 columnas
            clientes.append(datos[:5])  # Solo tomamos los primeros 5 elementos

    print(f"Clientes parseados correctamente: {clientes}")  # Ver si hay varios clientes
    return clientes

#===================================MICROTIK PCQ==================================





app.run(debug=True)