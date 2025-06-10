"""this  file used to encode and decode tokens"""

import jwt
from datetime import datetime, timedelta, timezone
from .config import jwt_setting
from uuid import uuid4

def generate_access_tokens(
    data: dict, expiry: timedelta = timedelta(days=1)
) -> str:
    token = jwt.encode(
        payload={
            **data,
            "jti":str(uuid4()),
            "exp": datetime.now(timezone.utc) + expiry,
        },
        algorithm=jwt_setting.JWT_ALGORITHM,
        key=jwt_setting.JWT_SECRET,
    )
    return token


def decode_access_tokens(token: str) -> dict:
    print('decode',jwt_setting.JWT_SECRET)
    try:
        return jwt.decode(
            jwt=token,
            key=jwt_setting.JWT_SECRET,
            algorithms=[jwt_setting.JWT_ALGORITHM],
        )
    except jwt.PyJWTError as e:
        print("decode errrrr", e)
        return None
