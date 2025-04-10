from flask import *
from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *



def procesar_registro_pago(id):
    if request.method == "POST":
        nombre = request.form["nombre"]
        paquete = request.form["paquete_cliente"]
        ip = request.form["direccion_ip"]
        mikrotik = request.form["mikrotik"]
        
        print(f"Nombre: {nombre}")
        print(f"Paquete: {paquete}")
        print(f"IP: {ip}")
        print(f"Mikrotik: {mikrotik}")
        
        return redirect(url_for("lista_clientes"))
    
    """Al registrar el pago, en mikrotik se debe eliminar de addres list solo si existe.
        Por otro lado se debe almanera el pago en base de datos con su informacion
        """