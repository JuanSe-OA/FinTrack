from abc import ABC, abstractmethod
from uuid import UUID

class TokenService(ABC):

    @abstractmethod
    def generate(self, user_id: UUID) -> str:
        pass

    @abstractmethod
    def decode(self, token: str) -> UUID:
        pass