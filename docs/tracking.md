# ReasonFlow Tracking System

## Overview
ReasonFlow provides two levels of tracking capabilities:
1. Basic Tracking (Default)
2. Advanced Tracking (via ReasonTrack integration)

## Basic Tracking
Built-in tracking system that provides essential workflow and task monitoring:

### Features
- Task status tracking
- Workflow state persistence
- Basic error logging
- JSON-based storage
- Memory-efficient operation

### Usage
```python
from reasonflow import WorkflowEngine

# Uses basic tracking by default
engine = WorkflowEngine()
```

### Storage Location
Basic tracking stores workflow states in `workflow_states/` directory:
- Each workflow gets a unique JSON file
- Format: `workflow_states/<workflow_id>.json`

## Advanced Tracking (ReasonTrack)
Enterprise-grade tracking system with advanced monitoring capabilities:

### Features
- Real-time event streaming
- Metrics collection
- Advanced analytics
- Distributed tracing
- Alert management
- Multi-backend support

### Prerequisites
```bash
pip install reasontrack
```

### Usage
```python
from reasonflow import WorkflowEngine

# Configure advanced tracking
engine = WorkflowEngine(
    tracker_type="reasontrack",
    tracker_config={
        "event_backend": "kafka",
        "metrics_backend": "prometheus",
        "storage_backend": "elasticsearch"
    }
)
```

### Supported Backends
- Events: Kafka, Redis, OpenTelemetry
- Metrics: Prometheus, StatsD
- Storage: Elasticsearch, MongoDB
- Alerts: Email, Slack, Custom Webhooks

## Comparison

| Feature                    | Basic Tracking | Advanced Tracking |
|---------------------------|----------------|------------------|
| Task Status               | ✅             | ✅               |
| Workflow State            | ✅             | ✅               |
| Error Logging             | ✅             | ✅               |
| Real-time Events          | ❌             | ✅               |
| Metrics Collection        | ❌             | ✅               |
| Distributed Tracing       | ❌             | ✅               |
| Alert Management          | ❌             | ✅               |
| Multi-backend Support     | ❌             | ✅               |
| Resource Requirements     | Low            | Medium-High      |
| Setup Complexity         | Simple         | Advanced         |

## Configuration Examples

### Basic Tracking
```python
engine = WorkflowEngine()  # No configuration needed
```

### Advanced Tracking with Kafka
```python
config = {
    "event_backend": "kafka",
    "kafka_config": {
        "bootstrap_servers": "localhost:9092",
        "topic_prefix": "reasonflow_"
    }
}
engine = WorkflowEngine(tracker_type="reasontrack", tracker_config=config)
```

### Advanced Tracking with Prometheus
```python
config = {
    "metrics_backend": "prometheus",
    "prometheus_config": {
        "pushgateway_url": "localhost:9091",
        "job_name": "reasonflow"
    }
}
engine = WorkflowEngine(tracker_type="reasontrack", tracker_config=config)
``` 