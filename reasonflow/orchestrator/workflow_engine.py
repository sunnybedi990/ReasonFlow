import os
from typing import Dict, List, Optional
import networkx as nx
from reasonchain.memory import SharedMemory
from reasonflow.agents.custom_agent_builder import CustomAgentBuilder
from reasonflow.tasks.task_manager import TaskManager
import re

class WorkflowEngine:
    def __init__(self, task_manager: Optional[TaskManager] = None):
        self.workflow_graph = nx.DiGraph()
        self.current_state = {}
        self.shared_memory = SharedMemory()
        self.agent_builder = CustomAgentBuilder()
        self.task_manager = task_manager or TaskManager(shared_memory=self.shared_memory)
        self.task_results = {}

    def add_task(self, task_id: str, agent_type: str, config: Dict) -> None:
        try:
            self.workflow_graph.add_node(task_id, agent_type=agent_type, config=config)
        except Exception as e:
            print(f"Error adding task: {str(e)}")
            
    def add_dependency(self, from_task: str, to_task: str) -> None:
        try:
            self.workflow_graph.add_edge(from_task, to_task)
        except Exception as e:
            print(f"Error adding dependency: {str(e)}")
            
    def _format_task_output(self, task_id: str, output: Dict) -> str:
        """Format task output for use in prompts."""
        if output.get("status") == "success":
            return output.get("output", "")
        return f"Error in task {task_id}: {output.get('message', 'Unknown error')}"

    def _execute_task(self, task_id: str, agent_type: str, config: Dict) -> Dict:
        """
        Execute a task using its agent type and configuration.
        """
        try:
            # Resolve placeholders in config before execution
            #print("Before Resolving config",config)
            config = self._resolve_placeholders(task_id, config)
            #print(f"Resolved config for task {task_id}: {config}")
            # Create and execute the agent
            agent = self.agent_builder.create_agent(agent_type, config)
            if not agent:
                raise ValueError(f"Failed to initialize agent for task {task_id}")

            result = agent.execute(**config.get("params", {}))

            # Store task result for future use
            self.task_results[task_id] = result
            return result
        except Exception as e:
            error_msg = f"Error executing task {task_id}: {str(e)}"
            self.shared_memory.add_entry(f"{task_id}_error", error_msg)
            return {"status": "error", "message": error_msg}
            
    def _resolve_placeholders(self, task_id: str, config: Dict) -> Dict:
        """
        Resolve placeholders in task parameters using the outputs of preceding tasks.
        """
        #print(f"Resolving placeholders for task {task_id}")
        #print(f"Params before resolution: {config.get('params', {})}")
        #print(f"Available task results: {self.task_results}")

        params = config.get("params", {})
        for key, value in params.items():
            if not isinstance(value, str):
                print(f"Skipping placeholder resolution for key '{key}': Value is not a string")
                continue

            #print(f"Processing key '{key}' with value: {value}")
            for match in re.finditer(r'\{\{([\w\-\.]+)\.([\w\-\.]+)\}\}', value):
                ref_task_id, field = match.groups()
                #print(f"Found placeholder: ref_task_id={ref_task_id}, field={field}")
                
                if ref_task_id in self.task_results:
                    if field in self.task_results[ref_task_id]:
                        field_value = self.task_results[ref_task_id][field]
                 #       print(f"Resolving placeholder '{{{{{ref_task_id}.{field}}}}}' with value: {field_value}")
                        params[key] = value.replace(match.group(0), str(field_value))
                    else:
                        #print(f"Warning: Field '{field}' not found in results of task {ref_task_id}")
                        params[key] = value.replace(match.group(0), "[UNRESOLVED]")
                else:
                    #print(f"Warning: Task ID '{ref_task_id}' not found in task results")
                    params[key] = value.replace(match.group(0), "[UNRESOLVED]")

        #print(f"Params after resolution: {params}")
        config["params"] = params
        return config



    def execute_workflow(self) -> Dict:
        execution_order = list(nx.topological_sort(self.workflow_graph))
        print(f"Execution order: {execution_order}")  # Debugging the task order

        results = {}

        for task_id in execution_order:
            node_data = self.workflow_graph.nodes[task_id]
            agent_type = node_data['agent_type']
            config = node_data['config']
            result = self._execute_task(task_id, agent_type, config)
            results[task_id] = result
            if isinstance(self.shared_memory, SharedMemory):
                self.shared_memory.add_entry(task_id, result)

        return results

