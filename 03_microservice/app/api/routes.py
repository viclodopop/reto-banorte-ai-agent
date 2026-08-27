from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatCompletionRequest, ChatCompletionResponse, Choice, ChatMessage, Usage
from app.core.cv_agent import agent_service
from app.api.dependencies import verify_api_key
import time

router = APIRouter()

@router.post("/responses", response_model=ChatCompletionResponse, dependencies=[Depends(verify_api_key)])
async def chat_completions(request: ChatCompletionRequest):
    # 1. Extraemos el mensaje de forma segura por si viene vacío o con otra estructura
    user_query = "Hola, cuéntame sobre Víctor."
    if request.messages and len(request.messages) > 0:
        user_query = request.messages[-1].content

    # 2. Generamos la respuesta con tu RAG y Gemini
    respuesta_ia = agent_service.generate_response(user_query)

    # 3. Devolvemos el JSON con el estándar exacto que espera la plataforma
    return ChatCompletionResponse(
        id="chatcmpl-banorte-01",
        object="chat.completion",
        created=int(time.time()),
        model="banorte-cv-agent",
        choices=[
            Choice(
                index=0,
                message=ChatMessage(role="assistant", content=respuesta_ia),
                finish_reason="stop"
            )
        ],
        usage=Usage(prompt_tokens=50, completion_tokens=50, total_tokens=100)
    )