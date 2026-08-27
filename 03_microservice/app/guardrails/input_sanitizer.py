import re
from typing import Tuple

class InputSanitizer:
    """
    Guardrail de entrada diseñado bajo principios de seguridad bancaria.
    Detecta y mitiga ataques comunes de Prompt Injection y Jailbreaks (OWASP LLM01).
    """
    
    # Patrones de ataque conocidos para manipular el comportamiento del LLM
    INJECTION_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"olvida\s+(todas\s+las\s+)?instrucciones\s+anteriores",
        r"you\s+are\s+now\s+a",
        r"ahora\s+eres\s+un",
        r"system\s*prompt",
        r"reveal\s+(your\s+)?instructions",
        r"muestra\s+tu\s+prompt",
        r"dan\s+mode",
        r"developer\s+mode",
        r"bypass\s+restrictions",
    ]

    def __init__(self):
        self.compiled_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.INJECTION_PATTERNS
        ]

    def sanitize(self, text: str) -> Tuple[bool, str]:
        """
        Evalúa si la entrada del usuario contiene patrones maliciosos.
        Retorna (es_valido, mensaje_o_texto_limpio).
        """
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return False, (
                    "Lo siento, únicamente puedo responder preguntas relacionadas "
                    "con la trayectoria profesional, experiencia y habilidades de Víctor."
                )
        return True, text.strip()

input_sanitizer = InputSanitizer()