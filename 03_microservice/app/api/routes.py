from fastapi import APIRouter, Depends
from app.api.dependencies import verify_api_key
from pydantic import BaseModel
from typing import List, Optional, Any

router = APIRouter()

class ContentItem(BaseModel):
    type: Optional[str] = "input_text"
    text: Optional[str] = ""

class MessageInput(BaseModel):
    role: str
    content: Any # Puede venir como texto plano o como arreglo de objetos

class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: Optional[List[MessageInput]] = []
    input: Optional[List[MessageInput]] = []

@router.post("/responses", dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatRequest):
    # 1. Extraemos la pregunta sin importar si mandaron 'messages' o 'input'
    user_query = "Hola, cuéntame sobre Víctor."
    
    # Revisamos en messages
    if request.messages:
        for m in reversed(request.messages):
            if m.content:
                if isinstance(m.content, str):
                    user_query = m.content
                    break
                elif isinstance(m.content, list) and len(m.content) > 0:
                    user_query = m.content[0].get("text", user_query)
                    break
                    
    # Revisamos en input por si el cliente usa ese campo
    if request.input:
        for m in reversed(request.input):
            if m.content:
                if isinstance(m.content, str):
                    user_query = m.content
                    break
                elif isinstance(m.content, list) and len(m.content) > 0:
                    user_query = m.content[0].get("text", user_query)
                    break

    # 2. Generamos la respuesta con tu agente RAG y Gemini
    from app.core.cv_agent import agent_service
    respuesta_ia = agent_service.generate_response(user_query)

    # 3. Respondemos estrictamente bajo el esquema Open Responses que el chat de React espera
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