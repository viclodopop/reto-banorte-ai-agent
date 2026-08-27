import time
import uuid
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    Choice, 
    ChatMessage, 
    Usage
)
from app.core.cv_agent import agent_service
from app.api.dependencies import verify_api_key

router = APIRouter()

@router.post("/chat/completions", response_model=ChatCompletionResponse, dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatCompletionRequest):
    """
    Endpoint principal. Recibe el historial de la conversación, 
    procesa la última pregunta a través del agente (RAG + Guardrails) 
    y devuelve la respuesta formateada.
    """
    if not request.messages:
        raise HTTPException(status_code=400, detail="El arreglo de mensajes no puede estar vacío.")

    # Extraemos el último mensaje (la pregunta actual del usuario)
    last_message = request.messages[-1]
    if last_message.role != "user":
        raise HTTPException(status_code=400, detail="El último mensaje debe ser del rol 'user'.")

    user_query = last_message.content

    # El agente hace toda la magia (sanitización, recuperación y generación)
    agent_response_text = await agent_service.answer_query(user_query)

    # Empaquetamos la respuesta en el formato estricto Open Responses
    response = ChatCompletionResponse(
        id=f"chatcmpl-{uuid.uuid4().hex[:12]}",
        created=int(time.time()),
        model=request.model or settings.MODEL_NAME,
        choices=[
            Choice(
                index=0,
                message=ChatMessage(
                    role="assistant",
                    content=agent_response_text
                ),
                finish_reason="stop"
            )
        ],
        usage=Usage(
            prompt_tokens=0, # En un entorno productivo calcularíamos los tokens reales
            completion_tokens=0,
            total_tokens=0
        )
    )

    return response