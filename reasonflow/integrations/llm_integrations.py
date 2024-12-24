import os
import logging
from typing import Dict, Optional


class LLMIntegration:
    SUPPORTED_PROVIDERS = {
        "openai": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini"],
        "groq": [
        "gemma-7b-it",
        "gemma2-9b-it",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-guard-3-8b",
        "llama3-70b-8192",
        "llama3-8b-8192",
        "llama3-groq-70b-8192-tool-use-preview",
        "llama3-groq-8b-8192-tool-use-preview",
        "llava-v1.5-7b-4096-preview",
        "mixtral-8x7b-32768"
    ],
    "ollama": [
        "llama3.1:latest",
        "Llama 3.1 - 8B",
        "Llama 3.1 - 70B",
        "Gemma 2 - 2B",
        "Gemma 2 - 9B",
        "Mistral-Nemo - 12B",
        "Mistral Large 2 - 123B",
        "Qwen 2 - 0.5B",
        "Qwen 2 - 72B",
        "DeepSeek-Coder V2 - 16B",
        "Phi-3 - 3B",
        "Phi-3 - 14B"
    ],
        "anthropic": ["claude-v1", "claude-v2"],
        "reasonchain": ["reason-llm-v1"]
    }
    
    def __init__(self, provider: str, model: str, api_key: Optional[str] = None):
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider. Use one of {list(self.SUPPORTED_PROVIDERS.keys())}")
        
        if model not in self.SUPPORTED_PROVIDERS[provider]:
            raise ValueError(f"Unsupported model for {provider}. Supported models: {self.SUPPORTED_PROVIDERS[provider]}")
            
        self.provider = provider
        self.model = model
        if provider == "ollama":
            self.api_key = None
        else:
            self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
            if not self.api_key:
                raise ValueError(f"API key for {provider} is missing. Please provide it or set it in the environment.")
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"{self.provider}-{self.model}")
        
    def execute(self, prompt: str, **kwargs) -> Dict:
        """Generate a response using the specified provider and model."""
        try:
            response = self._generate_response(prompt, **kwargs)
            return {
                "status": "success",
                "output": response,
                "metadata": {
                    "provider": self.provider,
                    "model": self.model
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "metadata": {
                    "provider": self.provider,
                    "model": self.model
                }
            }
    
    def _generate_response(self, prompt: str, model: Optional[str] = None, **kwargs) -> str:
        """Generate a response using the appropriate provider."""
        self.logger.info(f"Generating response with provider '{self.provider}' and model '{self.model}' for prompt: {prompt}")
        
        try:
            if self.provider == "openai":
                return self._generate_with_openai(prompt, model, **kwargs)
            if self.provider == "ollama":
                return self._generate_with_ollama(prompt, model, **kwargs)
            if self.provider == "groq":
                return self._generate_with_groq(prompt, model, **kwargs)
            if self.provider == "anthropic":
                return self._anthropic_generate(prompt, model, **kwargs)
            if self.provider == "reasonchain":
                return self._reasonchain_generate(prompt, model, **kwargs)
            
            raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            self.logger.error(f"Error in LLM generation: {e}")
            raise e

    def _generate_with_openai(self, prompt, model= None, **kwargs):
        """
        Generate a response using OpenAI API.
        :param prompt: Text prompt.
        :param model: OpenAI model to use.
        :return: Generated response.
        """
        import openai
        model = model or self.model
        openai_client = openai.OpenAI(api_key=self.api_key)

        try:
            # Add 'query' to the prompt if provided
            if 'query' in kwargs:
                prompt = f"{prompt}\n\nQuery Context: {kwargs['query']}"
        
            response = openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            message = response.choices[0].message.content.strip()
            formatted_response = {
                "status": "success",
                "content": message,
                "metadata": {
                    "provider": "openai",
                    "model": model
                }
            }
            return formatted_response
        except Exception as e:
            print(f"[ModelManager] Error generating response with OpenAI: {e}")
            return {
                "status": "error",
                "message": str(e),
                "metadata": {
                    "provider": "openai",
                    "model": model
                }
            }

    def _generate_with_ollama(self, prompt, model= None, **kwargs):
        """
        Generate a response using Ollama API.
        :param prompt: Text prompt.
        :param model: Ollama model to use.
        :return: Generated response.
        """
        import ollama
        model = model or self.model
        ollama_client = ollama.Client(host='http://localhost:11434')  # Ollama local client
        try:
            # Add 'query' to the prompt if provided
            if 'query' in kwargs:
                prompt = f"{prompt}\n\nQuery Context: {kwargs['query']}"
            response = ollama_client.chat(
                model=model,
                messages=[
                    {"role": "system", "content": "Provide a concise and relevant answer to the user's query."},
                    {"role": "user", "content": prompt}
                ]
            )
            if response and 'message' in response:
                message = response['message']['content']
                formatted_response = {
                    "status": "success",
                    "content": message,
                    "metadata": {
                        "provider": "ollama",
                        "model": model
                    }
                }
                return formatted_response
        except Exception as e:
            print(f"[ModelManager] Error generating response with Ollama: {e}")
            return {
                "status": "error",
                "message": str(e),
                "metadata": {
                    "provider": "ollama",
                    "model": model
                }
            }

    def _generate_with_groq(self, prompt, model= None, **kwargs):
        """
        Generate a response using Groq API.
        :param prompt: Text prompt.
        :param model: Groq model to use.
        :return: Generated response.
        """
        import groq
        model = model or self.model
        
        groq_client = groq.Groq(api_key=self.api_key)
        try:
            # Add 'query' to the prompt if provided
            if 'query' in kwargs:
                prompt = f"{prompt}\n\nQuery Context: {kwargs['query']}"
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Provide a concise and relevant answer to the user's query."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            if response.choices:
                message = response.choices[0].message.content.strip()
                formatted_response = {
                    "status": "success",
                    "content": message,
                    "metadata": {
                        "provider": "groq",
                        "model": model
                    }
                }
                return formatted_response
        except Exception as e:
            print(f"[ModelManager] Error generating response with Groq: {e}")
            return {
                "status": "error",
                "message": str(e),
                "metadata": {
                    "provider": "groq",
                    "model": model
                }
            }
        
    def _anthropic_generate(self, prompt: str, model= None, **kwargs) -> Dict:
        """
        Generate a response using Anthropic API.
        :param prompt: Text prompt for the LLM.
        :return: Dictionary with response or error.
        """
        # Placeholder for Anthropic implementation
        pass
        
    def _reasonchain_generate(self, prompt: str, model= None, **kwargs) -> Dict:
        """
        Generate a response using ReasonChain API.
        :param prompt: Text prompt for the LLM.
        :return: Dictionary with response or error.
        """
        # Placeholder for ReasonChain implementation
        pass

    @classmethod
    def add_provider(cls, provider_name: str, models: list, implementation_function):
        """
        Dynamically add a new provider with models to the integration.
        :param provider_name: Name of the new provider.
        :param models: List of models supported by the provider.
        :param implementation_function: Function handling the generation for the provider.
        """
        cls.SUPPORTED_PROVIDERS[provider_name] = models
        setattr(cls, f"_{provider_name}_generate", implementation_function)
        logging.info(f"Added new provider: {provider_name} with models: {models}")
