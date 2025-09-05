# Project Dashboard

## Project Overview

**Project Name:** Sakchyam Web Health Monitoring Stack  
**Course:** NIT6150  
**Description:**  
A serverless AWS solution that monitors the health (availability and latency) of a specified website, visualizes metrics, and logs alarms for further analysis.

---

## Current Status

- ✅ Lambda health check deployed
- ✅ Custom CloudWatch metrics and alarms set up
- ✅ SNS notifications and DynamoDB logging integrated
- ✅ CloudWatch Dashboard created
- 🟢 Project documentation complete

---

## Key Features & Deliverables

| Feature                | Status   | Description                                      |
|------------------------|----------|--------------------------------------------------|
| Lambda Health Check    | Complete | Periodic URL health checks                       |
| CloudWatch Metrics     | Complete | Custom metrics for availability & latency        |
| CloudWatch Alarms      | Complete | Alerts for threshold breaches                    |
| SNS Notifications      | Complete | Email & Lambda triggers on alarm                 |
| DynamoDB Logging       | Complete | Alarm events stored for auditing                 |
| Dashboard Visualization| Complete | CloudWatch Dashboard for real-time monitoring    |

---

## Metrics & Monitoring

- **Availability:** Percentage of successful health checks
- **Latency:** Response time of the monitored URL
- **Alarms:** Triggered when thresholds are crossed

*See CloudWatch Dashboard (`URLMonitorDashboard`) for live graphs and alarm status.*

---

## Screenshots

> _Add screenshots of your CloudWatch Dashboard and any relevant AWS resources here for visual reference._

---

## Next Steps / Open Issues

- [ ] Add more URLs for multi-site monitoring (optional)
- [ ] Enhance alerting (e.g., Slack integration)
- [ ] Cost optimization review

---

## Quick Links

- [Project Repository](<your-repo-url>)
- [CloudWatch Dashboard](https://console.aws.amazon.com/cloudwatch/home#dashboards:name=URLMonitorDashboard)
- [DynamoDB Table](https://console.aws.amazon.com/dynamodb/home#tables:selected=WebHealthTableV2)

---

_Last updated: 2025-09-