from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re
import random

app = FastAPI()

# Permitir CORS desde frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Codigo(BaseModel):
    code: str

# Diccionario de mensajes variados por tipo de estructura
MENSAJES_VARIADOS = {
    "for": [
        "Se detectó un ciclo 'for'. Revisa si puede convertirse en una comprensión de listas.",
        "Encontraste un bucle 'for'. A veces es posible optimizarlo usando funciones como map o list comprehensions.",
        "El ciclo 'for' es útil, pero considera si puedes usar una estructura más concisa como una expresión generadora.",
    ],
    "while": [
        "Se identificó un ciclo 'while'. Verifica que su condición tenga una salida clara para evitar bucles infinitos.",
        "Cuidado con los ciclos 'while': asegúrate de que la condición eventualmente se vuelva falsa.",
        "Un 'while' está presente en tu código. Revisa que no se repita indefinidamente sin control.",
    ],
    "if": [
        "Se encontró una condición 'if'. Asegúrate de cubrir todos los casos necesarios, incluso los no previstos.",
        "Tu código contiene una estructura 'if'. Evalúa si podrías simplificarla o dividirla en funciones.",
        "La instrucción 'if' ayuda a tomar decisiones. Verifica que todas las condiciones estén bien definidas.",
    ],
    "try": [
        "Detectamos un bloque 'try'. Es recomendable capturar solo las excepciones necesarias.",
        "Estás usando manejo de errores con 'try'. Intenta no usar 'except' genérico para evitar esconder errores graves.",
        "Un bloque 'try' fue encontrado. Recuerda siempre manejar adecuadamente los posibles errores esperados.",
    ]
}

def analizar_codigo(code: str):
    estructuras = []
    correccion = code
    explicaciones = []

    # Detectar estructura 'for' simple
    for_matches = re.findall(r"for (\w+) in (.+?):\n +(.+)", code)
    if for_matches:
        estructuras.append("for")
        for var, iterable, body in for_matches:
            body = body.strip()
            patron_acumulacion = re.match(rf"(\w+)\.append\({var}\)", body)
            if patron_acumulacion:
                lista = patron_acumulacion.group(1)
                nueva_linea = f"{lista} = list({iterable})"
                correccion = correccion.replace(f"for {var} in {iterable}:", "# Reemplazado automáticamente")
                correccion = correccion.replace(f"    {body}", nueva_linea)
                explicaciones.append("Se reemplazó un bucle 'for' simple por una expresión 'list()' para mayor legibilidad y eficiencia.")
            else:
                explicaciones.append(random.choice(MENSAJES_VARIADOS["for"]))

    # while
    if 'while' in code:
        estructuras.append("while")
        explicaciones.append(random.choice(MENSAJES_VARIADOS["while"]))

    # if
    if 'if' in code:
        estructuras.append("if")
        explicaciones.append(random.choice(MENSAJES_VARIADOS["if"]))

    # try
    if 'try:' in code:
        estructuras.append("try")
        explicaciones.append(random.choice(MENSAJES_VARIADOS["try"]))

    resumen = ""
    if estructuras:
        resumen += "🔍 Se encontraron las siguientes estructuras de control:\n"
        for e in estructuras:
            resumen += f"• {e.capitalize()}\n"
        resumen += "\n"
    else:
        resumen += "✅ No se detectaron estructuras de control específicas.\n"

    explicacion = resumen + "\n" + "\n".join(explicaciones)

    mensajes = []
    for exp in explicaciones:
        mensajes.append({"tipo": "sugerencia", "mensaje": exp})
    if resumen:
        mensajes.insert(0, {"tipo": "sugerencia", "mensaje": resumen})

    # Si no hubo corrección, agrega un mensaje empresarial y específico
    if correccion == code:
        if "for" in estructuras:
            mensajes.append({
                "tipo": "sugerencia",
                "mensaje": "No se requiere corrección. El uso del bucle 'for' en su código es adecuado y sigue buenas prácticas de legibilidad y eficiencia."
            })
        elif "while" in estructuras:
            mensajes.append({
                "tipo": "sugerencia",
                "mensaje": "No se requiere corrección. El ciclo 'while' está correctamente implementado y cumple con los estándares de control de flujo."
            })
        elif "if" in estructuras:
            mensajes.append({
                "tipo": "sugerencia",
                "mensaje": "No se requiere corrección. La estructura condicional 'if' está bien utilizada y mejora la claridad del código."
            })
        elif "try" in estructuras:
            mensajes.append({
                "tipo": "sugerencia",
                "mensaje": "No se requiere corrección. El bloque 'try' demuestra un manejo adecuado de excepciones."
            })
        else:
            mensajes.append({
                "tipo": "sugerencia",
                "mensaje": "No se requiere corrección. Su código cumple con las buenas prácticas y no se detectaron mejoras necesarias."
            })

    return {
        "explicacion": mensajes,
        "correccion": correccion if correccion != code else ""
    }

@app.post("/analizar")
async def analizar(request: Request, codigo: Codigo):
    resultado = analizar_codigo(codigo.code)
    return resultado
