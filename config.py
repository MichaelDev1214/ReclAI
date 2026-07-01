from adminChatbot import pregunta

def config(correo):
    print("Que desea gestionar?")
    print("1. Registrar empresa")
    print("2. Cerrar sesión")
    while True:
        opc = input("Seleccione una opción")
        if not opc.isdigit():
            continue
        opc = int(opc)
        if opc == 1:
            pregunta(correo)
        elif opc == 2:
            return
        else:
            continue