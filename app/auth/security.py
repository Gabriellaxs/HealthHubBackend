# app/auth/security.py
import bcrypt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import jwt

# ✅ Usa questi stessi valori anche nel router /auth/me quando decodifichi
SECRET_KEY = "SUPER_SECRET_KEY_CAMBIARE_IN_PRODUZIONE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def hash_password(password: str) -> str:
    # Genera un salt e hash della password usando bcrypt direttamente
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    try:
        # Verifica la password usando bcrypt direttamente
        pwd_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT con claim standard:
    - exp: scadenza
    - iat: issued-at
    Mantiene i tuoi claim custom (es: sub, role).
    """
    to_encode = data.copy()

    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # jose/jwt accetta datetime anche timezone-aware
    to_encode.update(
        {
            "exp": expire,
            "iat": now,
        }
    )

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
