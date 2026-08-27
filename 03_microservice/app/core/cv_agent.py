from google import genai
from google.genai import types
from app.config.settings import settings
from app.rag.retriever import retriever_service
from app.guardrails.input_sanitizer import input_sanitizer
from app.guardrails.output_filter import output_filter
from app.core.prompts import build_system_prompt
import logging


logger = logging.getLogger(__name__)

class CVAgent:
    """
    Agente de IA para consulta de CV.
    Combina RAG semántico, guardrails de seguridad y generación controlada.
    """
    def __init__(self):
        # Inicializa cliente SDK oficial de Google GenAI
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None
        logger.info(
            "CVAgent inicializado | model=%s | gemini_configured=%s",
            settings.MODEL_NAME,
            bool(settings.GEMINI_API_KEY),
        )

    async def answer_query(self, user_message: str) -> str:
        """Procesa la consulta pasando por filtros, recuperación RAG e inferencia."""
        logger.info("Inicio answer_query | input_len=%s", len(user_message or ""))
        
        # 1. Guardrail de entrada
        is_valid, sanitized_or_error = input_sanitizer.sanitize(user_message)
        if not is_valid:
            logger.warning("Input rechazado por guardrail de entrada")
            return sanitized_or_error

        # 2. Recuperación de contexto RAG
        context = retriever_service.get_relevant_context(sanitized_or_error)
        logger.info("Contexto recuperado | context_len=%s", len(context or ""))
        system_instruction = build_system_prompt(context)

        # 3. Inferencia con LLM (Fallback seguro si no hay API Key configurada)
        if not self.client:
            logger.warning("Modo simulacion activado: GEMINI_API_KEY no configurada")
            return f"[Modo Simulación / Sin API Key]: Contexto recuperado:\n{context}"

        try:
            logger.info("Invocando modelo Gemini | model=%s", settings.MODEL_NAME)
            response = self.client.models.generate_content(
                model=settings.MODEL_NAME,
                contents=sanitized_or_error,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1, # Máximo determinismo para perfil financiero
                    max_output_tokens=600,
                )
            )
            raw_output = response.text or "No se pudo generar una respuesta."
            logger.info("Respuesta modelo recibida | output_len=%s", len(raw_output or ""))
        except Exception as e:
            logger.exception("Error al invocar el modelo Gemini")
            raw_output = f"Ocurrió un error al procesar la solicitud con el modelo: {str(e)}"

        # 4. Guardrail de salida (DLP)
        safe_output = output_filter.filter(raw_output)
        if safe_output != raw_output:
            logger.warning("OutputFilter redacto datos sensibles en la respuesta")
        logger.info("Respuesta final lista | output_len=%s", len(safe_output or ""))
        return safe_output

agent_service = CVAgent()