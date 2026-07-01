import requests

def genResume(conversacion):
    contexto = f"""
    Eres un sistema especializado en analizar conversaciones de reclamos.

    Recibirás el historial completo entre un cliente y el asistente virtual.

    Tu única tarea es generar un resumen interno que será leído por empleados de la empresa.

    Reglas:

    - No escribas títulos.
    - No escribas listas.
    - No escribas introducciones.
    - No escribas "Análisis".
    - No expliques el proceso.
    - No menciones la conversación.
    - No repitas información.
    - Redacta un único párrafo de entre 80 y 150 palabras.

    El resumen debe incluir únicamente:

    - Qué ocurrió.
    - Qué producto o servicio está involucrado.
    - Qué problema presentó el cliente.
    - Qué esperaba como solución.
    - Qué solución quedó acordada.

    Si algún dato no aparece en la conversación, simplemente omítelo.

    Conversación:

    {conversacion}
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": contexto,
            "stream": False
        }
    )

    return response.json()["response"]