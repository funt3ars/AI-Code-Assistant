#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
import time
import logging
from typing import Optional, Dict, Any
from tools.token_tracker import TokenUsage, APIResponse, get_token_tracker
from tools.llm_api import query_llm, create_llm_client, LLMConfig

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

STATUS_FILE = '.cursorrules'
SCRATCHPAD_FILE = 'scratchpad.md'

def load_environment():
    """Load environment variables from .env files"""
    env_files = ['.env.local', '.env', '.env.example']
    env_loaded = False
    
    for env_file in env_files:
        env_path = Path('.') / env_file
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            env_loaded = True
            logger.info(f"Loaded environment from {env_file}")
            break
    
    if not env_loaded:
        logger.warning("No .env files found. Using system environment variables only.")

def read_file_content(file_path: str) -> Optional[str]:
    """Read content from a specified file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            logger.info(f"Successfully read content from {file_path}")
            return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None

def write_file_content(file_path: str, content: str) -> bool:
    """Write content to a specified file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            logger.info(f"Successfully wrote content to {file_path}")
            return True
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {e}")
        return False

def update_scratchpad(new_content: str) -> bool:
    """Update the scratchpad file with new content"""
    try:
        # Read existing content
        existing_content = read_file_content(SCRATCHPAD_FILE)
        if existing_content is None:
            # Create new file if it doesn't exist
            existing_content = "# Scratchpad\n\n"
        
        # Find the Scratchpad section
        scratchpad_marker = "# Scratchpad"
        if scratchpad_marker in existing_content:
            # Split content into before and after scratchpad sections
            parts = existing_content.split(scratchpad_marker)
            if len(parts) > 1:
                before_scratchpad = parts[0]
                
                # Update content, replacing everything after the Scratchpad marker
                updated_content = f"{before_scratchpad}{scratchpad_marker}\n\n{new_content}\n"
            else:
                # If no content after marker, just append
                updated_content = f"{existing_content}\n\n{new_content}"
        else:
            # Append to end of file
            updated_content = f"{existing_content}\n\n{new_content}"
        
        return write_file_content(SCRATCHPAD_FILE, updated_content)
    except Exception as e:
        logger.error(f"Error updating scratchpad: {e}")
        return False

def update_lessons(new_lesson: str) -> bool:
    """Update the lessons section in the .cursorrules file"""
    try:
        # Read existing content
        existing_content = read_file_content(STATUS_FILE)
        if existing_content is None:
            logger.error("Could not read .cursorrules file")
            return False
        
        # Find the Cursor learned section
        lessons_marker = "## Cursor learned"
        if lessons_marker in existing_content:
            # Split content into before and after lessons
            parts = existing_content.split(lessons_marker)
            if len(parts) > 1:
                before_lessons = parts[0]
                after_lessons = parts[1]
                
                # Find the next section marker
                next_section_marker = "\n# "
                if next_section_marker in after_lessons:
                    next_section_parts = after_lessons.split(next_section_marker, 1)
                    lessons_content = next_section_parts[0]
                    rest_content = next_section_marker + next_section_parts[1]
                else:
                    lessons_content = after_lessons
                    rest_content = ""
                
                # Add new lesson
                if not new_lesson.startswith("- "):
                    new_lesson = f"- {new_lesson}"
                
                updated_content = f"{before_lessons}{lessons_marker}\n{lessons_content}\n{new_lesson}\n{rest_content}"
            else:
                # If no content after marker, just append
                updated_content = f"{existing_content}\n{new_lesson}\n"
        else:
            # If no lessons section exists, create it
            updated_content = f"{existing_content}\n\n{lessons_marker}\n\n{new_lesson}\n"
        
        return write_file_content(STATUS_FILE, updated_content)
    except Exception as e:
        logger.error(f"Error updating lessons: {e}")
        return False

