from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_iam,
    RemovalPolicy,
    aws_events as events_,
    aws_events_targets as targets_,
    aws_cloudwatch as cloudwatch_,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamodb,
)
from constructs import Construct
from modules import constants as constants 
from aws_cdk.aws_dynamodb import TableV2, AttributeType

class SakchyamShresthaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create IAM role for Lambda with CloudWatch permissions
        webealthlambda_role = self.create_lambda_role("WebHealthLambdaRole")

        # Create the Lambda function for web health monitoring
        web_health_lambda = self.create_lambda(
            'WebHealthLambdaFunction',
            './modules',
            'WebHealthLambda.lambda_handler',
            webealthlambda_role
        )
        web_health_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Schedule Lambda to run every 1 minute
        lambda_schedule = events_.Schedule.rate(Duration.minutes(1))
        lambda_target = targets_.LambdaFunction(handler=web_health_lambda)

        # Create EventBridge rule to trigger Lambda
        rule = events_.Rule(self, "WebHealthInvocationRule", description="Periodic Lambda execution", enabled=True,
                            schedule=lambda_schedule, targets=[lambda_target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        # Define CloudWatch metrics for availability
        availability_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_METRIC_NAME_AVAILABILITY,
            dimensions_map={"URL": constants.URL_TO_MONITOR},
            label='URL Availability',
            statistic="Average",
            period=Duration.minutes(1),
        )

        # Define CloudWatch metrics for latency
        latency_metric = cloudwatch_.Metric(
            namespace=constants.URL_MONITOR_NAMESPACE,
            metric_name=constants.URL_MONITOR_METRIC_NAME_LATENCY,
            dimensions_map={"URL": constants.URL_TO_MONITOR},
            label='URL Latency',
            statistic="Average",
            period=Duration.minutes(1),
        )

        # Create CloudWatch alarms for availability
        availability_alarm = cloudwatch_.Alarm(self, "AvailabilityAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.LESS_THAN_THRESHOLD,
            threshold=0.99,
            evaluation_periods=1,
            metric=availability_metric,
            treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
        )

        # Create CloudWatch alarms for latency
        latency_alarm = cloudwatch_.Alarm(self, "LatencyAlarm",
            comparison_operator=cloudwatch_.ComparisonOperator.GREATER_THAN_THRESHOLD,
            threshold=0.3, 
            evaluation_periods=1,
            metric=latency_metric,
            treat_missing_data=cloudwatch_.TreatMissingData.BREACHING
        )
        # SNS Topic for alarm notifications
        topic = sns.Topic(self, "AlarmNotification")
        topic.add_subscription(subscriptions.EmailSubscription("ssakchyam@gmail.com"))

        # Attach SNS topic to CloudWatch alarms
        availability_alarm.add_alarm_action(cw_actions.SnsAction(topic))
        latency_alarm.add_alarm_action(cw_actions.SnsAction(topic))

        # CloudWatch dashboard
        graph_widget = cloudwatch_.GraphWidget(
            title="Web Health Metrics",
            left=[availability_metric, latency_metric],
            width=24,
            height=6,
            legend_position=cloudwatch_.LegendPosition.RIGHT,
            left_y_axis=cloudwatch_.YAxisProps(label="MetricValues", min=0, show_units=False),
            right_y_axis=cloudwatch_.YAxisProps(label="Time", min=0, show_units=False),
            period=Duration.minutes(1)
        )
        
        dashboard = cloudwatch_.Dashboard(self, "WebHealthDashboard")
        # Availability Dashboard widget
        dashboard.add_widgets(
            cloudwatch_.GraphWidget(
                title="Availability",
                left=[availability_metric],
                left_y_axis=cloudwatch_.YAxisProps(
                    label="Availability (0–1)",
                    min=0,
                    max=1,
                    show_units=False,
                ),
                width=12
            )
        )
        # Latency Dashboard widget
        dashboard.add_widgets(
            cloudwatch_.GraphWidget(
                title="Latency (p90)",
                left=[latency_metric],
                left_y_axis=cloudwatch_.YAxisProps(
                    label="Seconds",
                    min=0,
                    show_units=True,
                ),
                width=12
            )
        )

        # Create DynamoDB table V2
        db_table = dynamodb.Table(self, "WebHealthTableV2",
            partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create Lambda function for DynamoDB operations
        DBlambda_role = self.create_lambda_role("DBLambdaRole")
        DBlambda_role.add_to_policy(aws_iam.PolicyStatement(
            actions=["lambda:InvokeFunction"],
            resources=[web_health_lambda.function_arn]
        ))

        # Create the Lambda function for DynamoDB operations so that we can log results from WebHealthLambda
        DB_lambda = _lambda.Function(
            self,
            'Sakchyam_DynamoDBLambdaFunction',
            code=_lambda.Code.from_asset('./modules'),
            handler='DBLambda.lambda_handler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            role=DBlambda_role,
            timeout=Duration.seconds(15),
            environment={
                "TABLE_NAME": db_table.table_name,
                "WEBHEALTH_LAMBDA_NAME": "WebHealthLambda"
            }
        )
        DB_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        db_table.grant_write_data(DB_lambda)


    # Create IAM role for Lambda with CloudWatch permissions
    def create_lambda_role(self):
        """
        Creates and returns an IAM role for Lambda with CloudWatch permissions.
        """
    def create_lambda_role(self, role_id):
        lambda_role = aws_iam.Role(self, role_id,
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"),
            ]
        )
        return lambda_role

    # Create Lambda function
    def create_lambda(self, function_id, code_path, handler_name, role):

        return _lambda.Function(self, function_id,
            code=_lambda.Code.from_asset(code_path),
            handler=handler_name,
            runtime=_lambda.Runtime.PYTHON_3_9,
            role=role,
            timeout=Duration.seconds(15)
        )