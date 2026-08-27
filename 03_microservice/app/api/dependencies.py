from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Usamos HTTPBearer para atrapar el formato de Banorte automáticamente
security = HTTPBearer(auto_error=False)

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    expected_key = os.getenv("API_KEY", "banorte-live-secret-key-2026")
    
    # Validamos que el token exista y coincida
    if credentials and credentials.credentials == expected_key:
        return credentials.credentials
        
    raise HTTPException(status_code=401, detail="Acceso denegado. Llave incorrecta.")