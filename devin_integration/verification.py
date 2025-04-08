"""Verification functionality for devin_integration."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from .llm import LLMClient
from .errors import VerificationError

class VerificationResult:
    """Class representing a verification result."""
    
    def __init__(
        self,
        status: str,
        confidence: float,
        matches: List[str],
        mismatches: List[str]
    ):
        """Initialize the result.
        
        Args:
            status: The status of the verification ("success" or "failure").
            confidence: Confidence score between 0 and 1.
            matches: List of criteria that matched.
            mismatches: List of criteria that did not match.
        """
        self.status = status
        self.confidence = confidence
        self.matches = matches
        self.mismatches = mismatches
    
    def __str__(self) -> str:
        """Return a string representation of the result."""
        return (
            f"VerificationResult(status={self.status}, "
            f"confidence={self.confidence}, "
            f"matches={len(self.matches)}, "
            f"mismatches={len(self.mismatches)})"
        )

class VerificationClient:
    """Client for verifying tasks and results."""
    
    def __init__(
        self,
        min_confidence: float = 0.8,
        timeout: int = 30
    ):
        """Initialize the verification client.
        
        Args:
            min_confidence: Minimum confidence score for success.
            timeout: Timeout in seconds for verification.
        """
        self.min_confidence = min_confidence
        self.timeout = timeout
        self.llm_client = LLMClient()

    def _validate_verification_result(self, result: Dict) -> bool:
        """Validate a verification result.
        
        Args:
            result: The result to validate.
            
        Returns:
            True if the result is valid, False otherwise.
        """
        return (
            isinstance(result, dict) and
            "status" in result and
            "confidence" in result and
            "details" in result and
            isinstance(result["details"], dict) and
            "matches" in result["details"] and
            "mismatches" in result["details"]
        )

    async def verify_task(
        self,
        task: Dict,
        criteria: List[str],
        **options
    ) -> VerificationResult:
        """Verify a task against criteria.
        
        Args:
            task: The task to verify.
            criteria: List of criteria to verify against.
            **options: Additional options:
                - min_confidence: Minimum confidence score for success.
                - timeout: Timeout in seconds for verification.
            
        Returns:
            Verification result.
            
        Raises:
            VerificationError: If there is an error during verification.
        """
        try:
            # Get options
            min_confidence = options.get('min_confidence', self.min_confidence)
            timeout = options.get('timeout', self.timeout)
            
            # Create verification prompt
            prompt = (
                f"Please verify the following task against these criteria:\n\n"
                f"Task: {json.dumps(task, indent=2)}\n\n"
                f"Criteria: {json.dumps(criteria, indent=2)}\n\n"
                f"Respond with a JSON object containing:\n"
                f"- status: 'success' or 'failure'\n"
                f"- confidence: a number between 0 and 1\n"
                f"- details: an object with 'matches' and 'mismatches' arrays\n"
            )
            
            # Get verification result from LLM
            response = await self.llm_client.generate_response(prompt)
            result = json.loads(response.content)
            
            if not self._validate_verification_result(result):
                raise VerificationError("Invalid verification result format")
            
            # Create verification result
            return VerificationResult(
                status=result["status"],
                confidence=result["confidence"],
                matches=result["details"]["matches"],
                mismatches=result["details"]["mismatches"]
            )
        except Exception as e:
            raise VerificationError(f"Error verifying task: {e}", cause=e)

    async def verify_screenshot(
        self,
        screenshot_path: Union[str, Path],
        expected_content: List[str],
        prompt_template: Optional[str] = None
    ) -> Dict[str, bool]:
        """Verify the content of a screenshot.
        
        Args:
            screenshot_path: Path to the screenshot.
            expected_content: List of content items to verify.
            prompt_template: Optional template for the verification prompt.
            
        Returns:
            Dictionary mapping content items to verification results.
            
        Raises:
            VerificationError: If there is an error during verification.
        """
        try:
            if prompt_template is None:
                prompt_template = (
                    "Please verify if the following content appears in the image: {content}. "
                    "Respond with only 'yes' or 'no'."
                )
            
            results = {}
            for content in expected_content:
                prompt = prompt_template.format(content=content)
                response = await self.vision_client.analyze_image(
                    screenshot_path,
                    prompt,
                    max_tokens=10
                )
                results[content] = response.lower().strip() == "yes"
            
            return results
        except Exception as e:
            raise VerificationError(f"Error verifying screenshot: {e}")

    async def verify_url(
        self,
        url: str,
        expected_content: List[str],
        output_path: Optional[Union[str, Path]] = None,
        prompt_template: Optional[str] = None
    ) -> Dict[str, bool]:
        """Verify the content of a webpage.
        
        Args:
            url: The URL to verify.
            expected_content: List of content items to verify.
            output_path: Optional path to save the screenshot.
            prompt_template: Optional template for the verification prompt.
            
        Returns:
            Dictionary mapping content items to verification results.
            
        Raises:
            VerificationError: If there is an error during verification.
        """
        try:
            from .screenshot import take_screenshot
            
            if output_path is None:
                output_path = Path("screenshot.png")
            
            screenshot_path = await take_screenshot(url, output_path)
            return await self.verify_screenshot(
                screenshot_path,
                expected_content,
                prompt_template
            )
        except Exception as e:
            raise VerificationError(f"Error verifying URL {url}: {e}") 