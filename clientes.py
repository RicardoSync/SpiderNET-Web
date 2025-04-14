from d_insert import *
from d_consultas import *
from d_update import *
from d_eliminar import *
from flask import *

def procesar_cliente_creacion():
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
        
def procesar_lista_clientes():
    try:
        page = int(request.args.get("page", 1))
        por_pagina = int(request.args.get("limit", 10))
        offset = (page - 1) * por_pagina

        cn = conexion()
        cursor = cn.cursor()

        # Total de registros para calcular cuántas páginas hay
        cursor.execute("SELECT COUNT(*) FROM clientes")
        total_clientes = cursor.fetchone()[0]

        # Consulta con JOINs y sin modificar el formato de fecha
        sql = """
            SELECT 
                c.id,
                c.nombre,
                p.nombre AS paquete,
                c.fecha_registro,
                c.ip_cliente,
                c.dia_corte,
                a.nombre AS antena_ap,
                sp.nombre AS servicio_plataforma,
                cm.nombre AS microtik_nombre
            FROM clientes c
            LEFT JOIN paquetes p ON c.id_paquete = p.id
            LEFT JOIN credenciales_microtik cm ON c.id_microtik = cm.id
            LEFT JOIN antenasap a ON c.id_antena_ap = a.idantenasAp
            LEFT JOIN serviciosplataforma sp ON c.id_servicio_plataforma = sp.idPlataformas
            ORDER BY c.id ASC
            LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (por_pagina, offset))
        clientes = cursor.fetchall()

        cursor.close()
        cn.close()

        total_paginas = (total_clientes + por_pagina - 1) // por_pagina

        return render_template(
            "lista_clientes.html",
            clientes=clientes,
            pagina=page,
            total_paginas=total_paginas,
            por_pagina=por_pagina,
            antens=consutlarAntena(),
            paquetes=consutlarPaquete(),
            servicios=consultarServicio(),
            microtiks=consultarMicrotik(),
            queues_colas=consultarQeue()
        )

    except Exception as e:
        print(f"❌ Error en paginación avanzada: {e}")
        return render_template("error.html"), 500

def procesar_edicion_del_cliente(id):
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

def procesar_elimiacion_del_cliente(id):
    if eliminar_cliente_chido(id):
        flash("Cliente eliminado con exito", "succes")
        return redirect(url_for("lista_clientes"))
    else:
        flash("El cliente no se elimino", "danger")
        return redirect(url_for("lista_clientes"))
