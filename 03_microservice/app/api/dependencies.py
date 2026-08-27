from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging

# Usamos HTTPBearer para atrapar el formato de Banorte automáticamente
security = HTTPBearer(auto_error=False)
logger = logging.getLogger(__name__)

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    expected_key = os.getenv("API_KEY")

    # Falla explicita si el servicio no tiene configurado el secreto.
    if not expected_key:
        logger.error("API_KEY no configurada en variables de entorno")
        raise HTTPException(status_code=500, detail="Configuracion incompleta del servicio.")
    
    # Se valida el token Bearer antes de procesar cualquier inferencia.
    # Validamos que el token exista y coincida
    if credentials and credentials.credentials == expected_key:
        return credentials.credentials
        
    raise HTTPException(status_code=401, detail="Acceso denegado. Llave incorrecta.")