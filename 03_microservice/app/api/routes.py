from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse
from app.api.dependencies import verify_api_key
from pydantic import BaseModel
from typing import List, Optional, Any
import os
import json
import google.generativeai as genai

router = APIRouter()

class MessageInput(BaseModel):
    role: str
    content: Any

class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: Optional[List[MessageInput]] = []
    input: Optional[List[MessageInput]] = []
    stream: Optional[bool] = False

@router.post("/responses", dependencies=[Depends(verify_api_key)])
async def chat_completions(raw_request: Request):
    try:
        body = await raw_request.json()
    except Exception:
        body = {}
    
    stream_requested = body.get("stream", False)
    messages = body.get("messages", []) or body.get("input", [])
    
    user_query = "Hola, cuéntame sobre la trayectoria y perfil de Víctor Molina Sánchez."
    if messages:
        last_msg = messages[-1]
        if isinstance(last_msg, dict):
            content = last_msg.get("content")
            if isinstance(content, str):
                user_query = content
            elif isinstance(content, list) and len(content) > 0:
                user_query = content[0].get("text", user_query)

    cv_context = """
    Perfil: Víctor Molina Sánchez, nacido el 19 de febrero de 2003. Estudiante de Actuaría en la UNAM. 
    Experiencia: Ex Ingeniero Back-end en Babel (desarrollo de microservicios, optimización de APIs y bases de datos). 
    Habilidades: Python, FastAPI, Docker, Google Cloud Run, Git, Terraform, DevSecOps, Zero Trust.
    Intereses: Colecciona Monster High, juega videojuegos en Steam/Nintendo, usa herramientas de desarrollo y dispositivos Samsung.
    """

    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Eres el asistente experto del CV de Víctor Molina. Responde de forma profesional, técnica y concisa basándote estrictamente en su información."
        )
        response = model.generate_content(f"Contexto: {cv_context}\n\nPregunta del evaluador: {user_query}")
        respuesta_ia = response.text.strip()
    except Exception as e:
        respuesta_ia = "Hola, soy el agente de Víctor Molina. Es especialista en DevSecOps, Cloud y estudiante de Actuaría en la UNAM."

    if stream_requested:
        async def event_generator():
            # Evento con tipo explícito que exige el validador de Banorte
            chunk_data = {
                "type": "text",
                "role": "assistant",
                "content": respuesta_ia,
                "finish_reason": "stop"
            }
            yield f"event: message\ndata: {json.dumps(chunk_data)}\n\n"
            yield f"event: done\ndata: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    payload = {
        "object": "chat.completion",
        "model": "banorte-cv-agent",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": respuesta_ia
                },
                "finish_reason": "stop"
            }
        ]
    }
    return JSONResponse(content=payload)