from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ssh_leases import obtener_leases_por_nombre, hacer_estatico
from decoradores import *
from d_consultas import *
from ssh_leases import obtener_leases_por_nombre, hacer_estatico
from decoradores import *
from d_consultas import *

mikrotik_bp = Blueprint("mikrotik_bp", __name__)


@mikrotik_bp.route("/ver_dhcp_leases", methods=["GET", "POST"])
@login_requerido
def ver_dhcp_leases():
    leases = []
    nombre_mikrotik = None
    microtiks = consultar_lista_microtiks()

    if request.method == "POST":
        nombre_mikrotik = request.form.get("mikrotik_nombre")
        leases = obtener_leases_por_nombre(nombre_mikrotik)
        print(f"Leases recibidos de {nombre_mikrotik}:", leases)

    return render_template("Mdhcp_leases.html", microtiks=microtiks, leases=leases, nombre_mikrotik=nombre_mikrotik)



@mikrotik_bp.route("/make_static", methods=["POST"])
@login_requerido
def make_static():
    ip = request.form.get("ip")
    nombre = request.form.get("mikrotik")
    if hacer_estatico(nombre, ip):  # función que ejecuta comando en MikroTik
        flash("✔ Lease convertido a estático", "success")
    else:
        flash("❌ No se pudo hacer estático", "danger")
    return redirect(url_for("ver_dhcp_leases"))


@mikrotik_bp.route("/registrar_sistema", methods=["POST"])
@login_requerido
def registrar_sistema():
    ip = request.form.get("ip")
    mac = request.form.get("mac")
    hostname = request.form.get("hostname")
    # Aquí puedes registrar en la tabla `clientes` o `equipos`
    flash(f"✔ Dispositivo {hostname} registrado con IP {ip}", "success")
    return redirect(url_for("ver_dhcp_leases"))
