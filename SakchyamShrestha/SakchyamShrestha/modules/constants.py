# modules/constants.py
import os

URL_TO_MONITOR = os.getenv("URL_TO_MONITOR", "www.bbc.com/")
URL_MONITOR_NAMESPACE = os.getenv("URL_MONITOR_NAMESPACE", "SakchyamProjectNameSpace")
URL_MONITOR_METRIC_NAME_AVAILABILITY = "url_availability"
URL_MONITOR_METRIC_NAME_LATENCY = "url_latency"
