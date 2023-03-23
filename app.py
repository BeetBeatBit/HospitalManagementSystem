from flask import Flask, render_template, redirect, url_for, request, session, send_file
from functools import wraps
from reportlab.pdfgen import canvas
import database as db


app = Flask(__name__)
app.secret_key = 'my_secret_key'

# Funcion decoradora
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

# Funcion para cerrar sesion
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template("/index.html")


#Funciones que Renderizan
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def indexR():
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

@app.route("/registro.html")
def registro():
    return render_template("registro.html")

@app.route("/login.html")
def login():
    return render_template("/login.html")



#Funciones para Logear y Registrar
@app.route('/registerBD', methods=['GET', 'POST'])
def registerBD():
    if request.method == 'POST':
        # Recupera los datos ingresados por el usuario en el input
        fullname = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Validar si el correo electrónico del usuario ya existe en la base de datos
        cursor = db.database.cursor()
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
                db.database.commit()  # confirmar los cambios en la base de datos
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
       
        # Crear una consulta SQL para seleccionar los valores de correo y contraseña desde la tabla de usuarios
        sql = "SELECT email, password FROM users WHERE email = %s AND password = %s"
        values = (email, password)
        
        # Ejecutar la consulta SQL y obtener los resultados
        cursor = db.database.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()

        # Comparar los valores de correo y contraseña
        if result and result[0] == email and result[1] == password:
            # si el usuario es válido, establecer una variable de sesión y redirigirlo a la página principal
            session['logged_in'] = True
            session['user_email'] = email

            return render_template('/index.html', email=email, logged_in=session['logged_in'])
        else:
            # Credenciales no válidas, mostrar un mensaje de error
            login_error_msg = 'Credenciales no válidas. Intente de nuevo.'
            return render_template('/login.html', login_error_msg=login_error_msg)
    else:
        errorPOST = "Error POST"
        return render_template('/login.html', error=errorPOST)



#Rutas del Registro de Pacientes
@app.route('/pacientes.html')
@login_required
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM pacientes")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('pacientes.html', data=insertObject)
    
@app.route('/user', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    apellidoPat = request.form['apellidoPat']
    apellidoMat = request.form['apellidoMat']
    ciudad = request.form['ciudad']
    correo = request.form['correo']
    telefono = request.form['telefono']
    edad = request.form['edad']
    tipoSangre = request.form['tipoSangre']
    peso = request.form['peso']
    estatura = request.form['estatura']

    if nombre and apellidoPat and apellidoMat and ciudad and correo and telefono and edad and tipoSangre and peso and estatura:
        cursor = db.database.cursor()
        sql = "INSERT INTO pacientes (nombre, apellidoPat, apellidoMat, ciudad, correo, telefono, edad, tipoSangre, peso, estatura) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (nombre, apellidoPat, apellidoMat, ciudad, correo, telefono, edad, tipoSangre, peso, estatura)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM pacientes WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    apellidoPat = request.form['apellidoPat']
    apellidoMat = request.form['apellidoMat']
    ciudad = request.form['ciudad']
    correo = request.form['correo']
    telefono = request.form['telefono']
    edad = request.form['edad']
    tipoSangre = request.form['tipoSangre']
    peso = request.form['peso']
    estatura = request.form['estatura']

    if nombre and apellidoPat and apellidoMat and ciudad and correo and telefono and edad and tipoSangre and peso and estatura:
        cursor = db.database.cursor()
        sql = "UPDATE pacientes SET nombre = %s, apellidoPat = %s, apellidoMat = %s, ciudad = %s, correo = %s, telefono = %s, edad = %s, tipoSangre = %s, peso = %s, estatura = %s WHERE id = %s"
        data = (nombre, apellidoPat, apellidoMat, ciudad, correo, telefono, edad, tipoSangre, peso, estatura, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/pdf/<string:id>')
def generar_pdf(id):
    cursor = db.database.cursor()
    sql = "SELECT * FROM pacientes WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    paciente = cursor.fetchone()
    
    # Crear el PDF
    nombre_pdf = f"ID_{paciente[0]}_{paciente[2]}_{paciente[3]}_{paciente[1]}.pdf"
    c = canvas.Canvas(nombre_pdf)

    # Encabezado con logo y nombre de la clínica
    c.drawImage("static/images/logo.png", 40, 750, 50, 50)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(250, 770, "Clinica Lolsito")

    # Información del paciente
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"ID: {paciente[0]}")
    c.drawString(100, 680, f"Nombre: {paciente[1]}")
    c.drawString(100, 660, f"Apellido Paterno: {paciente[2]}")
    c.drawString(100, 640, f"Apellido Materno: {paciente[3]}")
    c.drawString(100, 620, f"Ciudad: {paciente[4]}")
    c.drawString(100, 600, f"Correo: {paciente[5]}")
    c.drawString(100, 580, f"Telefono: {paciente[6]}")
    c.drawString(100, 560, f"Edad: {paciente[7]}")
    c.drawString(100, 540, f"Tipo de Sangre: {paciente[8]}")
    c.drawString(100, 520, f"Peso: {paciente[9]}")
    c.drawString(100, 500, f"Estatura: {paciente[10]}")

    # Pie de página con dirección de la clínica
    c.setFont("Helvetica", 10)
    c.drawString(40, 50, "Av. Central Poniente Num# 51, Tuxtla Gutiérrez, Chiapas.")

    c.save()

    
    # Descargar el PDF
    path =  nombre_pdf
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug = True, port=4000, host="0.0.0.0")