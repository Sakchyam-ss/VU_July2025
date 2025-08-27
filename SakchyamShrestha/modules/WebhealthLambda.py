#WebHealthLambda.py --- IGNORE ---
import urllib.request
import time
# Import helper class for publishing metrics to CloudWatch
from CloudWatchMetric import CloudWatchMetricPublisher
# Import project constants
import constants

def get_url_latency(url):
    """Returns the latency (in seconds) for a given URL."""
    try:
        start = time.time()
        req = urllib.request.Request(f"https://{url}")
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = time.time() - start
        return latency
    except Exception as e:
        print(f"Error getting latency for {url}: {e}")
        return 0

def get_url_availability(url):
    """Returns 1 if the URL is available (HTTP 200), else 0."""
    try:
        req = urllib.request.Request(f"https://{url}")
        with urllib.request.urlopen(req, timeout=5) as response:
            return 1 if response.status == 200 else 0
    except Exception as e:
        print(f"Error getting availability for {url}: {e}")
        return 0

# Lambda entry point: checks URL health and publishes metrics
def lambda_handler(event, context):
    results = dict()
    metric_publisher = CloudWatchMetricPublisher()
    dimensions = [
        {'Name': 'URL', 'Value': constants.URL_TO_MONITOR}
    ]
    # Check availability
    availability = get_url_availability(constants.URL_TO_MONITOR)
    metric_publisher.put_metric_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_METRIC_NAME_AVAILABILITY, dimensions, availability)

    # Check latency
    latency = get_url_latency(constants.URL_TO_MONITOR)
    metric_publisher.put_metric_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_METRIC_NAME_LATENCY, dimensions, latency)

    results.update({"availability": availability, "latency": latency})
    return results