"""LLM vision functionality."""

import os
import base64
from typing import Dict, Optional
from openai import OpenAI
from .errors import LLMVisionError

class LLMVisionResponse:
    """Class representing an LLM vision response."""
    
    def __init__(self, content: str, role: str):
        """Initialize the response.
        
        Args:
            content: Response content.
            role: Response role (e.g., "assistant").
        """
        self.content = content
        self.role = role
    
    def __str__(self) -> str:
        """Return a string representation of the response."""
        return self.content

class LLMVisionClient:
    """Client for LLM vision functionality."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-vision-preview",
        max_tokens: int = 1000
    ):
        """Initialize the client.
        
        Args:
            api_key: OpenAI API key.
            model: Model to use for vision tasks.
            max_tokens: Maximum number of tokens in response.
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key)
    
    def _validate_image(self, image_path: str) -> bool:
        """Validate an image file.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            True if the image is valid, False otherwise.
        """
        if not os.path.exists(image_path):
            return False
            
        valid_extensions = [".png", ".jpg", ".jpeg"]
        _, ext = os.path.splitext(image_path)
        
        return ext.lower() in valid_extensions
    
    def _validate_response(self, response: Dict) -> bool:
        """Validate an LLM response.
        
        Args:
            response: Response to validate.
            
        Returns:
            True if the response is valid, False otherwise.
        """
        required_fields = ["choices"]
        
        if not isinstance(response, dict):
            return False
            
        if not all(field in response for field in required_fields):
            return False
            
        if not isinstance(response["choices"], list):
            return False
            
        if not response["choices"]:
            return False
            
        choice = response["choices"][0]
        if not isinstance(choice, dict):
            return False
            
        if "message" not in choice:
            return False
            
        message = choice["message"]
        if not isinstance(message, dict):
            return False
            
        if "content" not in message or "role" not in message:
            return False
            
        return True
    
    def _encode_image(self, image_path: str) -> str:
        """Encode an image as base64.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            Base64-encoded image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image(
        self,
        image_path: str,
        prompt: str,
        **options
    ) -> LLMVisionResponse:
        """Analyze an image using LLM vision.
        
        Args:
            image_path: Path to the image file.
            prompt: Prompt for image analysis.
            **options: Additional analysis options.
            
        Returns:
            LLM vision response.
            
        Raises:
            LLMVisionError: If analysis fails.
        """
        try:
            if not self._validate_image(image_path):
                raise LLMVisionError("Invalid image file")
            
            # Encode image
            base64_image = self._encode_image(image_path)
            
            # Create messages
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                **options
            )
            
            if not self._validate_response(response):
                raise LLMVisionError("Invalid response format")
            
            # Create response object
            choice = response.choices[0]
            return LLMVisionResponse(
                content=choice.message.content,
                role=choice.message.role
            )
        except Exception as e:
            raise LLMVisionError(f"Error analyzing image: {e}", cause=e)