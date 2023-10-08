from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette import status

from config import Config

cfg = Config()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class AuthError(Exception):
    pass

class UserData(BaseModel):
    roles: list = []
class VerifyToken:
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.signing_key = None
        self.token = token

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{cfg.AUTH0_DOMAIN}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise AuthError(str(error))
        except jwt.exceptions.DecodeError as error:
            raise AuthError(str(error))

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=cfg.AUTH0_ALGORITHMS,
                audience=cfg.AUTH0_AUDIENCE,
                issuer=cfg.AUTH0_ISSUER,
            )
        except Exception as e:
            raise AuthError(str(e))

        return payload

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = VerifyToken(token=token).verify()

    except AuthError:
        raise credentials_exception

    return UserData()
