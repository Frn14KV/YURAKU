"""Tesis YURAKU de Christian Flores y Franklin Villavicencio 2019"""

"""
    librerias importadas
    forms: libreria propia de django para crear formularios
    Planta: importa el modelo llamado Planta.
    UserCreationForm: importa el formulario propio de django con datos basicos para crear los usuarios del sistema.
    UserChangeForm: importa el formilario propio de django con los campos para realizar el cambio de clave de la cuenta de los usuarios del sistema.
    User: importa el modelo llamado User que representa los usuarios del Sistema.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

"""
    Clase LoginForm
    Clase creada para realizar el formulario de  inicio de session de los usuarios.
        Parametros
        :param forms.ModelForm: Modelo basico propio de Django.
        Campos:
        username: campo de texto para ingresar el username.
        password: campo de texto en sifrado (con caracteres para no hacer transparente la clave) para que dijite la clave.
"""
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

"""
    Clase SignUpForm
    Clase creada para realizar el formulario de registro de los usuarios.
        Parametros
        :param UserCreationForm: Modelo basico propio de Django para crear usuarios..
        Campos:
        first_name = campo de texto para ingresar el primer nombre del usuario.
        last_name = campo de texto para ingresar el primer apellido del usuario.
        username: campo de texto para ingresar el username.
        email = campo de email para ingresar el correo electronico del usuario.
        password: campo de texto en sifrado (con caracteres para no hacer transparente la clave) para que dijite la clave.
        typeuser = campo de texto para ingresar el tipo de usuario (este no se registra en la base pero sirve para crear los permisos guardados en tras tablas).

    Subclase Meta
        Clase creada para pasarle los atributos del moledo User al
        nuevo Formulario.
            Atributos:
                model : moldelo que tengra el fomulario (en esta caso sera del modelo User)
                fields : campos que tendra el formulario (en este caso sera del modelo User)
"""
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=1500)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    typeuser = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'typeuser')

"""
    Clase Edit
    Clase creada para crear el formulario con el campo para editar el tipo de usuario que tiene la cuenta.
        Parametros
        :param UserCreationForm: Modelo basico propio de Django.
        Campos:
        typeuser = campo de texto para ingresar el tipo de usuario (este no se registra en la base pero sirve para crear los permisos guardados en tras tablas.).
"""
class Edit(UserCreationForm):
    typeuser = forms.CharField(max_length=20)


"""
    Clase EditProfileForm
    Clase creada para asignarle al nuevo formulario los campos para editar los datos de la cuenta del usuario.
    
        Subclase Meta
        Clase creada para pasarle los atributos del moledo User al
        nuevo Formulario.
            Atributos:
                model : moldelo que tengra el fomulario (en esta caso sera del modelo User)
                fields : campos que tendra el formulario (en este caso sera del modelo User)
"""
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        # exclude =('password1','typeuser')
