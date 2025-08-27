#MainStack.py --- IGNORE ---
from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam,
    RemovalPolicy,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_cloudwatch_actions as cw_actions
    # aws_sqs as sqs,
)
from constructs import Construct
from modules import constants as constants 

class SakchyamShresthaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lambda with CloudWatch permissions
        lambda_role = self.create_lambda_role()

        # Create the Lambda function for web health monitoring
        web_health_lambda = self.create_lambda(
            'WebHealthLambdaFunction',
            './modules',
            'WebHealthLambda.lambda_handler',
            lambda_role
        )
        web_health_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Schedule Lambda to run every minute
        lambda_schedule = events_.Schedule.rate(Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=web_health_lambda)

        # Create EventBridge rule to trigger Lambda
        rule = events_.Rule(self, "WebHealthInvocationRule", description="Periodic Lambda execution", enabled=True,
                            schedule=lambda_schedule, targets=[lambda_target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        # Define CloudWatch metrics for availability and latency
        availability_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_METRIC_NAME_AVAILABILITY,
            dimensions_map={"URL": constants.URL_TO_MONITOR},
            label='URL Availability',
            statistic="Average",
            period=Duration.minutes(1),
        )

        latency_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_METRIC_NAME_LATENCY,
            dimensions_map={"URL": constants.URL_TO_MONITOR},
            label='URL Latency',
            statistic="Average",
            period=Duration.minutes(1),
        )

        # Create CloudWatch alarms for availability and latency
        availability_alarm = cloudwatch_.Alarm(self, "AvailabilityAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold=0.99,
            evaluation_periods=1,
            metric=availability_metric,
            treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
        )

        latency_alarm = cloudwatch_.Alarm(self, "LatencyAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=0.75, 
            evaluation_periods=1,
            metric=latency_metric,
            treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
        )

    def create_lambda_role(self):
        """
        Creates and returns an IAM role for Lambda with CloudWatch permissions.
        """
        lambda_role = aws_iam.Role(self, "WebHealthLambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
            ]
        )
        return lambda_role

    def create_lambda(self, function_id, code_path, handler_name, role):
        """
        Creates and returns a Lambda function resource.
        Args:
            function_id (str): Logical ID for the Lambda function
            code_path (str): Path to the Lambda code directory
            handler_name (str): Lambda handler function name
            role (aws_iam.Role): IAM role for the Lambda function
        """
        return _lambda.Function(self, function_id,
            code=_lambda.Code.from_asset(code_path),
            handler=handler_name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            role=role,
            timeout=Duration.seconds(20)
        )