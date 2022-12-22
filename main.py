from urllib import response
from flask import Flask, request, make_response, redirect, render_template, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "SUPER SECRETO"

class LoginForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Enviar")


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)

@app.errorhandler(500)
def not_server(error):
    return render_template("500.html", error=error)

@app.route("/")
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("/inicio"))
    session["user_ip"] = user_ip

    return response

@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    user_ip = session.get("user_ip")
    login_form = LoginForm()
    username = session.get("username")

    context = {
        "user_ip" : user_ip,
        "login_form" : login_form,
        "username" : username
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session["username"] = username

        flash("Ingreso exitoso!")

        return redirect(url_for("contribuyentes"))

    return render_template("inicio.html", **context)

@app.route("/contribuyentes", methods=["GET", "POST"])
def contribuyentes():
    username = inicio.username
    contribuyentes = 1000
    return render_template("contribuyentes.html", contribuyentes=contribuyentes)

@app.route("/inicio", methods=["GET", "POST"])
def closesession():
    session.clear()

    return render_template("inicio.html")