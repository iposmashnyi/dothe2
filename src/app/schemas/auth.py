from pydantic import BaseModel, EmailStr, Field


class EmailRequest(BaseModel):
    email: EmailStr = Field(..., description="Email address to send magic link to")


class VerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str = Field(..., min_length=6, max_length=6, description="6-digit verification code")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: int | None = None
    email: str | None = None
