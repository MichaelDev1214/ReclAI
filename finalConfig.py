import requests

def genResume(conversacion):
    contexto = f"""
    Eres un sistema encargado de resumir la configuración de una empresa.

    Recibirás el historial completo de la conversación entre un administrador y un asistente.

    Tu tarea consiste en redactar un único párrafo que servirá como contexto para otra IA.

    Incluye únicamente:

    - Nombre de la empresa.
    - Actividad principal.
    - Productos o servicios.
    - Soluciones que puede ofrecer.
    - Políticas importantes.
    - Restricciones relevantes.

    No escribas listas.

    No uses viñetas.

    No escribas títulos.

    No hagas introducciones.

    No expliques el análisis.

    No menciones que proviene de una conversación.

    Redacta el texto de forma natural como si fuera una descripción interna del negocio.

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