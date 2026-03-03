import os

import boto3

from app.application.unit_of_work import UnitOfWork
from app.infrastructure.repositories.dynamo_category_repository import DynamoCategoryRepository
from app.infrastructure.repositories.dynamo_transaction_repository import DynamoTransactionRepository
from app.infrastructure.repositories.dynamo_user_repository import DynamoUserRepository


class DynamoUnitOfWork(UnitOfWork):

    def __enter__(self):
        dynamodb = boto3.resource("dynamodb")
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