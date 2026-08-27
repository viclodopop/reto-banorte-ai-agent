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

    def _expand_if_too_short(self, answer: str, context: str) -> str:
        """Garantiza una respuesta minima util sin inventar informacion fuera del contexto."""
        normalized = (answer or "").strip()
        if len(normalized) >= 260:
            return normalized

        context_lines = [line.strip(" -\t") for line in context.splitlines() if line.strip()]
        context_lines = [line for line in context_lines if len(line) > 25]
        highlights = context_lines[:4]

        if not highlights:
            return normalized

        bullet_points = "\n".join(f"- {line}" for line in highlights)
        expanded = (
            f"{normalized}\n\n"
            "Para dar mayor contexto del perfil, estos son puntos relevantes:\n"
            f"{bullet_points}\n\n"
            "Si quieres, puedo profundizar en experiencia, educacion, habilidades o proyectos."
        )
        logger.info(
            "Respuesta expandida por longitud corta | original_len=%s | expanded_len=%s",
            len(normalized),
            len(expanded),
        )
        return expanded

    async def answer_query(self, user_message: str) -> str:
        """Procesa la consulta pasando por filtros, recuperación RAG e inferencia."""
        logger.info("Inicio answer_query | input_len=%s", len(user_message or ""))
        
        # Primera barrera: bloquea intentos de prompt injection.
        # 1. Guardrail de entrada
        is_valid, sanitized_or_error = input_sanitizer.sanitize(user_message)
        if not is_valid:
            logger.warning("Input rechazado por guardrail de entrada")
            return sanitized_or_error

        # Recupera evidencia textual del CV para anclar la respuesta del modelo.
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
                    # El system prompt define límites y tono del agente.
                    system_instruction=system_instruction,
                    temperature=0.1, # Máximo determinismo para perfil financiero
                    max_output_tokens=900,
                )
            )
            raw_output = response.text or "No se pudo generar una respuesta."
            raw_output = self._expand_if_too_short(raw_output, context)
            logger.info("Respuesta modelo recibida | output_len=%s", len(raw_output or ""))
        except Exception as e:
            logger.exception("Error al invocar el modelo Gemini")
            raw_output = f"Ocurrió un error al procesar la solicitud con el modelo: {str(e)}"

        # Última barrera: evita fuga accidental de datos sensibles.
        # 4. Guardrail de salida (DLP)
        safe_output = output_filter.filter(raw_output)
        if safe_output != raw_output:
            logger.warning("OutputFilter redacto datos sensibles en la respuesta")
        logger.info("Respuesta final lista | output_len=%s", len(safe_output or ""))
        return safe_output

agent_service = CVAgent()