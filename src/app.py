from functools import wraps
from flask import Flask, abort, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from config import config
from flask_mysqldb import MySQL
from models.ModelUsers import ModelUsers
from models.entities.users import User


app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

@app.route("/")
def index():
    return redirect("login")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User(0, request.form['username'], request.form['password'],0)
        logged_user = ModelUsers.login(db, user)
        if logged_user != None:
            login_user(logged_user)
            if logged_user.usertype == 1:
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("home"))
        else:
            flash("Acceso rechazado...")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
# Verificar si el usuario está autenticado y es un administrador
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403) # Acceso prohibido
        return func(*args, **kwargs)
    return decorated_view

@app.route("/admin")
@login_required
@admin_required
def admin():
    return render_template("admin.html")

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()