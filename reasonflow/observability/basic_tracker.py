from .tracking_interface import TrackingInterface
from .tracker import TaskTracker
from ..orchestrator.state_manager import StateManager
from reasonchain.memory import SharedMemory
from typing import Dict, Any
from datetime import datetime

class BasicTracker(TrackingInterface):
    def __init__(self):
        self.shared_memory = SharedMemory()
        self.task_tracker = TaskTracker(shared_memory=self.shared_memory)
        self.state_manager = StateManager()
    
    def track_workflow(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Use existing state management for workflows"""
        print(f"Tracking workflow {workflow_id}: {event_type}")
        state = self.state_manager.load_state(workflow_id) or {}
        state.update({
            "status": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        self.state_manager.save_state(workflow_id, state)
    
    def track_task(self, task_id: str, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Use existing task tracker"""
        self.task_tracker.log(task_id, data.get("name", ""), event_type)

    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status from state manager"""
        state = self.state_manager.load_state(workflow_id) or {}
        return {
            "status": state.get("status", "unknown"),
            "data": state.get("data", {}),
            "timestamp": state.get("timestamp")
        }

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status from task tracker"""
        logs = self.task_tracker.get_logs()
        task_logs = [log for log in logs if log["task_id"] == task_id]
        return {
            "status": task_logs[-1]["status"] if task_logs else "unknown",
            "history": task_logs,
            "last_update": task_logs[-1]["timestamp"] if task_logs else None
        } 