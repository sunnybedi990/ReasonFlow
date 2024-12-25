from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class TrackingInterface(ABC):
    @abstractmethod
    def track_workflow(self, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track workflow events"""
        pass
    
    @abstractmethod
    def track_task(self, task_id: str, workflow_id: str, event_type: str, data: Dict[str, Any]) -> None:
        """Track task events"""
        pass
    
    @abstractmethod
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status"""
        pass
    
    @abstractmethod
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get task status"""
        pass 