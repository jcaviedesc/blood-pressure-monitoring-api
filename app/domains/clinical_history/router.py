from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from firebase_admin import auth
from fastapi.encoders import jsonable_encoder
from app.dependencies.database import get_repository
from app.dependencies.authorization import get_professional_user
from app.core.repositories import UserRepository, DevicesRepository
from app.core.services import notifications

router = APIRouter(prefix='/clincal-history', tags=['Clinical history'])


@router.patch("/{patient_id}", status_code=status.HTTP_201_CREATED)
async def request_access_to_medical_records(
    patient_id: str,
    auth_professional_user: auth.UserRecord = Depends(get_professional_user),
    device_repo: DevicesRepository = Depends(
        get_repository(DevicesRepository)),
    users_repo: UserRepository = Depends(get_repository(UserRepository))
):
    professional_id = auth_professional_user.custom_claims.get('ref')
    # if professional_id == patient_id:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #                         detail="you cannot request access to your own medical record")

    device = await device_repo.get_device_by_user_id(patient_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="patient not found, request access to medical records failed",
        )
    else:
        patient = await users_repo.get_user_by_id(patient_id)
        # el paciente existe? el paciente no tiene asociado el profesional?
        if patient and professional_id in patient.linked_professionals:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="patient already linked",
            )
        body_message = f"hola {patient.name} soy {auth_professional_user.display_name} el profesional a cargo de tu seguimiento."
        android_actions = [notifications.AndroidAction(
            title='Aceptar', press_action={'id': 'medical_records_access'})]
        android_config = notifications.NotificationAndroid(
            large_icon=auth_professional_user.photo_url, color='#ef4565', importance=notifications.AndroidImportance.HIGH, actions=android_actions)
        notification = notifications.Notification(
            title='Solicitud de accesso a tu historia clinica', body=body_message, android=android_config)
        # send notification
        message_id = notifications.send(
            registration_token=device.token, notifee_message=notification)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
            {'message_id': message_id}, exclude_defaults=True, by_alias=False))
