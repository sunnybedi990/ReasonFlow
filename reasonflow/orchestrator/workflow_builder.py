from typing import Dict, Any, Optional
import uuid
from reasonflow.orchestrator.workflow_engine import WorkflowEngine
from reasonflow.orchestrator.state_manager import StateManager
from reasonflow.orchestrator.input_parser import InputParser
from reasonflow.tasks.task_manager import TaskManager
from reasonchain.memory import SharedMemory
import os
import numpy as np

class WorkflowBuilder:
    def __init__(self, task_manager: Optional[TaskManager] = None):
        self.engine = WorkflowEngine(task_manager=task_manager)
        self.state_manager = StateManager()
        self.parser = InputParser()
        self.task_manager = task_manager or TaskManager()
        self.shared_memory = SharedMemory()


    def create_workflow(self, config: Dict[str, Any]) -> str:
        """Create a new workflow from configuration."""
        try:
            workflow_id = str(uuid.uuid4())
            serializable_config = self._make_config_serializable(config)

            if not self.parser.validate_workflow(serializable_config):
                raise ValueError("Invalid workflow configuration")

            # Add tasks to the workflow engine
            for task_id, task_config in serializable_config["tasks"].items():
                self.engine.add_task(task_id, task_config["type"], task_config.get("config", {}))
                self.task_manager.add_task({
                    "id": task_id,
                    "name": task_config.get("name", task_id),
                    "dependencies": task_config.get("dependencies", []),
                    "status": "pending",
                    "priority": task_config.get("priority", 1),
                })

            # Add dependencies to the workflow engine
            for dep in serializable_config["dependencies"]:
                self.engine.add_dependency(dep["from"], dep["to"])

            # Save initial state
            self.state_manager.save_state(workflow_id, {"status": "created", "config": serializable_config})
            return workflow_id
        except Exception as e:
            print(f"Error creating workflow: {e}")
            return ""


    def _make_config_serializable(self, config: Dict) -> Dict:
        """
        Convert config to a JSON-serializable format while preserving critical data.
        """
        serializable = {}
        for key, value in config.items():
            if isinstance(value, dict):
                # Recursively serialize nested dictionaries
                serializable[key] = self._make_config_serializable(value)
            elif isinstance(value, list):
                # Serialize lists
                serializable[key] = [
                    self._make_config_serializable(v) if isinstance(v, dict) else self._serialize_value(v)
                    for v in value
                ]
            elif key == "agent":
                # Keep the agent object as is for specific processing elsewhere
                serializable[key] = value
            else:
                # General serialization for other values
                serializable[key] = self._serialize_value(value)
        return serializable

    def _serialize_value(self, value: Any) -> Any:
        """
        Helper method to serialize individual values.
        """
        try:
            if hasattr(value, '__dict__'):
                # Convert objects with __dict__ attribute to their string representation
                return str(value)
            elif isinstance(value, (int, float, str, bool, type(None))):
                # Basic JSON-serializable types
                return value
            elif isinstance(value, (np.ndarray, list, tuple, set)):
                # Convert collections to lists
                return list(value)
            elif isinstance(value, (np.floating, np.integer)):
                # Convert numpy types to native Python types
                return value.item()
            else:
                # Fallback: convert to string
                return str(value)
        except Exception as e:
            # Handle serialization errors gracefully
            return f"// Serialization Error: {str(e)}"

    # def execute_workflow(self, workflow_id: str) -> Dict:
    #     """Execute a workflow by ID."""
    #     try:
    #         # Load workflow state
    #         state = self.state_manager.load_state(workflow_id)
    #         if not state:
    #             raise ValueError(f"Workflow {workflow_id} not found")

    #         # Update status to running
    #         state["status"] = "running"
    #         self.state_manager.save_state(workflow_id, state)

    #         # Execute workflow tasks in the order of dependencies
    #         results = {}
    #         while not self.task_manager.is_empty():
    #             task = self.task_manager.get_next_task()
    #             if task and task["status"] == "pending":
    #                 task_id = task["id"]
    #                 node_data = self.engine.workflow_graph.nodes[task_id]
    #                 agent_type = node_data["agent_type"]
    #                 config = node_data["config"]

    #                 result = self.engine._execute_task(task_id, agent_type, config)
    #                 results[task_id] = result

    #                 # Update task status in TaskManager
    #                 if result.get("status") == "success":
    #                     self.task_manager.update_task_status(task_id, "completed")
    #                 else:
    #                     self.task_manager.update_task_status(task_id, "failed")

    #         # Update final state
    #         state["status"] = "completed"
    #         state["results"] = results
    #         self.state_manager.save_state(workflow_id, state)

    #         return results

    #     except Exception as e:
    #         error_state = {"status": "failed", "error": str(e)}
    #         self.state_manager.save_state(workflow_id, error_state)
    #         self.shared_memory.add_entry("workflow_execution_error", str(e))
    #         return {"error": str(e)}

    # def execute_workflow(self, workflow_id: str) -> Dict:
    #     """Execute a workflow by ID with progress tracking."""
    #     try:
    #         state = self.state_manager.load_state(workflow_id)
    #         if not state:
    #             raise ValueError(f"Workflow {workflow_id} not found")

    #         state["status"] = "running"
    #         self.state_manager.save_state(workflow_id, state)

    #         results = {}
    #         total_tasks = len(self.engine.workflow_graph.nodes)
    #         completed_tasks = 0

    #         while not self.task_manager.is_empty():
    #             task = self.task_manager.get_next_task()
    #             if task and task["status"] == "pending":
    #                 task_id = task["id"]
    #                 result = self.execute_with_retries(
    #                     task_id, 
    #                     self.engine.workflow_graph.nodes[task_id]["agent_type"], 
    #                     self.engine.workflow_graph.nodes[task_id]["config"]
    #                 )
    #                 results[task_id] = result
    #                 completed_tasks += 1
    #                 progress = (completed_tasks / total_tasks) * 100
    #                 print(f"Progress: {progress:.2f}%")

    #                 if result.get("status") == "success":
    #                     self.task_manager.update_task_status(task_id, "completed")
    #                 else:
    #                     self.task_manager.update_task_status(task_id, "failed")

    #         state["status"] = "completed"
    #         state["results"] = results
    #         self.state_manager.save_state(workflow_id, state)
    #         return results
    #     except Exception as e:
    #         error_state = {"status": "failed", "error": str(e)}
    #         self.state_manager.save_state(workflow_id, error_state)
    #         return {"error": str(e)}

    def execute_workflow(self, workflow_id: str) -> Dict:
        """Execute a workflow by ID."""
        try:
            # Load workflow state
            state = self.state_manager.load_state(workflow_id)
            if not state:
                raise ValueError(f"Workflow {workflow_id} not found")

            # Update status to running
            state["status"] = "running"
            self.state_manager.save_state(workflow_id, state)

            # Execute tasks in topological order
            results = self.engine.execute_workflow()

            # Update state after execution
            state["status"] = "completed"
            state["results"] = results
            self.state_manager.save_state(workflow_id, state)

            return results
        except Exception as e:
            error_state = {"status": "failed", "error": str(e)}
            self.state_manager.save_state(workflow_id, error_state)
            return {"error": str(e)}



    def stop_workflow(self, workflow_id: str) -> bool:
        """Stop a running workflow."""
        try:
            state = self.state_manager.load_state(workflow_id)
            if not state:
                raise ValueError(f"Workflow {workflow_id} not found")

            if state["status"] == "running":
                state["status"] = "stopped"
                self.state_manager.save_state(workflow_id, state)
                return True
            return False

        except Exception as e:
            self.shared_memory.add_entry("workflow_stop_error", str(e))
            return False

    def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow and its state."""
        try:
            state = self.state_manager.load_state(workflow_id)
            if not state:
                return False

            # Remove workflow state
            os.remove(f"{self.state_manager.storage_path}/{workflow_id}.json")
            return True

        except Exception as e:
            self.shared_memory.add_entry("workflow_delete_error", str(e))
            return False

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """Get current status of a workflow."""
        try:
            state = self.state_manager.load_state(workflow_id)
            if not state:
                raise ValueError(f"Workflow {workflow_id} not found")
            return {
                "workflow_id": workflow_id,
                "status": state.get("status", "unknown"),
                "created_at": state.get("created_at"),
                "results": state.get("results"),
            }
        except Exception as e:
            self.shared_memory.add_entry("workflow_status_error", str(e))
            return {"error": str(e)}
        
    def validate_and_repair_state(self, workflow_id: str) -> bool:
        """Validate and repair a workflow state if necessary."""
        try:
            state = self.load_state(workflow_id)
            if not state:
                raise ValueError("State not found")

            # Check for required fields
            required_keys = ["status", "config"]
            for key in required_keys:
                if key not in state:
                    print(f"Missing key: {key}. Attempting repair...")
                    state[key] = "unknown" if key == "status" else {}

            # Save repaired state
            self.save_state(workflow_id, state)
            return True
        except Exception as e:
            print(f"Error validating or repairing state: {e}")
            return False
    
    def finalize_workflow(self, workflow_id: str):
        """Perform cleanup operations after workflow execution."""
        try:
            self.shared_memory.clear()  # Clear shared memory
            self.task_manager.clear_tasks()  # Clear task queue
            print(f"Workflow {workflow_id} finalized.")
        except Exception as e:
            print(f"Error finalizing workflow {workflow_id}: {e}")
    
    def execute_with_retries(self, task_id: str, agent_type: str, config: Dict, retries: int = 3) -> Dict:
        """Execute a task with retry logic."""
        for attempt in range(retries):
            try:
                result = self.engine._execute_task(task_id, agent_type, config)
                if result.get("status") == "success":
                    return result
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for task {task_id}: {e}")
        return {"status": "failed", "error": f"Task {task_id} failed after {retries} retries"}



