from typing import Dict, Any, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from ..orchestrator.workflow_builder import WorkflowBuilder
from ..agents.custom_agent_builder import CustomAgentBuilder
from ..persistence.document_management import DocumentManager
from ..tasks.task_manager import TaskManager
import json

app = FastAPI()

workflow_builder = WorkflowBuilder()
agent_builder = CustomAgentBuilder()
doc_manager = DocumentManager()
task_manager = TaskManager()


class WorkflowConfig(BaseModel):
    tasks: Dict[str, Dict[str, Any]]
    dependencies: List[Dict[str, str]]


class AgentConfig(BaseModel):
    type: str
    name: str
    description: str
    config: Dict[str, Any]


@app.post("/workflows", summary="Create a new workflow")
async def create_workflow(config: WorkflowConfig):
    """
    Create a workflow with specified tasks and dependencies.
    """
    try:
        workflow_id = workflow_builder.create_workflow(config.dict())
        if not workflow_id:
            raise HTTPException(status_code=400, detail="Failed to create workflow")
        return {"workflow_id": workflow_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/workflows/{workflow_id}/execute", summary="Execute a workflow")
async def execute_workflow(workflow_id: str):
    """
    Execute the workflow specified by the workflow_id.
    """
    try:
        results = workflow_builder.execute_workflow(workflow_id)
        if "error" in results:
            raise HTTPException(status_code=500, detail=results["error"])
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{workflow_id}/status", summary="Get workflow status")
async def get_workflow_status(workflow_id: str):
    """
    Fetch the current status of a workflow by its ID.
    """
    try:
        status = workflow_builder.get_workflow_status(workflow_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agents", summary="Create a new agent")
async def create_agent(config: AgentConfig):
    """
    Create an agent with the specified configuration.
    """
    try:
        agent = agent_builder.create_agent(config.type, config.dict()["config"])
        return {"agent_id": id(agent)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agents", summary="List all agents")
async def list_agents():
    """
    List all active agents.
    """
    try:
        agents = agent_builder.list_agents()
        return {"agents": agents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/upload", summary="Upload a document")
async def upload_document(file: UploadFile = File(...), metadata: str = Form(...)):
    """
    Upload a document and its metadata to the document manager.
    """
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        doc_id = doc_manager.upload_document(temp_path, json.loads(metadata))
        return {"document_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/search", summary="Search documents")
async def search_documents(query: str, limit: int = 10):
    """
    Search for documents matching the query.
    """
    try:
        results = doc_manager.search_documents(query, limit)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks", summary="List all tasks")
async def list_tasks():
    """
    List all tasks managed by the TaskManager.
    """
    try:
        tasks = task_manager.list_all_tasks()
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}/status", summary="Get task status")
async def get_task_status(task_id: str):
    """
    Retrieve the status of a specific task by ID.
    """
    try:
        status = task_manager.get_task_status(task_id)
        if status == "not_found":
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task_id": task_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks/{task_id}/retry", summary="Retry a failed task")
async def retry_task(task_id: str):
    """
    Retry a failed task by its ID.
    """
    try:
        task_manager.retry_failed_tasks()
        return {"status": "retry initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
