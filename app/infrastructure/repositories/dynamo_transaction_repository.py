from datetime import datetime
from decimal import Decimal
from uuid import UUID
from boto3.dynamodb.conditions import Key
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import TransactionRepository


class DynamoTransactionRepository(TransactionRepository):

    def __init__(self, table):
        self.table = table

    def add(self, transaction: Transaction) -> None:
        self.table.put_item(Item={
            "PK": f"USER#{transaction.user_id}",
            "SK": f"TRANSACTION#{transaction.id}",
            "id": str(transaction.id),
            "amount": str(transaction.amount),  
            "category_id": str(transaction.category_id),
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat(),
        })


    def get_by_id(self, user_id: UUID, transaction_id: UUID) -> Transaction | None:
        response = self.table.get_item(Key={
            "PK": f"USER#{user_id}",
            "SK": f"TRANSACTION#{transaction_id}"
        })
        item = response.get("Item")
        if not item:
            return None
        return self._to_entity(item)
    


    def list_by_user_id(self, user_id: UUID) -> list[Transaction]:
        response = self.table.query(
            KeyConditionExpression=Key("PK").eq(f"USER#{user_id}") & Key("SK").begins_with("TRANSACTION#")
        )
        return [self._to_entity(item) for item in response.get("Items", [])]
    

    def _to_entity(self, item: dict) -> Transaction:
        return Transaction(
            id=UUID(item["id"]),
            user_id=UUID(item["PK"].replace("USER#", "")),
            category_id=UUID(item["category_id"]),
            amount=Decimal(item["amount"]),  
            description=item.get("description"),
            created_at=datetime.fromisoformat(item["created_at"]),
        )
    

    def get_total_expenses_for_month(self, user_id, category_id, year, month) -> float:
        transactions = self.list_by_user_id(user_id)
        return sum(
            float(t.amount)
            for t in transactions
            if t.category_id == category_id
            and t.created_at.year == year
            and t.created_at.month == month
        )