import aws_cdk as cdk
from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_sqs as sqs,
    aws_lambda_event_sources as lambda_events,
    aws_secretsmanager as secretsmanager,
    aws_logs as logs,
    BundlingOptions,
)
from constructs import Construct


class FinTrackStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ─── DynamoDB ───────────────────────────────────────────
        table = dynamodb.Table(
            self, "FinTrackTable",
            table_name="fintrack",
            partition_key=dynamodb.Attribute(
                name="PK",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="SK",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # ─── Secrets Manager ────────────────────────────────────
        secret = secretsmanager.Secret(
            self, "FinTrackSecret",
            secret_name="fintrack/config",
            description="FinTrack API secrets",
        )

        # ─── SQS ────────────────────────────────────────────────
        email_queue = sqs.Queue(
            self, "EmailQueue",
            queue_name="fintrack-email-queue",
            visibility_timeout=cdk.Duration.seconds(30),
        )

        # ─── Log Groups ─────────────────────────────────────────
        api_log_group = logs.LogGroup(
            self, "FinTrackApiLogGroup",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        email_log_group = logs.LogGroup(
            self, "EmailWorkerLogGroup",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY,
        )

        # ─── Bundling ────────────────────────────────────────────
        bundling = BundlingOptions(
            image=lambda_.Runtime.PYTHON_3_12.bundling_image,
            command=[
                "bash", "-c",
                "pip install -r requirements.txt -t /asset-output && cp -r app /asset-output/ && cp email_worker.py /asset-output/"
            ]
        )

        # ─── Lambda principal (FastAPI) ──────────────────────────
        api_lambda = lambda_.Function(
            self, "FinTrackApi",
            function_name="fintrack-api",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.main.handler",
            code=lambda_.Code.from_asset("..", bundling=bundling),
            timeout=cdk.Duration.seconds(30),
            memory_size=256,
            environment={
                "DYNAMO_TABLE_NAME": table.table_name,
                "SECRET_NAME": secret.secret_name,
                "EMAIL_QUEUE_URL": email_queue.queue_url,
            },
            log_group=api_log_group,
        )

        # ─── Lambda worker (emails) ──────────────────────────────
        email_lambda = lambda_.Function(
            self, "EmailWorker",
            function_name="fintrack-email-worker",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="email_worker.handler",
            code=lambda_.Code.from_asset("..", bundling=bundling),
            timeout=cdk.Duration.seconds(30),
            environment={
                "SECRET_NAME": secret.secret_name,
                "SES_SENDER_EMAIL": "papcreativaexpress@gmail.com",
            },
            log_group=email_log_group,
        )

        # ─── Permisos ────────────────────────────────────────────
        table.grant_read_write_data(api_lambda)
        secret.grant_read(api_lambda)
        secret.grant_read(email_lambda)
        email_queue.grant_send_messages(api_lambda)
        email_queue.grant_consume_messages(email_lambda)

        # ─── SES permisos para email worker ─────────────────────
        from aws_cdk import aws_iam as iam
        email_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["ses:SendEmail", "ses:SendRawEmail"],
            resources=["*"]
        ))

        # ─── SQS trigger ────────────────────────────────────────
        email_lambda.add_event_source(
            lambda_events.SqsEventSource(email_queue, batch_size=1)
        )

        # ─── API Gateway ─────────────────────────────────────────
        api = apigw.LambdaRestApi(
            self, "FinTrackApiGateway",
            handler=api_lambda,
            rest_api_name="FinTrack API",
            proxy=True,
        )

        # ─── Outputs ─────────────────────────────────────────────
        cdk.CfnOutput(self, "ApiUrl", value=api.url)
        cdk.CfnOutput(self, "TableName", value=table.table_name)
        cdk.CfnOutput(self, "QueueUrl", value=email_queue.queue_url)