from conexion import conexion

def login(username, password):
    try:
        cn = conexion()
        if cn is None:
            conexion().reconnect()

        cursor = cn.cursor()
        cursor.execute("SELECT usuario, password, rol FROM usuarios WHERE usuario = %s", (username,))
        resultado = cursor.fetchone()
        
        cursor.close()
        cn.close()

        print(f"Login intentado: {username=} {password=}")
        print(f"Resultado en DB: {resultado=}")

        if resultado is not None:
            db_user, db_pass, db_rol = resultado
            if str(db_pass) == str(password):  # Comparación estricta
                print("✔ Contraseña correcta")
                return db_rol
            else:
                print("❌ Contraseña incorrecta")
                return False
        else:
            print("❌ Usuario no encontrado")
            return False

    except Exception as r:
        print(f"Error de sesión: {r}")
        return False
