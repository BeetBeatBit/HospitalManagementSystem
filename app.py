from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/especialidades.html")
def espec():
    return render_template("especialidades.html")

@app.route("/servicios.html")
def serv():
    return render_template("servicios.html")

@app.route("/quienesSomos.html")
def quiens():
    return render_template("quienesSomos.html")

@app.route("/contactanos.html")
def contact():
    return render_template("contactanos.html")

@app.route("/login.html")
def login():
    return render_template("/login.html")

@app.route("/index.html")
def indexR():
    return render_template("index.html")

@app.route("/registro.html")
def registro():
    return render_template("registro.html")

@app.route('/registerBD', methods=['GET', 'POST'])
def registerBD():
    if request.method == 'POST':
        # Recupera los datos ingresados por el usuario en el input
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Establecer la conexión a la base de datos
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Daniel98@",
            database="clinica_lolsito"
        )

        # Validar si el correo electrónico del usuario ya existe en la base de datos
        cursor = db.cursor()
        query = "SELECT email FROM users WHERE email=%s"
        cursor.execute(query, (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # El correo electrónico ya está registrado en la base de datos, mostrar mensaje de error al usuario
            reg_error_msg = "El correo electrónico ya está registrado. Por favor, inicia sesión."
            return render_template('registro.html', reg_error_msg=reg_error_msg)
        else:
            # Insertar usuario nuevo dentro de la tabla users
            sql = "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s);"
            values = (fullname, email, password)

            # Ejecutar la consulta SQL y obtener los resultados
            cursor.execute(sql, values)

            if cursor.rowcount > 0:
                db.commit()  # confirmar los cambios en la base de datos
                # Registro exitoso, mostrar mensaje de éxito al usuario
                reg_success_msg = "Registro exitoso. ¡Ahora Inicia sesión!"
                return render_template('registro.html', reg_success_msg=reg_success_msg)
            else:
                # Error al registrar usuario, mostrar mensaje de error al usuario
                reg_error_msg = "No se pudo completar el registro. Intente de nuevo."
                return render_template('registro.html', reg_error_msg=reg_error_msg)
    else:
        errorPOST = "Error POST"
        return render_template('/login.html', error_msg=errorPOST)


@app.route('/loginBD', methods=['GET', 'POST'])
def loginBD():
    if request.method == 'POST':
        # Recupera los datos ingresados por el usuario en el input
        email = request.form['email']
        password = request.form['password']
        # Establecer la conexión a la base de datos
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Daniel98@",
            database="clinica_lolsito"
        )
        # Crear una consulta SQL para seleccionar los valores de correo y contraseña desde la tabla de usuarios
        sql = "SELECT email, password FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        
        # Ejecutar la consulta SQL y obtener los resultados
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()

        # Comparar los valores de correo y contraseña
        if result and result[0] == email and result[1] == password:
            # Credenciales válidas, redirigir al usuario a la página de inicio de sesión

            #login_success_msg = 'Credenciales válidas. Bienvenido.'
            #return render_template('/login.html', login_success_msg=login_success_msg)

            login_success_name = email
            return render_template('/index.html', login_success_name=login_success_name)
            #return redirect(url_for('inicio'))
        else:
            # Credenciales no válidas, mostrar un mensaje de error
            login_error_msg = 'Credenciales no válidas. Intente de nuevo.'
            return render_template('/login.html', login_error_msg=login_error_msg)
    else:
        errorPOST = "Error POST"
        return render_template('/login.html', error=errorPOST)

if __name__ == "__main__":
    app.run(debug = True, port=4000, host="0.0.0.0")