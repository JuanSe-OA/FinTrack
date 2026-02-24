from abc import ABC, abstractmethod


class NotificationService(ABC):

    @abstractmethod
    def send_budget_exceeded(self, user_email: str, category_name: str, spent: float, limit: float) -> None:
        pass