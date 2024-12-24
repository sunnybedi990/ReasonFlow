import heapq
from typing import List, Dict, Any, Optional
from ..tasks.task import Task
from ..observability.tracker import TaskTracker
from reasonchain.memory import SharedMemory

class TaskManager:
    def __init__(self, shared_memory: Optional[SharedMemory] = None):
        self.tasks: Dict[str, Task] = {}
        self.task_queue = []  # Priority queue using heapq
        self.task_status = {}  # Dictionary to track task statuses
        self.waiting_tasks = []  # Tasks waiting for dependencies
        self.completed_tasks = []  # List of completed task names
        self.tracker = TaskTracker(shared_memory=shared_memory or SharedMemory())

    def is_empty(self) -> bool:
        """Check if there are no more tasks to process."""
        return len(self.tasks) == 0 or all(
            task.status in ["completed", "failed"] for task in self.tasks.values()
        )

    def add_task(self, task_dict: Dict) -> None:
        """Add a task to the manager."""
        try:
            task = Task(
                id=task_dict["id"],
                name=task_dict["name"],
                priority=task_dict.get("priority", 1),
                dependencies=task_dict.get("dependencies", []),
                status=task_dict.get("status", "pending"),
                metadata=task_dict.get("metadata", {})
            )
            self.tasks[task.id] = task
            self.task_status[task.id] = task.status
            if task.is_ready(self.completed_tasks):
                heapq.heappush(self.task_queue, (-task.priority, task))
            else:
                self.waiting_tasks.append(task)
        except Exception as e:
            print(f"Error adding task: {str(e)}")

    def get_next_task(self) -> Optional[Dict]:
        """Get the next task to execute."""
        self.resolve_dependencies()
        while self.task_queue:
            _, task = heapq.heappop(self.task_queue)
            if task.id in self.tasks and self.tasks[task.id].status == "pending":
                return {
                    "id": task.id,
                    "name": task.name,
                    "status": task.status,
                    "priority": task.priority
                }
        return None

    def update_task_status(self, task_id: str, status: str) -> None:
        """Update task status."""
        if task_id in self.tasks:
            self.tasks[task_id].status = status
            self.task_status[task_id] = status
            if status == "completed":
                self.completed_tasks.append(self.tasks[task_id].name)
            self.tracker.log(task_id, self.tasks[task_id].name, status)

    def resolve_dependencies(self):
        """Check waiting tasks and move ready tasks to the queue."""
        ready_tasks = [
            task for task in self.waiting_tasks if task.is_ready(self.completed_tasks)
        ]
        for task in ready_tasks:
            heapq.heappush(self.task_queue, (-task.priority, task))
            self.waiting_tasks.remove(task)

    def retry_failed_tasks(self):
        """Re-add failed tasks to the queue."""
        for task_id, status in list(self.task_status.items()):
            if status == "failed":
                task = self.tasks.get(task_id)
                if task:
                    task.status = "pending"  # Reset status
                    heapq.heappush(self.task_queue, (-task.priority, task))
                    print(f"Retrying task: {task}")
                    self.tracker.log(task.id, task.name, "pending")

    def list_all_tasks(self) -> List[Task]:
        """List all tasks."""
        return [task for _, task in self.task_queue]

    def validate_dependencies(self, workflow_config: Dict) -> bool:
        """Validate dependencies to ensure no circular or missing dependencies."""
        try:
            dependency_map = {dep["to"]: dep["from"] for dep in workflow_config["dependencies"]}
            visited = set()

            def check_cycle(task_id, stack):
                if task_id in stack:
                    raise ValueError(f"Circular dependency detected: {stack}")
                if task_id not in visited:
                    visited.add(task_id)
                    stack.append(task_id)
                    if task_id in dependency_map:
                        check_cycle(dependency_map[task_id], stack)
                    stack.pop()

            for task_id in workflow_config["tasks"]:
                check_cycle(task_id, [])
            return True
        except Exception as e:
            print(f"Dependency validation failed: {e}")
            return False

    def prioritize_and_validate(self):
        """Validate and prioritize tasks based on dependencies and priority."""
        self.resolve_dependencies()
        # Re-prioritize tasks in the queue
        self.task_queue = sorted(self.task_queue, key=lambda x: (-x[1].priority, x[1].id))
        heapq.heapify(self.task_queue)

    def list_completed_tasks(self) -> List[str]:
        """List all completed task names."""
        return self.completed_tasks


