from ipaddress import ip_address
import ipaddress

def generar_rango_ips(ip_base):
    try:
        ip = ip_address(ip_base)  # Convertir la IP en un objeto ip_address
        ip_inicio = ip + 1  # Primera IP en el rango
        ip_fin = ip + 253   # Última IP en el rango

        return f"{ip_inicio}-{ip_fin}"
    except ValueError:
        return "IP no válida"
    

def obtener_subred(ip):
    try:
        # Convertir la IP en un objeto de la librería ipaddress
        ip_obj = ipaddress.IPv4Address(ip)
        # Obtener la dirección base de la subred
        subred = ipaddress.IPv4Network(f"{ip}/24", strict=False).network_address
        return f"{subred}/24"
    except ValueError:
        return "IP no válida"