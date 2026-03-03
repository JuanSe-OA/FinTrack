from decimal import Decimal
from uuid import UUID

from boto3.dynamodb.conditions import Key, Attr

from app.domain.entities.budget import Budget
from app.domain.repositories.budget_repository import BudgetRepository


class DynamoBudgetRepository(BudgetRepository):

    def __init__(self, table):
        self.table = table

    def add(self, budget: Budget) -> None:
        self.table.put_item(Item={
            "PK": f"USER#{budget.user_id}",
            "SK": f"BUDGET#{budget.id}",
            "id": str(budget.id),
            "user_id": str(budget.user_id),
            "category_id": str(budget.category_id),
            "month": budget.month,
            "year": budget.year,
            "limit_amount": str(budget.limit_amount),
        })

    def get_by_id(self, user_id: UUID, budget_id: UUID) -> Budget | None:
        response = self.table.get_item(Key={
            "PK": f"USER#{user_id}",
            "SK": f"BUDGET#{budget_id}"
        })
        item = response.get("Item")
        if not item:
            return None
        return self._to_entity(item)

    def get_by_user_category_month_year(
        self,
        user_id: UUID,
        category_id: UUID,
        month: int,
        year: int
    ) -> Budget | None:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("BUDGET#"),
            FilterExpression=
                Attr("category_id").eq(str(category_id)) &
                Attr("month").eq(month) &
                Attr("year").eq(year)
        )
        items = response.get("Items", [])
        return self._to_entity(items[0]) if items else None

    def update(self, budget: Budget) -> None:
        self.table.update_item(
            Key={
                "PK": f"USER#{budget.user_id}",
                "SK": f"BUDGET#{budget.id}"
            },
            UpdateExpression="SET limit_amount = :limit_amount",
            ExpressionAttributeValues={
                ":limit_amount": str(budget.limit_amount)
            }
        )

    def _to_entity(self, item: dict) -> Budget:
        return Budget(
            id=UUID(item["id"]),
            user_id=UUID(item["user_id"]),
            category_id=UUID(item["category_id"]),
            month=int(item["month"]),
            year=int(item["year"]),
            limit_amount=Decimal(item["limit_amount"]),
        )