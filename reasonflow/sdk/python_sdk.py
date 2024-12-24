from typing import Dict, Optional, List
import os
from ..orchestrator.workflow_engine import WorkflowEngine
from ..orchestrator.input_parser import InputParser
from ..agents.custom_agent_builder import CustomAgentBuilder
from ..persistence.document_management import DocumentManager


class ReasonFlowSDK:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the SDK with optional API key and components for workflows, agents, and documents.
        """
        self.api_key = api_key or os.getenv("REASONFLOW_API_KEY")
        self.engine = WorkflowEngine()
        self.parser = InputParser()
        self.agent_builder = CustomAgentBuilder()
        self.document_manager = DocumentManager()

    # Workflow Management
    def create_workflow(self, workflow_path: str) -> str:
        """
        Create a new workflow from a configuration file.
        """
        try:
            workflow_config = self.parser.parse_workflow(workflow_path)
            if not self.parser.validate_workflow(workflow_config):
                raise ValueError("Invalid workflow configuration")

            workflow_id = self.engine.add_workflow(workflow_config)
            print(f"Workflow created successfully with ID: {workflow_id}")
            return workflow_id
        except FileNotFoundError:
            print(f"Error: Workflow configuration file '{workflow_path}' not found.")
            return ""
        except Exception as e:
            print(f"Error creating workflow: {str(e)}")
            return ""

    def execute_workflow(self, workflow_id: str) -> Dict:
        """
        Execute a workflow by its ID.
        """
        try:
            results = self.engine.execute_workflow(workflow_id)
            print(f"Workflow executed successfully: {workflow_id}")
            return results
        except KeyError:
            print(f"Error: Workflow with ID '{workflow_id}' not found.")
            return {"error": "Workflow not found"}
        except Exception as e:
            print(f"Error executing workflow: {str(e)}")
            return {"error": str(e)}

    def list_workflows(self) -> Dict:
        """
        List all workflows and their statuses.
        """
        try:
            workflows = self.engine.list_workflows()
            return workflows
        except Exception as e:
            print(f"Error listing workflows: {str(e)}")
            return {"error": str(e)}

    def get_workflow_status(self, workflow_id: str) -> Dict:
        """
        Retrieve the status of a specific workflow.
        """
        try:
            status = self.engine.get_workflow_status(workflow_id)
            return status
        except KeyError:
            print(f"Error: Workflow with ID '{workflow_id}' not found.")
            return {"error": "Workflow not found"}
        except Exception as e:
            print(f"Error retrieving workflow status: {str(e)}")
            return {"error": str(e)}

    # Agent Management
    def create_agent(self, agent_type: str, config: Dict) -> str:
        """
        Create a new agent.
        :param agent_type: Type of the agent (e.g., "llm", "data_retrieval").
        :param config: Configuration for the agent.
        :return: Agent ID if successful.
        """
        try:
            agent = self.agent_builder.create_agent(agent_type, config)
            agent_id = id(agent)
            print(f"Agent created successfully with ID: {agent_id}")
            return str(agent_id)
        except Exception as e:
            print(f"Error creating agent: {str(e)}")
            return ""

    def list_agents(self) -> List[Dict]:
        """
        List all created agents.
        """
        try:
            return self.agent_builder.list_agents()
        except Exception as e:
            print(f"Error listing agents: {str(e)}")
            return []

    # Document Management
    def upload_document(self, file_path: str, metadata: Dict) -> str:
        """
        Upload a document to the system.
        :param file_path: Path to the document file.
        :param metadata: Metadata for the document.
        :return: Document ID if successful.
        """
        try:
            doc_id = self.document_manager.upload_document(file_path, metadata)
            print(f"Document uploaded successfully with ID: {doc_id}")
            return doc_id
        except FileNotFoundError:
            print(f"Error: Document file '{file_path}' not found.")
            return ""
        except Exception as e:
            print(f"Error uploading document: {str(e)}")
            return ""

    def search_documents(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for documents using a query.
        :param query: Search query.
        :param limit: Maximum number of results to return.
        :return: List of document results.
        """
        try:
            results = self.document_manager.search_documents(query, limit)
            print(f"Found {len(results)} document(s) for query: '{query}'")
            return results
        except Exception as e:
            print(f"Error searching documents: {str(e)}")
            return []
