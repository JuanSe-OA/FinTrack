from app.domain.entities.alert import Alert
from app.domain.repositories.alert_repository import AlertRepository
from sqlalchemy.orm import Session

from app.infrastructure.database.models.alert_model import AlertModel


class SqlAlchemyAlertRepository(AlertRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, alert: Alert) -> None:
        model = AlertModel(
            id=alert.id,
            user_id=alert.user_id,
            message=alert.category_id,
            read=alert.threshold,
            created_at=alert.created_at,
            user = alert.user
        )
        self.session.add(model)

    def list_by_user(self, user_id) -> list[Alert]:
        models = self.session.query(AlertModel).filter_by(user_id=user_id).all()
        return [
            Alert(
                id=model.id,
                user_id=model.user_id,
                message=model.message,
                read=model.read,
                created_at=model.created_at,
                user = model.user
            )
            for model in models
        ]
