from pydantic import BaseModel



class TokenVerifyRequest(BaseModel):
    token: str

class TokenVerifyResponse(BaseModel):
    sid: str
    iss: str
    iat: int
    aud: str
    sub: str
    exp: int

