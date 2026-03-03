import boto3
from uuid import UUID
from datetime import datetime, timezone
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from boto3.dynamodb.conditions import Attr


class DynamoUserRepository(UserRepository):

    def __init__(self, table):
        self.table = table

    def add(self, user: User) -> None:
        self.table.put_item(Item={
            "PK": f"USER#{user.id}",
            "SK": "PROFILE",
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat(),
        })

    def get_by_id(self, user_id: UUID) -> User | None:
        response = self.table.get_item(Key={
            "PK": f"USER#{user_id}",
            "SK": "PROFILE"
        })
        item = response.get("Item")
        if not item:
            return None
        return self._to_entity(item)

    def get_by_email(self, email: str) -> User | None:
        response = self.table.scan(
            FilterExpression=Attr("email").eq(email)
        )
        items = response.get("Items", [])
        return self._to_entity(items[0]) if items else None

    def _to_entity(self, item: dict) -> User:
        return User(
            id=UUID(item["PK"].replace("USER#", "")),
            email=item["email"],
            hashed_password=item["hashed_password"],
            is_active=item["is_active"],
            created_at=datetime.fromisoformat(item["created_at"]),
        )