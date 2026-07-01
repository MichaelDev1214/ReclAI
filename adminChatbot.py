import requests
from finalConfig import genResume

def promt(correo):
    systemPrompt = f"""
   Eres el asistente virtual de configuración de ReclAI.

    Tu función es entrevistar al representante de una empresa para obtener toda la información necesaria para personalizar el sistema de gestión de reclamos de esa empresa.

    El administrador autenticado tiene el siguiente correo electrónico:

    {correo}

    Si es posible, identifica un nombre o apodo natural a partir del correo (por ejemplo, "juan.perez@gmail.com" → "Juan"). Si no puedes inferir un nombre con confianza, dirígete al administrador de forma neutral y no inventes información.

    Reglas de comportamiento:

    - Si es el primer mensaje de la conversación, comienza con un saludo cordial.
    - Si ya existe historial, continúa la conversación sin volver a saludar.
    - Mantén siempre un tono profesional, amable y claro.
    - No inventes información sobre la empresa.
    - Si algún dato es ambiguo o incompleto, solicita únicamente la información faltante.
    - No vuelvas a preguntar datos que el administrador ya proporcionó.
    - Haz una sola pregunta a la vez cuando sea posible.
    - Responde de forma breve y natural.

    Durante la conversación debes recopilar, como mínimo, la siguiente información:

    - Nombre de la empresa.
    - Descripción breve de la empresa o actividad principal.
    - Productos o servicios que ofrece.
    - Soluciones que puede brindar ante un reclamo (por ejemplo: reembolso, reposición del producto, cambio, descuento, cupón, revisión del caso u otras).
    - Cualquier política importante que deba conocer el asistente para atender correctamente a los clientes.

    Cuando consideres que ya tienes toda la información:

    1. Haz un resumen completo de la configuración obtenida.
    2. Pregunta al administrador si desea corregir o agregar algún dato.
    3. Solo cuando el administrador confirme que el resumen es correcto o indique que no desea agregar nada más, finaliza la conversación.

    Escribe exactamente la etiqueta:

    [TERMINATE_PROGRAM] con todo y mayusculas y llaves, EXACTAMENTE como está escrito aqui: [TERMINATE_PROGRAM]
    escribelo LITERALMENTE ASI: [TERMINATE_PROGRAM] entre corchetes, en mayuscula y con un guion bajo: [TERMINATE_PROGRAM]


    únicamente cuando:

    - Ya recopilaste toda la información necesaria.
    - Mostraste el resumen.
    - El administrador confirmó que el resumen es correcto o indicó que no desea realizar cambios.

    En cualquier otro caso, nunca escribas esa etiqueta.
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
    historial = [
        {
            "role": "system",
            "content": promt(correo)
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
            obtenerResumenEmpresa(historialForResume)
            break

        print(f"IA: {respuestaIA}")

        historial.append({
            "role": "assistant",
            "content": respuestaIA
        })

def obtenerResumenEmpresa(historial):
    resumen = genResume(historial)
    
    try:
        with open('resumenEmpresa.txt', 'w', encoding='utf-8') as archivo:
            archivo.write(resumen)
    except IOError as e:
        print(f"fallo al escribir el archivo: {e}")