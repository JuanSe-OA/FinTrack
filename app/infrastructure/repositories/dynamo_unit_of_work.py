import os
import boto3

from app.application.unit_of_work import UnitOfWork
from app.infrastructure.repositories.dynamo_user_repository import DynamoUserRepository
from app.infrastructure.repositories.dynamo_category_repository import DynamoCategoryRepository
from app.infrastructure.repositories.dynamo_transaction_repository import DynamoTransactionRepository
from app.infrastructure.repositories.dynamo_budget_repository import DynamoBudgetRepository
from app.infrastructure.repositories.dynamo_alert_repository import DynamoAlertRepository


class DynamoUnitOfWork(UnitOfWork):

    def __enter__(self):
        print("Entrando al UnitOfWork")
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        print(f"DYNAMO_TABLE_NAME: {os.getenv('DYNAMO_TABLE_NAME')}")
        self.table = dynamodb.Table(os.getenv("DYNAMO_TABLE_NAME"))

        self.users = DynamoUserRepository(self.table)
        self.categories = DynamoCategoryRepository(self.table)
        self.transactions = DynamoTransactionRepository(self.table)
        self.budgets = DynamoBudgetRepository(self.table)
        self.alerts = DynamoAlertRepository(self.table)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()

    def commit(self):
        pass  

    def rollback(self):
        pass 