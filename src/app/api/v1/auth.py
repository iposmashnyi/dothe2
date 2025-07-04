from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from app.api.dependencies import CurrentUserDep, DatabaseDep
from app.core.config import settings
from app.core.email import send_magic_link_email, send_welcome_email
from app.core.logger import logging
from app.core.security import create_access_token
from app.crud.auth import (
    create_auth_token,
    get_auth_token_by_code,
    get_auth_token_by_token,
    mark_token_as_used,
)
from app.crud.users import create_user, get_user_by_email, get_user_by_id, get_user_by_username
from app.schemas.auth import EmailRequest, Token, VerifyCodeRequest
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

logger = logging.getLogger(__name__)


@router.post("/request-login", status_code=204)
async def request_login(
    request: Request,
    email_request: EmailRequest,
    db: DatabaseDep,
) -> None:
    email = email_request.email

    user = await get_user_by_email(db, email)
    if not user:
        # Create new user with minimal info
        username = email.split("@")[0]
        # Ensure username is unique
        base_username = username[:20]  # Max 20 chars
        final_username = base_username
        counter = 1
        while await get_user_by_username(db, final_username):
            final_username = f"{base_username}{counter}"
            counter += 1

        user_create = UserCreate(
            email=email,
            name=base_username,
            username=final_username,
        )
        user = await create_user(db, user_create)

        # Send welcome email
        await send_welcome_email(user.email, user.name)
        logger.info(f"New user created: {user.email}")

    # Create auth token
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", "")[:200]

    auth_token = await create_auth_token(
        db,
        user_id=user.id,
        ip_address=client_ip,
        user_agent=user_agent,
    )

    # Generate magic link
    magic_link = f"{settings.BASE_URL}/auth/verify?token={auth_token.token}"

    # Send email
    await send_magic_link_email(
        email=user.email,
        name=user.name,
        magic_link=magic_link,
        otp_code=auth_token.code,
    )


@router.post("/verify-code", response_model=Token)
async def verify_code(
    verify_request: VerifyCodeRequest,
    db: DatabaseDep,
) -> Token:
    auth_token = await get_auth_token_by_code(db, verify_request.email, verify_request.code)

    if not auth_token:
        raise HTTPException(status_code=400, detail="Invalid or expired code")

    # Mark token as used
    await mark_token_as_used(db, auth_token)

    # Create JWT token
    access_token = create_access_token(data={"sub": str(auth_token.user_id), "email": verify_request.email})

    return Token(access_token=access_token)


@router.get("/verify")
async def verify_magic_link(
    token: str,
    db: DatabaseDep,
) -> RedirectResponse:
    auth_token = await get_auth_token_by_token(db, token)

    if not auth_token:
        # Redirect to error page
        return RedirectResponse(url=f"{settings.BASE_URL}/auth/error?reason=invalid_token")

    # Mark token as used
    await mark_token_as_used(db, auth_token)

    # Get user
    user = await get_user_by_id(db, auth_token.user_id)
    if not user:
        return RedirectResponse(url=f"{settings.BASE_URL}/auth/error?reason=user_not_found")

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

    # Redirect to frontend with token
    return RedirectResponse(url=f"{settings.BASE_URL}/auth/success?token={access_token}", status_code=302)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: CurrentUserDep,
) -> UserResponse:
    return current_user
