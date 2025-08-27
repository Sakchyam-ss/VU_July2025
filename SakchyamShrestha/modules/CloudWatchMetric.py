#CloudWatchMetric.py --- IGNORE ---
import boto3

class CloudWatchMetricPublisher:
    """Helper class to publish custom metrics to AWS CloudWatch."""
    def __init__(self):
        self.client = boto3.client('cloudwatch')

    def put_metric_data(self, namespace, metric_name, dimensions, value):
        """Publishes a single metric data point to CloudWatch."""
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,
                }
            ]
        )