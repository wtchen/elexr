from fastapi import Depends
from ..security import oauth2_scheme
from ..types import users


def fake_decode_token(token):
    return users.User(
        username=token + "fakedecoded", email="john@example.com"
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return fake_decode_token(token)
