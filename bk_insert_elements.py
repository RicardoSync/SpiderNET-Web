from conexion import conexion

#esta funciona la usamos para almacenar la informacion en base de datos
#ya que esta funcion recibe como parametros el nombre, descripcion, precio
def almacenarServicio(nombre, descripcion, precio):
    cn = conexion()
    if cn is None:
        conexion().reconnect()
    
    try:
        cursor = cn.cursor()
        sql = "INSERT INTO serviciosplataforma (nombre, descripcion, precio) VALUES (%s,%s,%s)"
        valores = (nombre, descripcion, precio)

        cursor.execute(sql, valores)

        """Si los datos se almacenan devuelve el valor true
        caso contrarop imprime el error en consola y devuelve false
        """
        cn.commit()
        cursor.close()
        cn.close()

        return True
    
    except Exception as r:
        print(r)
        return False