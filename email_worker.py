import json
import boto3
import os


ses_client = boto3.client("ses", region_name=os.getenv("AWS_REGION", "us-east-1"))


def handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        email_type = body.get("type")

        if email_type == "budget_exceeded":
            send_budget_exceeded_email(body)
        elif email_type == "welcome":
            send_welcome_email(body)
        elif email_type == "login":
            send_login_notification_email(body)


def send_budget_exceeded_email(body):
    ses_client.send_email(
        Source=os.getenv("SES_SENDER_EMAIL"),
        Destination={"ToAddresses": [body["user_email"]]},
        Message={
            "Subject": {"Data": f"Budget exceeded: {body['category_name']}"},
            "Body": {
                "Text": {
                    "Data": (
                        f"You have exceeded your budget for {body['category_name']}.\n"
                        f"Spent: {body['spent']}\n"
                        f"Limit: {body['limit']}\n"
                        f"Exceeded by: {float(body['spent']) - float(body['limit']):.2f}"
                    )
                }
            }
        }
    )


def send_welcome_email(body):
    ses_client.send_email(
        Source=os.getenv("SES_SENDER_EMAIL"),
        Destination={"ToAddresses": [body["user_email"]]},
        Message={
            "Subject": {"Data": "Welcome to FinTrack!"},
            "Body": {
                "Text": {
                    "Data": f"Hi! Welcome to FinTrack. Your account has been created successfully."
                }
            }
        }
    )


def send_login_notification_email(body):
    ses_client.send_email(
        Source=os.getenv("SES_SENDER_EMAIL"),
        Destination={"ToAddresses": [body["user_email"]]},
        Message={
            "Subject": {"Data": "New login to FinTrack"},
            "Body": {
                "Text": {
                    "Data": f"A new login was detected on your FinTrack account."
                }
            }
        }
    )