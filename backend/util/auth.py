from datetime import UTC, datetime, timedelta

from core.config import settings
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError, decode, encode

security = HTTPBearer()


def generate_jwt(user_id: int) -> str:
    """
    Generate a JSON Web Token (JWT) for the given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The generated JWT.

    """
    payload = {
        "user_id": user_id,
        "exp": datetime.now(UTC) + timedelta(days=1),
    }

    JWT = encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return JWT


def validate_jwt(token: str = Security(security)):
    """
    Validate a JSON Web Token (JWT).

    Args:
        jwt (str): The JWT to validate.

    Returns:
        bool: True if the JWT is valid, False otherwise.

    """
    credentials: HTTPAuthorizationCredentials = token
    jwt_token = credentials.credentials
    try:
        payload = decode(jwt_token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials. Please log in.",
        )
