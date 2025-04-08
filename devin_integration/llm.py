"""LLM functionality for devin_integration."""

import os
from typing import Dict, List, Optional, Union
import openai
import anthropic
from .errors import LLMError
from .utils import get_env_var

class LLMResponse:
    """Class representing an LLM response."""
    
    def __init__(self, content: str, role: str = "assistant"):
        """Initialize the response.
        
        Args:
            content: The content of the response.
            role: The role of the response (e.g., "assistant").
        """
        self.content = content
        self.role = role
    
    def __str__(self) -> str:
        """Return the content as a string."""
        return self.content

class LLMClient:
    """Client for interacting with LLMs."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", max_tokens: int = 1000):
        """Initialize the LLM client.
        
        Args:
            api_key: Optional API key. If not provided, will try to get from environment.
            model: The model to use.
            max_tokens: Maximum number of tokens to generate.
        """
        self.api_key = api_key or get_env_var("OPENAI_API_KEY")
        self.model = model
        self.max_tokens = max_tokens
        openai.api_key = self.api_key

    def _format_prompt(self, prompt: str) -> List[Dict[str, str]]:
        """Format a prompt for the LLM.
        
        Args:
            prompt: The prompt to format.
            
        Returns:
            Formatted prompt as a list of messages.
        """
        return [{"role": "user", "content": prompt}]

    def _validate_response(self, response: Dict) -> bool:
        """Validate an LLM response.
        
        Args:
            response: The response to validate.
            
        Returns:
            True if the response is valid, False otherwise.
        """
        return (
            isinstance(response, dict) and
            "choices" in response and
            isinstance(response["choices"], list) and
            len(response["choices"]) > 0 and
            "message" in response["choices"][0] and
            "content" in response["choices"][0]["message"]
        )

    async def generate_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        stop: Optional[Union[str, List[str]]] = None
    ) -> LLMResponse:
        """Generate a response using the LLM.
        
        Args:
            prompt: The prompt to generate from.
            temperature: Sampling temperature.
            stop: Optional stop sequences.
            
        Returns:
            The generated response.
            
        Raises:
            LLMError: If there is an error generating text.
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=self._format_prompt(prompt),
                max_tokens=self.max_tokens,
                temperature=temperature,
                stop=stop
            )
            
            if not self._validate_response(response):
                raise LLMError("Invalid response format")
                
            message = response["choices"][0]["message"]
            return LLMResponse(message["content"], message["role"])
        except Exception as e:
            raise LLMError(f"Error generating text: {e}", cause=e) 