# Practica5_Login_parte_3
Andre Alexander Hidrogo Rocha 27/11/2023 Tercera parte del login por medio de Flask

### Instalación de flask_login
Para iniciar, se debe instalar el paquete flask_login en el entorno virtual utilizando el siguiente comando:

``` bash
pip install FLASK_LOGIN
```

### Implementación en el código
En el archivo app.py, se realiza la importación de las clases y funciones necesarias desde el paquete flask_login. Estas incluyen LoginManager, login_user, logout_user, y login_required.

``` python
from flask_login import LoginManager, login_user, logout_user, login_required
```

LoginManager: Es la clase para configurar la autenticación y administrar las sesiones de usuario en Flask.
login_user: Función para iniciar sesión de un usuario en el sistema luego de proporcionar credenciales válidas.
logout_user: Utilizada para cerrar la sesión de un usuario en la aplicación.
login_required: Decorador para rutas o vistas que requieren que el usuario esté autenticado para acceder.

### Configuración de LoginManager
Se crea una instancia de LoginManager asociada a la aplicación Flask:

``` python
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager(app)
```

despues debemos verificar que las credenciales del usuario son válidas, se establece la sesión utilizando login_user():

``` python
if logged_user is not None:
    login_user(logged_user)
```
Cargador de usuario (user_loader)
Se define un user_loader para cargar los datos del usuario que ha iniciado sesión:

``` python
Copy code
@login_manager.user_loader
def load_user(user_id):
    return ModelUsers.get_by_id(db, user_id)
```

Se agrega un atributo is_active a la clase User para controlar la sesión. Para lograrlo, se hace que la clase User herede de UserMixin del paquete flask_login:

 ``` python
from flask_login import UserMixin
class User(UserMixin):
 ```

### Uso en las plantillas HTML
Para mostrar los datos del usuario en home.html y admin.html: 

``` html
<h1>{{ current_user.fullname }}</h1>
```

Para el logout, se crea la ruta /logout y se utiliza el método logout_user(). También se agrega un enlace en las plantillas admin.html y home.html para realizar el logout.

``` python
@app.route("/logout")
@login_required
def logout():
logout_user()
return redirect(url_for("login"))
```

Por ultimo se implementa admin_required para permitir el acceso solo a usuarios autenticados y con privilegios de administrador.
