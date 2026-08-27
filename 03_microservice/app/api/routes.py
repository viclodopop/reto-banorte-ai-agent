from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from app.api.dependencies import verify_api_key
from app.core.cv_agent import agent_service
from app.config.settings import settings
from typing import List, Optional, Any
from pydantic import BaseModel
import logging
import time
import uuid

router = APIRouter()
logger = logging.getLogger(__name__)

class MessageInput(BaseModel):
    role: str
    content: Any

class ChatRequest(BaseModel):
    model: Optional[str] = None
    messages: Optional[List[MessageInput]] = []
    input: Optional[List[MessageInput]] = []
    stream: Optional[bool] = False


def _extract_text_from_content(content: Any) -> Optional[str]:
    if isinstance(content, str):
        text = content.strip()
        return text or None

    if isinstance(content, list):
        for chunk in content:
            if not isinstance(chunk, dict):
                continue
            # Compatibilidad con formato Open Responses y variantes del frontend
            if isinstance(chunk.get("text"), str) and chunk.get("text", "").strip():
                return chunk["text"].strip()

    return None


def _extract_user_query(body: dict) -> str:
    default_query = "Hola, cuentame sobre la trayectoria y perfil de Victor Molina Sanchez."

    # Open Responses: input puede ser string o lista de items
    raw_input = body.get("input")
    if isinstance(raw_input, str) and raw_input.strip():
        return raw_input.strip()

    if isinstance(raw_input, list):
        for item in reversed(raw_input):
            if not isinstance(item, dict):
                continue
            if item.get("role") not in (None, "user"):
                continue
            candidate = _extract_text_from_content(item.get("content"))
            if candidate:
                return candidate

    # Chat Completions: messages
    messages = body.get("messages", [])
    if isinstance(messages, list):
        for msg in reversed(messages):
            if not isinstance(msg, dict):
                continue
            if msg.get("role") not in (None, "user"):
                continue
            candidate = _extract_text_from_content(msg.get("content"))
            if candidate:
                return candidate

    return default_query


def _build_open_response(answer: str, model_name: str) -> dict:
    created_at = int(time.time())
    response_id = f"resp_{uuid.uuid4().hex[:18]}"
    message_id = f"msg_{uuid.uuid4().hex[:18]}"

    return {
        "id": response_id,
        "object": "response",
        "created_at": created_at,
        "status": "completed",
        "error": None,
        "incomplete_details": None,
        "model": model_name,
        "output": [
            {
                "id": message_id,
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": answer,
                        "annotations": []
                    }
                ]
            }
        ],
        "parallel_tool_calls": False,
        "temperature": 0.1,
        "tool_choice": "none",
        "tools": [],
        "top_p": 1.0,
        "output_text": answer,
        "usage": {
            "input_tokens": 0,
            "output_tokens": 0,
            "total_tokens": 0
        }
    }


def _build_chat_completion_response(answer: str, model_name: str) -> dict:
    return {
        "id": f"chatcmpl_{uuid.uuid4().hex[:18]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model_name,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": answer,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        },
    }

@router.post("/responses", dependencies=[Depends(verify_api_key)])
async def chat_completions(raw_request: Request):
    try:
        body = await raw_request.json()
    except Exception:
        logger.exception("No fue posible parsear el JSON del request en /v1/responses")
        body = {}

    user_query = _extract_user_query(body)
    requested_model = body.get("model") or "banorte-cv-agent"
    logger.info(
        "Solicitud /v1/responses recibida | model=%s | stream=%s | query_len=%s",
        requested_model,
        bool(body.get("stream", False)),
        len(user_query),
    )

    try:
        answer = await agent_service.answer_query(user_query)
    except Exception:
        logger.exception("Fallo no controlado en answer_query")
        answer = (
            "Ocurrio un error interno al procesar la consulta. "
            "Intenta nuevamente en unos segundos."
        )

    open_response = _build_open_response(answer=answer, model_name=requested_model)
    logger.info(
        "Respuesta Open Responses terminal generada | status=%s | output_items=%s",
        open_response.get("status"),
        len(open_response.get("output", [])),
    )
    return JSONResponse(content=open_response)


@router.post("/chat/completions", dependencies=[Depends(verify_api_key)])
async def legacy_chat_completions(raw_request: Request):
    """Compatibilidad hacia atras para clientes que aun usan Chat Completions."""
    try:
        body = await raw_request.json()
    except Exception:
        logger.exception("No fue posible parsear el JSON del request en /v1/chat/completions")
        body = {}

    user_query = _extract_user_query(body)
    requested_model = body.get("model") or settings.MODEL_NAME
    logger.info(
        "Solicitud /v1/chat/completions recibida | model=%s | query_len=%s",
        requested_model,
        len(user_query),
    )

    try:
        answer = await agent_service.answer_query(user_query)
    except Exception:
        logger.exception("Fallo no controlado en answer_query para /chat/completions")
        answer = (
            "Ocurrio un error interno al procesar la consulta. "
            "Intenta nuevamente en unos segundos."
        )

    return JSONResponse(content=_build_chat_completion_response(answer, requested_model))