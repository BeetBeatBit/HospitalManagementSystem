from flask import Flask, render_template
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

if __name__ == "__main__":
    app.run(port=4000, host="0.0.0.0")