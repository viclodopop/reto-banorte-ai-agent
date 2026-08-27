from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# Esquema para cada mensaje dentro del historial de conversación
class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(
        ..., 
        description="Rol del emisor: system (reglas), user (pregunta), assistant (respuesta)"
    )
    content: str = Field(..., min_length=1, description="Texto del mensaje")

# Payload de entrada esperado por el endpoint /v1/chat/completions
class ChatCompletionRequest(BaseModel):
    model: Optional[str] = Field(
        default="banorte-cv-agent", 
        description="Identificador del modelo solicitado"
    )
    messages: List[ChatMessage] = Field(
        ..., 
        min_length=1, 
        description="Historial de mensajes de la sesión"
    )
    temperature: Optional[float] = Field(
        default=0.1, 
        ge=0.0, 
        le=2.0, 
        description="Determinismo de inferencia (valores bajos evitan alucinaciones)"
    )
    max_tokens: Optional[int] = Field(
        default=800, 
        description="Límite máximo de tokens en la respuesta"
    )

# Estructura interna de una opción de respuesta
class Choice(BaseModel):
    index: int = 0
    message: ChatMessage
    finish_reason: str = "stop"

# Estructura del consumo de tokens (metadata)
class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

# Respuesta estándar que entrega la API al consumidor
class ChatCompletionResponse(BaseModel):
    id: str = Field(..., description="Identificador único de la transacción")
    object: str = "chat.completion"
    created: int = Field(..., description="Timestamp Unix de generación")
    model: str = "banorte-cv-agent-v1"
    choices: List[Choice]
    usage: Usage