# import heapq
# from typing import List, Dict, Any, Optional
# from ..tasks.task import Task
# from ..observability.tracker import TaskTracker
# from reasonchain.memory import SharedMemory
# class TaskManager:
#     def __init__(self, shared_memory: Optional[SharedMemory] = None):
#         self.tasks: Dict[str, Task] = {}
#         self.task_queue = []  # Priority queue using heapq
#         self.task_status = {}  # Dictionary to track task statuses
#         self.waiting_tasks = []  # Tasks waiting for dependencies
#         self.completed_tasks = []  # List of completed task names
#         self.tracker = TaskTracker(shared_memory=shared_memory or SharedMemory())

#     def is_empty(self) -> bool:
#         """Check if there are no more tasks to process."""
#         return len(self.tasks) == 0 or all(task.status in ["completed", "failed"] for task in self.tasks.values())

#     def add_task(self, task_dict: Dict) -> None:
#         """Add a task to the manager."""
#         try:
#             task = Task(
#                 id=task_dict["id"],
#                 name=task_dict["name"],
#                 priority=task_dict.get("priority", 1),
#                 dependencies=task_dict.get("dependencies", []),
#                 status=task_dict.get("status", "pending"),
#                 metadata=task_dict.get("metadata", {})
#             )
#             self.tasks[task.id] = task
#             self.task_status[task.id] = task.status
#             if task.is_ready(self.completed_tasks):
#                 heapq.heappush(self.task_queue, (-task.priority, task))
#             else:
#                 self.waiting_tasks.append(task)
#         except Exception as e:
#             print(f"Error adding task: {str(e)}")

#     def get_next_task(self) -> Optional[Dict]:
#         """Get the next task to execute."""
#         self.resolve_dependencies()
#         while self.task_queue:
#             _, task = heapq.heappop(self.task_queue)
#             if task.id in self.tasks and self.tasks[task.id].status == "pending":
#                 return {
#                     "id": task.id,
#                     "name": task.name,
#                     "status": task.status,
#                     "priority": task.priority
#                 }
#         return None

#     def update_task_status(self, task_id: str, status: str) -> None:
#         """Update task status."""
#         if task_id in self.tasks:
#             self.tasks[task_id].status = status
#             self.task_status[task_id] = status
#             if status == "completed":
#                 self.completed_tasks.append(self.tasks[task_id].name)
#             self.tracker.log(task_id, self.tasks[task_id].name, status)

#     def resolve_dependencies(self):
#         """Check waiting tasks and move ready tasks to the queue."""
#         for task in self.waiting_tasks[:]:
#             if task.is_ready(self.completed_tasks):
#                 self.add_task(task)
#                 self.waiting_tasks.remove(task)

#     def retry_failed_tasks(self):
#         """Re-add failed tasks to the queue."""
#         for task_id, status in list(self.task_status.items()):
#             if status == "failed":
#                 task = next((t[1] for t in self.task_queue if t[1].id == task_id), None)
#                 if task:
#                     self.add_task(task)
#                     print(f"Retrying task: {task}")
#                     self.tracker.log(task.id, task.name, "pending")
#     def list_all_tasks(self) -> List[Task]:
#         """List all tasks."""
#         return [task for _, task in self.task_queue]
    
#     def validate_dependencies(self, workflow_config: Dict) -> bool:
#         """Validate dependencies to ensure no circular or missing dependencies."""
#         try:
#             dependency_map = {dep["to"]: dep["from"] for dep in workflow_config["dependencies"]}
#             visited = set()

#             def check_cycle(task_id, stack):
#                 if task_id in stack:
#                     raise ValueError(f"Circular dependency detected: {stack}")
#                 if task_id not in visited:
#                     visited.add(task_id)
#                     stack.append(task_id)
#                     if task_id in dependency_map:
#                         check_cycle(dependency_map[task_id], stack)
#                     stack.pop()

#             for task_id in workflow_config["tasks"]:
#                 check_cycle(task_id, [])
#             return True
#         except Exception as e:
#             print(f"Dependency validation failed: {e}")
#             return False


# if __name__ == "__main__":
#     # Initialize TaskManager
#     task_manager = TaskManager()

#     # Define tasks
#     task1 = Task(name="Task1", priority=10, metadata={"type": "data_processing"})
#     task2 = Task(name="Task2", priority=5, dependencies=["Task1"], metadata={"type": "analysis"})
#     task3 = Task(name="Task3", priority=7, dependencies=["Task1", "Task2"], metadata={"type": "reporting"})

#     # Add tasks
#     task_manager.add_task(task1)
#     task_manager.add_task(task2)
#     task_manager.add_task(task3)

#     # Process tasks
#     while (task := task_manager.get_next_task()) is not None:
#         print(f"Executing: {task}")
#         task_manager.update_task_status(task.id, "completed")

#     # Retry any failed tasks
#     task_manager.retry_failed_tasks()
