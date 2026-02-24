from dataclasses import dataclass
from uuid import UUID

from app.application.unit_of_work import UnitOfWork


@dataclass
class MarkAlertAsReadCommand:
    alert_id: UUID


class MarkAlertAsReadUseCase:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(self, cmd: MarkAlertAsReadCommand) -> None:
        with self.uow:
            alert = self.uow.alerts.get_by_id(cmd.alert_id)
            if alert is None:
                raise ValueError("Alert not found")

            alert.read = True
            self.uow.alerts.update(alert)
            self.uow.commit()