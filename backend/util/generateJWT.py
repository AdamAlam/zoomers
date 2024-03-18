from datetime import UTC, datetime, timedelta

import jwt
from core.config import settings


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

    JWT = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return JWT
