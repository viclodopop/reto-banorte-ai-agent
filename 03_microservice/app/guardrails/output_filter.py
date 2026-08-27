import re

class OutputFilter:
    """
    Guardrail de salida (DLP / Data Loss Prevention).
    Enmascara datos sensibles o PII en caso de que el modelo intente generarlos.
    """
    
    PATTERNS = {
        # Detección de tarjetas bancarias (16 dígitos)
        "CREDIT_CARD": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        # Formato de RFC mexicano
        "RFC": r"\b[A-Z&Ñ]{3,4}\d{6}[A-V1-9][A-Z0-9][0-9A]\b",
        # Llaves de API comunes (Bearer, sk-, etc.)
        "API_KEYS": r"\b(sk-[a-zA-Z0-9]{20,}|AIza[a-zA-Z0-9_\-]{35})\b"
    }

    def __init__(self):
        self.compiled_patterns = {
            name: re.compile(pat, re.IGNORECASE) for name, pat in self.PATTERNS.items()
        }

    def filter(self, text: str) -> str:
        """Enmascara cualquier dato sensible detectado con un token seguro."""
        sanitized_text = text
        for name, pattern in self.compiled_patterns.items():
            sanitized_text = pattern.sub(f"[REDACTED_{name}]", sanitized_text)
        return sanitized_text

output_filter = OutputFilter()