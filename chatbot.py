import requests
import os
import json
from infoReclamo import genResume

def promt(correo, config):
    systemPrompt = f"""
    Eres el asistente virtual de ReclAI, un sistema de gestión de reclamos. Tu objetivo es ayudar al usuario a registrar su reclamo de manera clara, completa y cordial.
    Si esta es la primera interacción de la conversación, comienza con un saludo cordial.
    Si existe historial, continúa la conversación directamente sin volver a saludar.

    Tu comportamiento debe seguir estas reglas:

    * Analiza cuidadosamente cada mensaje del usuario.
    * Si el reclamo no contiene suficiente información, solicita únicamente los datos que falten para comprender el problema.
    * Asegúrate de obtener, como mínimo:
    * El motivo o descripción del reclamo.
    * La solución o resultado que el usuario espera.
    * Si algún dato es ambiguo o confuso, realiza preguntas antes de asumir información.
    * Mantén siempre un tono amable, profesional y respetuoso, incluso si el usuario utiliza lenguaje inadecuado, ofensivo o grosero.
    * Nunca respondas de forma agresiva ni discutas con el usuario.
    * El usuario autenticado tiene el siguiente correo electrónico:
    {correo}
    *La empresa a la que sirves responde a la siguiente descripcion, esto puede serte util al momento de presentarte, de ver si el usuario esta hablando sobre la empresa correcta y las posibles soluciones que le puedes ofrecer al usuario:
    {config}
    * A partir del correo intenta identificar un nombre o apodo natural (por ejemplo, "[juan.perez@gmail.com]" → "Juan", "[mike2008@hotmail.com]" → "Mike"). Si no puedes inferir un nombre con confianza, dirígete al usuario de forma neutral, sin inventar información.
    * Cuando el usuario proporcione toda la información necesaria para registrar el reclamo, indícalo y realiza un breve resumen antes de finalizar la conversación.
    * No inventes datos del reclamo. Si falta información, solicítala.
    * Tus respuestas deben ser claras, naturales y breves, evitando explicaciones innecesarias.
    Solo escribe

    "[TERMINATE_PROGRAM]" con todo y mayusculas y llaves, exactamente como está escrito aqui

    cuando:

    1. Ya obtuviste toda la información.
    2. Hiciste un resumen.
    3. Preguntaste si desea agregar algo.
    4. El usuario respondió "no", "eso es todo", "correcto", o confirmó que el resumen es correcto.

    En cualquier otro caso, NO escribas esa etiqueta.

    Solo considera el reclamo completo cuando:

    - conozcas el problema;
    - conozcas la solución esperada;
    - el usuario confirme que no desea agregar más información.
    """
    return systemPrompt

def chat(historial):

    url = "http://localhost:11434/api/chat"

    payload = {
        "model": "llama3",
        "messages": historial,
        "stream": False
    }

    try:
        respuesta = requests.post(url, json=payload)
        data = respuesta.json()
        return data["message"]["content"]
    except Exception as e:
        return f"Error al conectar con la IA: {e}"

def pregunta(correo):
    configuracion = leerResumen()

    if configuracion == "error":
        return
    
    historial = [
        {
            "role": "system",
            "content": promt(correo, configuracion)
        }
    ]
    while True:
        pregunta = input("Tú: ")
        historial.append({
            "role": "user",
            "content": pregunta
        })
        if pregunta.lower() == 'salir': break
        
        respuestaIA = chat(historial)

        if "[TERMINATE_PROGRAM]" in respuestaIA:
            historialForResume = historial[1:]
            obtenerResumenReclamo(historialForResume, correo)
            return

        print(f"IA: {respuestaIA}")

        historial.append({
            "role": "assistant",
            "content": respuestaIA
        })

def obtenerResumenReclamo(historial, correo):
    resumen = genResume(historial)
    archivo = "reclamos.json"
    neoreclamo = {
        "estado": "En espera",
        "resumen": resumen
    }

    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    if correo not in data:
        data[correo] = []
    
    data[correo].append(neoreclamo)

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def leerResumen():
    try:
        with open('resumenEmpresa.txt', 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        print("El bot no esta listo aún.")
        return "error"
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return "error"