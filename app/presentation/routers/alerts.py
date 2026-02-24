from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.application.use_cases.alert.get_user_alert_use_case import GetUserAlertsUseCase
from app.application.use_cases.alert.mark_alert_as_read_use_case import MarkAlertAsReadCommand, MarkAlertAsReadUseCase
from app.infrastructure.sql_alchemy_unit_of_work import SqlAlchemyUnitOfWork
from app.presentation.dependencies import get_current_user_id


router = APIRouter(prefix="/alerts", tags=["Alerts"])


# Schema
class AlertResponse(BaseModel):
    id: str
    message: str
    read: bool
    created_at: datetime


# Endpoints
@router.get("/", response_model=list[AlertResponse])
def get_user_alerts(user_id: UUID = Depends(get_current_user_id)):
    uow = SqlAlchemyUnitOfWork()
    use_case = GetUserAlertsUseCase(uow)
    try:
        alerts = use_case.execute(user_id)
        return [
            AlertResponse(
                id=str(a.id),
                message=a.message,
                read=a.read,
                created_at=a.created_at
            )
            for a in alerts
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{alert_id}/read", status_code=204)
def mark_alert_as_read(
    alert_id: UUID,
    user_id: UUID = Depends(get_current_user_id)
):
    uow = SqlAlchemyUnitOfWork()
    use_case = MarkAlertAsReadUseCase(uow)
    try:
        use_case.execute(MarkAlertAsReadCommand(alert_id=alert_id))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))