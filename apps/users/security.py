from jose import jwt, JWTError

from datetime import timedelta, datetime

ALGORITHM = "HS256"


def create_jwt_token(data: dict, jwt_secret_key: str, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta

    to_encode = {**data, "exp": expire}

    token = jwt.encode(to_encode, jwt_secret_key, ALGORITHM)
    return token


def decode_jwt_token(token: str, jwt_secret_key: str) -> dict | None:
    try:
        decoded_token = jwt.decode(token, jwt_secret_key, algorithms=[ALGORITHM])

        return decoded_token
    except JWTError:
        return None
