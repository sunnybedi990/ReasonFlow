import time
from collections import defaultdict
class Metrics:
    def __init__(self, shared_memory: None):
        # Dictionary to store metrics
        self.task_metrics = defaultdict(lambda: {"execution_count": 0, "total_duration": 0.0, "success_count": 0, "failure_count": 0})
        self.workflow_metrics = defaultdict(lambda: {"execution_count": 0, "total_duration": 0.0, "success_count": 0, "failure_count": 0})
        self.shared_memory = shared_memory

    def start_timer(self):
        """
        Start a timer for tracking task or workflow duration.
        :return: Start time in seconds.
        """
        return time.time()

    def end_timer(self, start_time):
        """
        End the timer and calculate the duration.
        :param start_time: Start time in seconds.
        :return: Duration in seconds.
        """
        return time.time() - start_time

    def record_task_metrics(self, task_name, duration, success=True):
        """
        Record metrics for a task.
        :param task_name: Name of the task.
        :param duration: Duration of the task in seconds.
        :param success: Whether the task was successful.
        """
        metrics = self.task_metrics[task_name]
        metrics["execution_count"] += 1
        metrics["total_duration"] += duration
        if success:
            metrics["success_count"] += 1
        else:
            metrics["failure_count"] += 1
         # Save to shared memory
        if self.shared_memory:
            self.shared_memory.store(f"metrics_{task_name}", metrics)

    def record_workflow_metrics(self, workflow_name, duration, success=True):
        """
        Record metrics for a workflow.
        :param workflow_name: Name of the workflow.
        :param duration: Duration of the workflow in seconds.
        :param success: Whether the workflow was successful.
        """
        metrics = self.workflow_metrics[workflow_name]
        metrics["execution_count"] += 1
        metrics["total_duration"] += duration
        if success:
            metrics["success_count"] += 1
        else:
            metrics["failure_count"] += 1
        # Save to shared memory
        if self.shared_memory:
            self.shared_memory.store(f"metrics_{workflow_name}", metrics)

    def get_task_metrics(self, task_name):
        """
        Get metrics for a specific task.
        :param task_name: Name of the task.
        :return: Dictionary with task metrics.
        """
        return self.task_metrics.get(task_name, {})

    def get_workflow_metrics(self, workflow_name):
        """
        Get metrics for a specific workflow.
        :param workflow_name: Name of the workflow.
        :return: Dictionary with workflow metrics.
        """
        return self.workflow_metrics.get(workflow_name, {})

    def summarize_metrics(self):
        """
        Summarize all metrics for tasks and workflows.
        :return: Dictionary with summarized metrics.
        """
        return {
            "task_metrics": dict(self.task_metrics),
            "workflow_metrics": dict(self.workflow_metrics),
        }
