import random
import secrets
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from src.api.dependencies import AccessTokenBearer
from src.core.db import get_session
from src.model.user import User
from src.services.email import send_otp_email, send_confirmation_email, send_reset_password_email
from src.services.user import UserService
from src.utils import generateAccessToken, generate_password_hash
from src.api.dependencies import RefreshTokenBearer
from datetime import datetime
from src.core.redis import add_jti_to_blacklist, delete_otp, get_otp, save_otp, get_resend_cooldown, save_reset_token, set_resend_cooldown, get_email_from_reset_token,delete_reset_token

auth_router = APIRouter()
users = UserService()
 
@auth_router.post("/signup")
async def signup(user_data: User, session: AsyncSession = Depends(get_session)):
    try:
        new_user = await users.signup(user_data, session)
        otp = f"{random.randint(100000, 999999)}"
        await save_otp(user_data.email, otp)
        send_otp_email(user_data.email, otp)
        return JSONResponse(
            content={"message": "User created successfully, Veuillez vérifier votre email pour le code OTP.", 
                     "user_id": str(new_user.id)
                    }, 
                    status_code=status.HTTP_201_CREATED)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
@auth_router.post("/verify-otp")
async def verify_account(user_data: User, code: str, session: AsyncSession = Depends(get_session)):
    stored_otp = await get_otp(user_data.email)
    
    if stored_otp is None or stored_otp != code:
        raise HTTPException(status_code=400, detail="Code invalide ou expiré")
    get_user = await users.get_user_by_email_or_username(user_data.email, user_data.username, session)
    if not get_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    access_token = generateAccessToken(user_data={"sub": str(get_user.id), "email": get_user.email})
    refresh_token = generateAccessToken(user_data={"sub": str(get_user.id), "email": get_user.email}, refresh=True)

    get_user.isverified = True
    session.add(get_user)
    await session.commit()
    await delete_otp(get_user.email)

    send_confirmation_email(get_user.email, get_user.first_name or "Utilisateur")

    return {
        "message": "Compte vérifié avec succès",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": str(get_user.id),
            "email": get_user.email,
            "first_name": get_user.first_name
        }
    }


@auth_router.post("/resend-otp")
async def resend_otp(user_data: User, session: AsyncSession = Depends(get_session)):
    user = await users.get_user_by_email_or_username(user_data.email, user_data.username, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Utilisateur introuvable"
        )

    cooldown = await get_resend_cooldown(user_data.email)
    if cooldown:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Veuillez patienter 60 secondes avant de renvoyer un code"
        )

    otp = f"{random.randint(100000, 999999)}"

    await save_otp(user_data.email, otp, expiry=300)
    await set_resend_cooldown(user_data.email, seconds=60)

    first_name = getattr(user, "first_name", "Utilisateur")
    send_otp_email(user_data.email, otp) 

    return {"message": "OTP renvoyé avec succès", "first_name": first_name}


@auth_router.post("/login")
async def login(login_data: User, session: AsyncSession = Depends(get_session)):
    user = await users.login(login_data, session)
    
    if not user:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou mot de passe incorrect")

    access_token = generateAccessToken(user_data={"sub": str(user.id), "email": user.email})
    refresh_token = generateAccessToken(user_data={"sub": str(user.id), "email": user.email}, refresh=True)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "email": user.email,
            "username": user.username
        }
    }

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = generateAccessToken(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


@auth_router.post("/forgot-password")
async def forgot_password(user_data: User, session: AsyncSession = Depends(get_session)):
    user = await users.get_user_by_email_or_username(user_data.email, user_data.username, session)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    token = secrets.token_urlsafe(32)
    await save_reset_token(user_data.email, token)

    send_reset_password_email(user_data.email, token)

    return {"message": "Lien de réinitialisation envoyé par email."}


@auth_router.post("/reset-password/{token}")
async def reset_password(user_data: User, token: str, new_password: str, session: AsyncSession = Depends(get_session)):
    email = await get_email_from_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Jeton invalide ou expiré")

    user = await users.get_user_by_email_or_username(user_data.email, user_data.username, session)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    user.password = generate_password_hash(new_password)
    session.add(user)
    await session.commit()

    await delete_reset_token(token)

    return {"message": "Mot de passe modifié avec succès !"}


@auth_router.post("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.get('jti')
    if jti:
        await add_jti_to_blacklist(jti)
        return JSONResponse(content={"message": "Successfully logged out"}, status_code=status.HTTP_200_OK)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")    