def query_llm_with_plan(
    plan_content: str,
    user_prompt: Optional[str] = None,
    file_content: Optional[str] = None,
    provider: str = "openai",
    model: Optional[str] = None
) -> Optional[str]:
    """Query the LLM with combined prompts"""
    try:
        # Create LLM client with configuration
        config = LLMConfig()
        if not model:
            model = config.get_provider_config(provider).get("default_model")
        
        client = create_llm_client(provider=provider, model=model)
        logger.info(f"Created LLM client with provider={provider}, model={model}")
        
        # Combine prompts
        combined_prompt = f"""You are working on a multi-agent context. The executor is the one who actually does the work. And you are the planner. Now the executor is asking you for help. Please analyze the provided project plan and status, then address the executor's specific query or request.

You need to think like a founder. Prioritize agility and don't over-engineer. Think deep. Try to foresee challenges and derisk earlier. If opportunity sizing or probing experiments can reduce risk with low cost, instruct the executor to do them.
        
Project Plan and Status:
======
{plan_content}
======
"""

        if file_content:
            combined_prompt += f"\nFile Content:\n======\n{file_content}\n======\n"

        if user_prompt:
            combined_prompt += f"\nUser Query:\n{user_prompt}\n"

        combined_prompt += """\nYour response should be in two parts:

Part 1: Lessons Learned
Identify any important lessons or best practices that should be captured for future reference. These should be practical, reusable insights that would be valuable for similar tasks in the future. Format each lesson as a bullet point.

Part 2: Implementation Plan
Create a detailed plan that includes:
1. A clear description of the task
2. Key challenges and considerations
3. Step-by-step implementation plan
4. Success criteria
5. Any relevant notes or dependencies

Format your response with clear section markers:
[LESSONS]
Your lessons here...
[/LESSONS]

[PLAN]
Your markdown-formatted plan here...
[/PLAN]
"""

        # Query the LLM
        logger.info("Sending combined prompt to LLM")
        response = client.query(combined_prompt)
        logger.info("Received response from LLM")
        
        # Extract lessons and plan
        if response and "[LESSONS]" in response and "[/LESSONS]" in response and "[PLAN]" in response and "[/PLAN]" in response:
            lessons = response.split("[LESSONS]")[1].split("[/LESSONS]")[0].strip()
            plan = response.split("[PLAN]")[1].split("[/PLAN]")[0].strip()
            
            # Update lessons if any were provided
            if lessons:
                for lesson in lessons.split("\n"):
                    if lesson.strip():
                        update_lessons(lesson.strip())
            
            return plan
        else:
            logger.warning("Response did not contain properly formatted sections")
            return response
            
    except Exception as e:
        logger.error(f"Error in query_llm_with_plan: {e}")
        return None

def main():
    try:
        parser = argparse.ArgumentParser(description='Query LLM with project plan context')
        parser.add_argument('--prompt', type=str, help='Additional prompt to send to the LLM', required=False)
        parser.add_argument('--file', type=str, help='Path to a file whose content should be included in the prompt', required=False)
        parser.add_argument('--provider', choices=['openai','anthropic','gemini','local','deepseek','azure'], default='openai', help='The API provider to use')
        parser.add_argument('--model', type=str, help='The model to use (default depends on provider)')
        parser.add_argument('--debug', action='store_true', help='Enable debug logging')
        parser.add_argument('--config', type=str, help='Path to configuration file')
        args = parser.parse_args()

        if args.debug:
            logger.setLevel(logging.DEBUG)
            logger.debug("Debug logging enabled")

        if args.config:
            os.environ['LLM_CONFIG_PATH'] = args.config

        # Load environment variables
        load_environment()

        # Read plan status
        plan_content = read_file_content(STATUS_FILE)
        if not plan_content:
            logger.error("Failed to read plan status")
            sys.exit(1)

        # Read file content if specified
        file_content = None
        if args.file:
            file_content = read_file_content(args.file)
            if file_content is None:
                logger.error("Failed to read specified file")
                sys.exit(1)

        # Query LLM and update scratchpad
        response = query_llm_with_plan(plan_content, args.prompt, file_content, provider=args.provider, model=args.model)
        if response:
            if update_scratchpad(response):
                print('Successfully updated scratchpad.md with the new plan.')
                print('Please review the changes and proceed with implementation.')
            else:
                logger.error("Failed to update scratchpad")
                sys.exit(1)
        else:
            logger.error("Failed to get response from LLM")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error in main: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 