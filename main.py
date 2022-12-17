from urllib import response
from flask import Flask, request, make_response, redirect, render_template, url_for

app = Flask(__name__)

obligaciones = ["Impuesto a la Renta", "Impuesto a las ventas",
 "Retención en la Fuente", "Impuesto de industria y comercio"]

@app.route("/")
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/inicio"))
    response.set_cookie("user_ip", user_ip)

    return response

@app.route("/inicio")
def inicio():
    user_ip = request.cookies.get("user_ip")
    context = {
        "user_ip" : user_ip,
        "obligaciones" : obligaciones
    }

    return render_template("inicio.html", **context)