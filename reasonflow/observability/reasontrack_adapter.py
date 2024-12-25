from typing import Dict, Any, Optional, Callable
from datetime import datetime
from .tracking_interface import TrackingInterface

class EventType:
    """Event types for workflow and task tracking"""
    WORKFLOW_START = "workflow_start"
    WORKFLOW_COMPLETE = "workflow_complete"
    WORKFLOW_FAIL = "workflow_fail"
    WORKFLOW_PAUSE = "workflow_pause"
    WORKFLOW_RESUME = "workflow_resume"
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    TASK_FAIL = "task_fail"
    TASK_RETRY = "task_retry"
    TASK_SKIP = "task_skip"

class ReasonTrackAdapter(TrackingInterface):
    def __init__(self, config: Dict[str, Any]):
        try:
            from reasontrack import ReasonTrack
            self.tracker = ReasonTrack(**config)
        except ImportError:
            raise ImportError("ReasonTrack is not installed. Install it with: pip install reasontrack")

    def track_workflow(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track workflow events with enhanced metadata"""
        event_type_map = {
            "started": EventType.WORKFLOW_START,
            "completed": EventType.WORKFLOW_COMPLETE,
            "failed": EventType.WORKFLOW_FAIL,
            "paused": EventType.WORKFLOW_PAUSE,
            "resumed": EventType.WORKFLOW_RESUME
        }
        
        self.tracker.track_event(
            type=event_type_map.get(event_type, event_type),
            name=f"workflow_{workflow_id}",
            metadata={
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                **data
            }
        )

    def track_task(self, task_id: str, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track task events with metrics collection"""
        event_type_map = {
            "started": EventType.TASK_START,
            "completed": EventType.TASK_COMPLETE,
            "failed": EventType.TASK_FAIL,
            "retrying": EventType.TASK_RETRY,
            "skipped": EventType.TASK_SKIP
        }
        
        self.tracker.track_event(
            type=event_type_map.get(event_type, event_type),
            name=f"task_{task_id}",
            metadata={
                "task_id": task_id,
                "workflow_id": workflow_id,
                "timestamp": datetime.now().isoformat(),
                **data
            }
        )
        
        # Collect metrics if task completed
        if event_type == "completed":
            self.record_task_metrics(task_id, workflow_id, data)

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get comprehensive workflow status"""
        return {
            "metrics": self.tracker.get_workflow_metrics(workflow_id),
            "events": self.tracker.get_workflow_events(workflow_id),
            "state": self.tracker.get_workflow_state(workflow_id)
        }

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get detailed task status and metrics"""
        return {
            "metrics": self.get_task_metrics(task_id),
            "events": self.tracker.get_task_events(task_id)
        }

    def get_task_metrics(self, task_id: str) -> Dict[str, Any]:
        """Get comprehensive task metrics"""
        return {
            "duration": self.tracker.get_metric("task_duration", task_id),
            "memory_usage": self.tracker.get_metric("task_memory_usage", task_id),
            "cpu_usage": self.tracker.get_metric("task_cpu_usage", task_id),
            "error_rate": self.tracker.get_metric("task_error_rate", task_id),
            "retry_count": self.tracker.get_metric("task_retry_count", task_id)
        }

    def record_task_metrics(self, task_id: str, workflow_id: str, data: Dict[str, Any]) -> None:
        """Record detailed task metrics"""
        metrics = {
            "task_duration": data.get("duration", 0),
            "task_memory_usage": data.get("memory_usage", 0),
            "task_cpu_usage": data.get("cpu_usage", 0),
            "task_error_rate": 0 if data.get("status") == "success" else 1,
            "task_retry_count": data.get("retries", 0)
        }
        
        for metric_name, value in metrics.items():
            self.tracker.record_metric(
                name=metric_name,
                value=value,
                labels={
                    "task_id": task_id,
                    "workflow_id": workflow_id
                }
            ) 