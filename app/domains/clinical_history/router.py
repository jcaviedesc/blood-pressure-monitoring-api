from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from fastapi.encoders import jsonable_encoder
from ...dependencies.database import get_repository
from ...dependencies.authorization import get_professional_user
from ...core.repositories.devices import DevicesRepository
from ...core.services import notifications

router = APIRouter(prefix='/clincal-history', tags=['Clinical history'])


@router.patch("/{patient_id}", status_code=status.HTTP_201_CREATED)
async def request_access_to_medical_records(
    patient_id: str,
    auth_professional_user=Depends(get_professional_user),
    device_repo: DevicesRepository = Depends(get_repository(DevicesRepository))
):
    user_id = auth_professional_user.custom_claims.get('ref')
    if user_id == patient_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="you cannot request access to your own medical record")
    
    device = await device_repo.get_device_by_user_id(patient_id)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="patient not found, request access to medical records failed",
        )
    else:
        patient = {}
        notification = notifications.Notification(
            title='notifee remote 7', body='notificacion creada desde el back')
        # send notification
        message_id = notifications.send(
            registration_token=device.token, notifee_message=notification)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
            {'message_id': message_id}, exclude_defaults=True, by_alias=False))
