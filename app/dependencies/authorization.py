from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
import firebase_admin
from firebase_admin import auth
from loguru import logger

firebase_admin.initialize_app()


async def get_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        decoded_token = auth.verify_id_token(
            cred.credentials, check_revoked=True)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    except auth.ExpiredIdTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{err}",
            headers={'WWW-Authenticate': 'Bearer error="expired_token"'},
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"{err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    return decoded_token


def get_user_with_claims(current_user=Depends(get_user)):
    try:
        user = auth.get_user(current_user.get('uid'))
        if not user.custom_claims:
            logger.error(f"user {current_user.get('uid')} has not custom_claims")
            raise HTTPException(
                status_code=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
                detail=f"reauthentication required",
                headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
            )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    except auth.UserNotFoundError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    return user


def get_professional_user(user=Depends(get_user_with_claims)):
    if not user.custom_claims.get('role', -1) == 1:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Sorry! user is not authorized",
        )
    return user
