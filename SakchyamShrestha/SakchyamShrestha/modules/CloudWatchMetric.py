# modules/CloudWatchMetric.py
import boto3

_client = boto3.client("cloudwatch")  # reused across invocations

class CloudWatchMetricPublisher:
    """Helper class to publish custom metrics to AWS CloudWatch."""
    def put_metric_data(self, namespace, metric_name, dimensions, value, unit="None"):
        _client.put_metric_data(
            Namespace=namespace,
            MetricData=[{
                "MetricName": metric_name,
                "Dimensions": dimensions or [],
                "Value": float(value),
                "Unit": unit,
            }]
        )