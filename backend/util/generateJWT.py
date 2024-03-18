from datetime import UTC, datetime, timedelta

import jwt
from core.config import settings


def generate_jwt(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.now(UTC) + timedelta(days=1),
    }

    JWT = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return JWT
