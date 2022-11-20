from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from starlette import status
from firebase_admin import auth
from fastapi.encoders import jsonable_encoder
from app.dependencies.database import get_repository
from app.dependencies.authorization import get_professional_user
from app.core.repositories import UserRepository, DevicesRepository
from app.core.services import notifications
from .repositories import ClinicalMonitoringRequestsRepository
from .models import ClinicalMonitoringRequestsCreateModel
from .schemas import ClinicalMonitoringRequestsUpdateSchema

router = APIRouter(prefix='/clinical-monitoring', tags=['Clinical monitoring'])


@router.post("/patients/{document_id}/requests", status_code=status.HTTP_201_CREATED)
async def request_for_patient_monitoring(
    document_id: str,
    auth_professional_user: auth.UserRecord = Depends(get_professional_user),
    device_repo: DevicesRepository = Depends(
        get_repository(DevicesRepository)),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    clinical_history_request_repo: ClinicalMonitoringRequestsRepository = Depends(
        get_repository(ClinicalMonitoringRequestsRepository)),
):
    # TODO implement chain of responsibility and change to use-cases 
    professional_id = ''
    if auth_professional_user.custom_claims is not None:
        professional_id = auth_professional_user.custom_claims.get('ref')
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="request access to medical records failed",
        )

    patient = await users_repo.get_user_by_document_id(document_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="patient not found, request access to medical records failed",
        )
    else:
        patient_id = str(patient.id)
        if professional_id == str(patient.id):
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="you cannot request access to your own medical record")
        
        if professional_id in patient.linked_professionals:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Already monitoring the patient",
            )

        patient_device = await device_repo.get_device_by_user_id(patient_id)
        if patient_device is None:
            # TODO agregar logs y monitor para alertar el error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups, we can not process your request, it is what it is, but we are working to solve it",
            )
        # persistimos la solicitud hecha por el profesional en base de datos
        clinical_monitoring_request = ClinicalMonitoringRequestsCreateModel(
            request_by=professional_id, patient_id=patient_id)  # type: ignore
        clinical_monitoring_request_created = await clinical_history_request_repo.create(clinical_monitoring_request)
        if clinical_monitoring_request_created is None:
            # TODO agregar logs y monitor para alertar el error
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ups, we can not process your request, it is what it is, but we are working to solve it",
            )

        notification_data = {
            'id': str(clinical_monitoring_request_created.id),
            'professional': auth_professional_user.display_name,
            'avatar': auth_professional_user.photo_url,
            'patient': patient_id,
        }
        # TODO i18n
        body_message = f"{auth_professional_user.display_name} ."

        android_press_action = notifications.NotificationPressAction(
            id='medical_records_access')

        android_actions = [notifications.AndroidAction(
            title='Aceptar', press_action=android_press_action)]

        android_config = notifications.NotificationAndroid(
            large_icon=auth_professional_user.photo_url, color='#ef4565', importance=notifications.AndroidImportance.HIGH, actions=android_actions, small_icon='ic_small_icon', channel_id='messages')

        notification = notifications.Notification(
            title='Solicitud de seguimiento clinico', body=body_message, android=android_config, data=notification_data)
        # send notification
        message_id = notifications.send(
            registration_token=patient_device.token, notifee_message=notification)
    
    response = {**notification_data, 'message_id': message_id}

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
        response, exclude_defaults=True, by_alias=False))


@router.patch("/patients/{patient_id}/requests/{request_id}")
async def patient_response_to_clinical_monitoring(
    patient_id: str,
    request_id: str,
    body: ClinicalMonitoringRequestsUpdateSchema = Body(...),
    users_repo: UserRepository = Depends(get_repository(UserRepository)),
    clinical_monitoring_request_repo: ClinicalMonitoringRequestsRepository = Depends(
        get_repository(ClinicalMonitoringRequestsRepository))
):
    # update request by id and patient_id with body body.
    updated_request = await clinical_monitoring_request_repo.update(request_id, payload=body)
    if updated_request:
        patient = await users_repo.get_user_by_id(patient_id)
        if patient is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="patient not found, request access to medical records failed",
            )
        else:
            # si todo bien y la respuesta es confirmed actualizamos linked_professionals del profesional.
            patient_updated = await users_repo.update_linked_specialists(patient_id=patient_id, specialist_id=updated_request.request_by)

        # TODO send push notification on response?
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(
            patient_updated, exclude_defaults=True, by_alias=False))
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ups, we can not process your request, it is what it is, but we are working to solve it",
        )
