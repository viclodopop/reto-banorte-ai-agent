from fastapi import APIRouter, Depends
from app.api.dependencies import verify_api_key
from pydantic import BaseModel
from typing import List, Optional, Any
import os
import google.generativeai as genai

router = APIRouter()

class MessageInput(BaseModel):
    role: str
    content: Any

class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: Optional[List[MessageInput]] = []
    input: Optional[List[MessageInput]] = []

@router.post("/responses", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatRequest):
    # 1. Extraemos la pregunta del usuario de forma segura
    user_query = "Hola, cuéntame sobre la trayectoria y perfil de Víctor Molina Sánchez."
    
    for container in [request.messages, request.input]:
        if container:
            for m in reversed(container):
                if hasattr(m, 'content') and m.content:
                    if isinstance(m.content, str):
                        user_query = m.content
                        break
                    elif isinstance(m.content, list) and len(m.content) > 0:
                        user_query = m.content[0].get("text", user_query)
                        break

    # 2. Contexto profesional del CV
    cv_context = """
    Perfil: Víctor Molina Sánchez, nacido el 19 de febrero de 2003. Estudiante de Actuaría en la UNAM. 
    Experiencia: Ex Ingeniero Back-end en Babel (desarrollo de microservicios, optimización de APIs y bases de datos). 
    Habilidades: Python, FastAPI, Docker, Google Cloud Run, Git, Terraform, DevSecOps, Zero Trust.
    Intereses: Colecciona Monster High, juega videojuegos en Steam/Nintendo, usa herramientas de desarrollo y dispositivos Samsung.
    """

    # 3. Llamada estricta y segura a Gemini usando exclusivamente variables de entorno
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Eres el asistente experto del CV de Víctor Molina. Responde de forma profesional, técnica y concisa basándote estrictamente en su información."
        )
        response = model.generate_content(f"Contexto: {cv_context}\n\nPregunta del evaluador: {user_query}")
        respuesta_ia = response.text
    except Exception as e:
        respuesta_ia = f"Hola, soy el agente de Víctor Molina. Es especialista en DevSecOps, Cloud y estudiante de Actuaría en la UNAM."

    # 4. Respuesta estructurada bajo el estándar Open Responses que espera Banorte
    return {
        "model": "banorte-cv-agent",
        "output": [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": respuesta_ia
                    }
                ]
            }
        ]
    }