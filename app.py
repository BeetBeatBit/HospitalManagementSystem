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


@app.route('/verificar', methods=['GET', 'POST'])
def login2():
    if request.method == 'POST':
        # Recupera los datos ingresados por el usuario en el input
        email = request.form['email']
        password = request.form['contraseña']
        # Establecer la conexión a la base de datos
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Daniel98@",
            database="clinica"
        )
        # Crear una consulta SQL para seleccionar los valores de correo y contraseña desde la tabla de usuarios
        sql = "SELECT username, password FROM users WHERE username = %s AND password = %s"
        values = (email, password)
        
        # Ejecutar la consulta SQL y obtener los resultados
        cursor = db.cursor()
        cursor.execute(sql, values)
        result = cursor.fetchone()
        # Comparar los valores de correo y contraseña
        if result and result[0] == email and result[1] == password:
            # Credenciales válidas, redirigir al usuario a la página de inicio de sesión
            print("Si encontre")
            
            error = 'Credenciales válidas. Bienvenido.'
            return render_template('/login.html', error=error)
            
            #return redirect(url_for('inicio'))
        else:
            # Credenciales no válidas, mostrar un mensaje de error
            print("NO encontre")
            
            error = 'Credenciales no válidas. Intente de nuevo.'
            return render_template('/login.html', error=error)
    else:
        return render_template('/login.html', error=error)

if __name__ == "__main__":
    app.run(port=4000, host="0.0.0.0")