from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct

class SakchyamShresthaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_function = lambda_.Function(
            self, "HelloLambda",
            runtime=lambda_.Runtime.PYTHON_3_13,
            #handler="HelloWorld.lambda_handler",
            handler="WebhealthLambda.lambda_handler",
            code=lambda_.Code.from_asset("./modules"),
            timeout=Duration.seconds(30),
        )

        # Add permission to publish metrics to CloudWatch
        lambda_function.add_to_role_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=["cloudwatch:PutMetricData"],
                resources=["*"]
            )
        )
        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "SakchyamShresthaQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
