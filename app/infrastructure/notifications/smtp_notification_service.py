import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.domain.services.notification_service import NotificationService




class SmtpNotificationService(NotificationService):

    def __init__(self, host: str, port: int, username: str, password: str, sender: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.sender = sender

    def send_budget_exceeded(self, user_email: str, category_name: str, spent: float, limit: float) -> None:
        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = user_email
        message["Subject"] = f"Budget exceeded: {category_name}"

        body = f"""
        You have exceeded your budget for {category_name}.
        Spent: {spent}
        Limit: {limit}
        Exceeded by: {spent - limit:.2f}
        """
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.sender, user_email, message.as_string())