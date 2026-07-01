import random
import json
import os
from chatbot import pregunta
from config import config

def genPassword():
    password = random.randint(100000,999999)
    with open('password.txt', 'w') as archivo:
        archivo.write(str(password))
    return password

def chatbot(correo, isAdmin):
    if isAdmin:
        config(correo)
    else:
        pregunta(correo)

def login(isAdmin):
    if isAdmin:
        archivo = "admins.json" 
    else:
        archivo = "users.json"

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except FileNotFoundError:
        print("Aún no hay usuarios registrados.")
        return
    
    while True:
        correo = input("Ingrese su correo electrónico: ")
        if validarCorreo(correo):
            password = input("Ingrese su contraseña: ")
            usuarioEncontrado = None
            for u in usuarios:
                if u["correo"] == correo:
                    usuarioEncontrado = u
                    break
            if usuarioEncontrado and usuarioEncontrado["password"] == password:
                print(f"Bienvenido, {correo}, inicio de sesión exitoso.")
                chatbot(correo, isAdmin)
                break
            else:
                print("Credenciales incorrectas. Inténtalo de nuevo.")
                continue
        else:
            continue


def validarCorreo(correo):
    if "@" in correo and "." in correo.split("@")[-1] and " " not in correo:
        return True
    return False

def register(isAdmin):
    if isAdmin:
        archivo = "admins.json" 
    else:
        archivo = "users.json"

    if os.path.exists(archivo):
        with open(archivo, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    while True:
        correo = input("Ingrese su correo electrónico: ")

        if not validarCorreo(correo):
            print("correo invalido")
            continue

        correoExiste = False
        for usuario in data:
            if usuario["correo"] == correo:
                correoExiste = True
                break

        if correoExiste:
            print("Correo ya registrado. Intente con otro.")
            continue

        print("correo registrado con éxito")
        password = input("Ingrese una contraseña: ")
        print("Contraseña guardada con éxito")
        break

    nuevoUsuario = {
        "correo": correo,
        "password": password,
        "rol": "admin" if isAdmin else "user"
    }

    data.append(nuevoUsuario)

    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)
    print("Registro completado con éxito")

def mainLogin(admin):
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    while True:
        opc = input()
        if not opc.isdigit():
            print("Opción inválida")
            continue
        opc = int(opc)
        if 0 < opc < 4:
            match opc:
                case 1: login(admin)
                case 2: register(admin)
                case 3: return
        break

def selectAdminUser():
    AdminPassword = genPassword()
    print("Bienvenido al sistema de reclamos Bravo")
    admin = False
    while True:
        print("Seleccione un tipo de inicio de sesion")
        print("1. Administrador")
        print("2. Usuario")
        print("3. Salir")
        opc = input("Opción: ")
        if not opc.isdigit():
            print("Opcion no válida")
            continue
        opc = int(opc)
        if opc == 1:
            while True:
                password = input("ingrese la clave de administrador (o escriba 'salir' para volver): ")
                if password.lower() == "salir":
                    print("Volviendo al menu principal")
                    break
                if not password.isdigit() or int(password) != AdminPassword:
                    print("Acceso denegado")
                    continue
                print("Acceso concedido")
                admin = True
                mainLogin(admin)
                break
        elif opc == 2:
            print("Iniciando sesión como usuario...")
            admin = False
            mainLogin(admin)
            break
        elif opc == 3:
            break
selectAdminUser()