from uuid import UUID
from boto3.dynamodb.conditions import Key, Attr
from app.domain.entities.alert import Alert
from app.domain.repositories.alert_repository import AlertRepository
from datetime import datetime


class DynamoAlertRepository(AlertRepository):
    def __init__(self, table):
        self.table = table

    def add(self, alert: Alert) -> None:
        self.table.put_item(Item={
            "PK": f"USER#{alert.user_id}",
            "SK": f"ALERT#{alert.id}",
            "id": str(alert.id),
            "user_id": str(alert.user_id),
            "message": alert.message,
            "created_at": alert.created_at.isoformat(),
            "read": alert.read,
        })

    def list_by_user(self, user_id: UUID) -> list[Alert]:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("ALERT#")
        )
        items = response.get("Items", [])
        return [self._to_entity(item) for item in items]

    def update(self,user_id : UUID, alert_id: UUID) -> None:
        self.table.update_item(
            Key={
                "PK": f"USER#{user_id}",
                "SK": f"ALERT#{alert_id}"
            },
            UpdateExpression="SET read = :read",
            ExpressionAttributeValues={
                ":read": True
            }
        )
        pass

    def get_by_id(self, user_id: UUID, alert_id: UUID) -> Alert | None:
        response = self.table.get_item(Key={
            "PK": f"USER#{user_id}",
            "SK": f"ALERT#{alert_id}"
        })
        item = response.get("Item")
        if not item:
            return None
        return self._to_entity(item)

    def _to_entity(self, item: dict) -> Alert:
        return Alert(
            id=UUID(item["id"]),
            user_id=UUID(item["user_id"]),
            message=item["message"],
            read=item["read"],
            created_at=datetime.fromisoformat(item["created_at"]),
        )