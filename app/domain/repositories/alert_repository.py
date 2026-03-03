from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.alert import Alert


class AlertRepository(ABC):

    @abstractmethod
    def add(self, alert: Alert) -> None:
        pass

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[Alert]:
        pass

    @abstractmethod
    def update(self, alert_id: UUID) -> None:
        pass

    @abstractmethod
    def get_by_id(self,user_id: UUID, alert_id: UUID) -> Alert | None:
        pass
