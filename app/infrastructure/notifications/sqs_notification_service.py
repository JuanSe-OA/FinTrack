import json
import os
import boto3

from app.domain.services.notification_service import NotificationService

 


class SqsNotificationService(NotificationService):

    def __init__(self):
        self.sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION", "us-east-1"))
        self.queue_url = os.getenv("EMAIL_QUEUE_URL")

    def send_budget_exceeded(self, user_email: str, category_name: str, spent: float, limit: float) -> None:
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps({
                "user_email": user_email,
                "category_name": category_name,
                "spent": str(spent),
                "limit": str(limit),
            })
        )