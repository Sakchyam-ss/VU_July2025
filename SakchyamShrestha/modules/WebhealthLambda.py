import boto3
import urllib.request
import time

#  URL=["skipq.org","bbc.com","aljazeera.com"]
URL = ["skipq.org", "bbc.com", "aljazeera.com", "cnn.com", "nytimes.com"]
NAMESPACE = "SakchyamProjectNameSpace"
availabilityMetric="AVAILABILITY_METRIC"
latencyMetric="LATENCY_METRIC"

def get_latency(url):
    try:
        start = time.time()
        req = urllib.request.Request(f"https://{url}")
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = time.time() - start
        return latency
    except Exception as e:
        print(f"Error getting latency for {url}: {e}")
        return 0

def get_availability(url):
    try:
        req = urllib.request.Request(f"https://{url}")
        with urllib.request.urlopen(req, timeout=5) as response:
            return 1 if response.status == 200 else 0
    except Exception as e:
        print(f"Error getting availability for {url}: {e}")
        return 0

def lambda_handler(event, context):
    client = boto3.client('cloudwatch')
    for url in URL:
        availability = get_availability(url)
        latency = get_latency(url)
        print(f"URL: {url}, Availability: {availability}, Latency: {latency}")
        # publish to cloudwatch
        client.put_metric_data(
            Namespace=NAMESPACE,
            MetricData=[
                {
                    'MetricName': availabilityMetric,
                    'Dimensions': [
                        {
                            'Name': 'url',
                            'Value': url
                        },
                    ],
                    'Value': availability,
                },
                {
                    'MetricName': latencyMetric,
                    'Dimensions': [
                        {
                            'Name': 'url',
                            'Value': url
                        },
                    ],
                    'Value': latency,
                }
            ]
        )





