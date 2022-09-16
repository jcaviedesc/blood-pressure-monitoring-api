from urllib import response
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from firebase_admin import auth
from fastapi.encoders import jsonable_encoder
from app.dependencies.database import get_repository
from app.dependencies.authorization import get_professional_user
from app.core.repositories import UserRepository, DevicesRepository
from app.core.services import notifications
from .repositories import ClinalHistoryRequestsRepository
from .models import ClinalHistoryRequestsCreateModel

router = APIRouter(prefix='/clincal-history', tags=['Clinical history'])


@router.post("/{patient_id}/request", status_code=status.HTTP_201_CREATED)
async def request_access_to_medical_records(
    patient_id: str,
    auth_professional_user: auth.UserRecord = Depends(get_professional_user),
    device_repo: DevicesRepository = Depends(
        get_repository(DevicesRepository)),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    clinical_history_request_repo: ClinalHistoryRequestsRepository = Depends(
        get_repository(ClinalHistoryRequestsRepository)),
):
    professional_id = auth_professional_user.custom_claims.get('ref')
    # if professional_id == patient_id:
    #     raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #                         detail="you cannot request access to your own medical record")

    patient = await users_repo.get_user_by_id(patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="patient not found, request access to medical records failed",
        )
    else:
        # el paciente existe? el paciente no tiene asociado el profesional?
        if professional_id in patient.linked_professionals:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="patient already linked",
            )

        device = await device_repo.get_device_by_user_id(patient_id)
        if device is None:
            # TODO agregar logs y monitor para alertar el error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups, we can not process your request, it is what it is, but we are working to solve it",
            )
        # persistimos la solicitud hecha por el profesional en base de datos
        clinical_history_request = ClinalHistoryRequestsCreateModel(
            request_by=professional_id, patiend_id=str(patient.id))  # type: ignore
        clinical_history_request_response = await clinical_history_request_repo.create(clinical_history_request)
        if clinical_history_request_response is None:
            # TODO agregar logs y monitor para alertar el error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups, we can not process your request, it is what it is, but we are working to solve it",
            )

        # TODO  enviar la notificaion push con el  clinical_history_request_response.id
        notification_data = {
            'chrId': str(clinical_history_request_response.id),
            'professional': auth_professional_user.display_name,
            'avatar': auth_professional_user.photo_url
        }
        body_message = f"hola {patient.name} soy {auth_professional_user.display_name} el profesional a cargo de tu seguimiento."
        android_press_action = notifications.NotificationPressAction(
            id='medical_records_access')
        android_actions = [notifications.AndroidAction(
            title='Aceptar', press_action=android_press_action)]
        android_config = notifications.NotificationAndroid(
            large_icon=auth_professional_user.photo_url, color='#ef4565', importance=notifications.AndroidImportance.HIGH, actions=android_actions, small_icon='ic_small_icon')
        notification = notifications.Notification(
            title='Solicitud de accesso a tu historia clinica', body=body_message, android=android_config, data=notification_data)
        # send notification
        message_id = notifications.send(
            registration_token=device.token, notifee_message=notification)
        response = {**notification_data, 'message_id': message_id}
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
            response, exclude_defaults=True, by_alias=False))

@router.patch("/{patient_id}/response/{request_id}")
async def response_access_to_medical_records():
    pass