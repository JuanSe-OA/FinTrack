import os
import aws_cdk as cdk
from cdk_stack import FinTrackStack

app = cdk.App()
FinTrackStack(app, "FinTrackStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)
app.synth()