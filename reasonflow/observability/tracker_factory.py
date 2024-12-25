from typing import Dict, Any, Optional
from .basic_tracker import BasicTracker
from .reasontrack_adapter import ReasonTrackAdapter
from .tracking_interface import TrackingInterface

class TrackerFactory:
    @staticmethod
    def validate_config(tracker_type: str, config: Optional[Dict[str, Any]] = None) -> None:
        """Validate tracker configuration"""
        if tracker_type == "reasontrack":
            if not config:
                raise ValueError("ReasonTrack requires configuration")
            
            required_configs = {
                "event_backend": ["type", "config"],
                "metrics_backend": ["type", "config"],
                "alert_config": ["storage_path", "retention_days"],
                "state_config": ["storage_path"]
            }
            
            for section, fields in required_configs.items():
                if section not in config:
                    raise ValueError(f"Missing required section: {section}")
                for field in fields:
                    if field not in config[section]:
                        raise ValueError(f"Missing required field '{field}' in {section}")

    @staticmethod
    def create_tracker(tracker_type: str = "basic", config: Optional[Dict[str, Any]] = None) -> TrackingInterface:
        """Create appropriate tracker based on type with validation"""
        try:
            TrackerFactory.validate_config(tracker_type, config)
            
            if tracker_type == "basic":
                return BasicTracker()
            elif tracker_type == "reasontrack":
                return ReasonTrackAdapter(config or {})
            else:
                raise ValueError(f"Unknown tracker type: {tracker_type}")
                
        except Exception as e:
            print(f"Error creating tracker: {str(e)}")
            print("Falling back to basic tracker...")
            return BasicTracker() 