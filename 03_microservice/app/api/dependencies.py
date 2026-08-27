from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.settings import settings

security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Valida que el token enviado en la cabecera (Authorization: Bearer <token>)
    coincida con la API Key interna del servicio.
    Demuestra un manejo de seguridad básico pero necesario en ambientes corporativos.
    """
    if credentials.credentials != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas. Acceso denegado al agente CV.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials