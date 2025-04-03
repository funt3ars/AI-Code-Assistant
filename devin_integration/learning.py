"""Learning module for managing and applying lessons."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Lesson:
    """Represents a learned lesson."""
    content: str
    context_tags: List[str]
    created_at: datetime
    last_used: Optional[datetime] = None
    success_count: int = 0
    failure_count: int = 0
    effectiveness_score: float = 0.0

    def update_effectiveness(self, success: bool) -> None:
        """Update the effectiveness score based on usage result."""
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
            
        total_uses = self.success_count + self.failure_count
        self.effectiveness_score = self.success_count / total_uses if total_uses > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert lesson to dictionary for storage."""
        return {
            "content": self.content,
            "context_tags": self.context_tags,
            "created_at": self.created_at.isoformat(),
            "last_used": self.last_used.isoformat() if self.last_used else None,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "effectiveness_score": self.effectiveness_score
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Lesson':
        """Create lesson from dictionary."""
        return cls(
            content=data["content"],
            context_tags=data["context_tags"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]) if data.get("last_used") else None,
            success_count=data.get("success_count", 0),
            failure_count=data.get("failure_count", 0),
            effectiveness_score=data.get("effectiveness_score", 0.0)
        )

class LessonManager:
    """Manages lessons and their application."""
    
    def __init__(self, lessons_file: str = ".cursorrules"):
        """Initialize the lesson manager.
        
        Args:
            lessons_file: Path to the lessons file.
        """
        self.lessons_file = Path(lessons_file)
        self.lessons: List[Lesson] = []
        self._load_lessons()
    
    def _load_lessons(self) -> None:
        """Load lessons from the lessons file."""
        if not self.lessons_file.exists():
            logger.warning(f"Lessons file not found: {self.lessons_file}")
            return
            
        try:
            with open(self.lessons_file, 'r') as f:
                content = f.read()
                
            # Find the lessons section
            if "## Cursor learned" in content:
                lessons_section = content.split("## Cursor learned")[1].split("\n# ")[0]
                
                # Try to load lessons with metadata first
                try:
                    metadata_start = lessons_section.find("<!--")
                    metadata_end = lessons_section.find("-->")
                    if metadata_start != -1 and metadata_end != -1:
                        metadata = json.loads(lessons_section[metadata_start + 4:metadata_end])
                        self.lessons = [Lesson.from_dict(data) for data in metadata]
                        logger.info(f"Loaded {len(self.lessons)} lessons with metadata")
                        return
                except Exception as e:
                    logger.debug(f"No metadata found or invalid format: {e}")
                
                # Fall back to parsing markdown format
                lesson_lines = [line.strip() for line in lessons_section.split("\n") if line.strip().startswith("- ")]
                for line in lesson_lines:
                    lesson_content = line[2:].strip()  # Remove the "- " prefix
                    self.lessons.append(Lesson(
                        content=lesson_content,
                        context_tags=self._extract_context_tags(lesson_content),
                        created_at=datetime.now()
                    ))
                    
            logger.info(f"Loaded {len(self.lessons)} lessons")
        except Exception as e:
            logger.error(f"Error loading lessons: {e}")
    
    def _extract_context_tags(self, lesson_content: str) -> List[str]:
        """Extract context tags from lesson content."""
        # Simple implementation - can be enhanced with NLP
        tags = []
        content_lower = lesson_content.lower()
        
        # Language tags
        if "python" in content_lower:
            tags.append("python")
        if "javascript" in content_lower or "js" in content_lower:
            tags.append("javascript")
        if "typescript" in content_lower or "ts" in content_lower:
            tags.append("typescript")
            
        # Operation tags
        if "file" in content_lower:
            tags.append("file_operations")
        if "path" in content_lower:
            tags.append("path_handling")
        if "error" in content_lower or "exception" in content_lower:
            tags.append("error_handling")
        if "test" in content_lower:
            tags.append("testing")
        if "database" in content_lower or "db" in content_lower:
            tags.append("database")
            
        return tags
    
    def get_relevant_lessons(self, context: Dict[str, Any]) -> List[Lesson]:
        """Get lessons relevant to the current context.
        
        Args:
            context: Dictionary containing current task context.
            
        Returns:
            List of relevant lessons.
        """
        relevant_lessons = []
        context_tags = context.get("tags", [])
        
        for lesson in self.lessons:
            # Simple matching - can be enhanced with more sophisticated matching
            if any(tag in context_tags for tag in lesson.context_tags):
                relevant_lessons.append(lesson)
        return relevant_lessons
    
    def apply_lessons(self, context: Dict[str, Any]) -> List[str]:
        """Apply relevant lessons to the current context.
        
        Args:
            context: Dictionary containing current task context.
            
        Returns:
            List of applied lesson contents.
        """
        relevant_lessons = self.get_relevant_lessons(context)
        applied_lessons = []
        
        for lesson in relevant_lessons:
            applied_lessons.append(f"- {lesson.content}")
            lesson.last_used = datetime.now()
            
        return applied_lessons
    
    def add_lesson(self, content: str, context_tags: Optional[List[str]] = None) -> None:
        """Add a new lesson.
        
        Args:
            content: The lesson content.
            context_tags: Optional list of context tags.
        """
        if context_tags is None:
            context_tags = self._extract_context_tags(content)
            
        new_lesson = Lesson(
            content=content,
            context_tags=context_tags,
            created_at=datetime.now()
        )
        
        self.lessons.append(new_lesson)
        self._save_lessons()
    
    def track_lesson_usage(self, lesson_content: str, success: bool) -> None:
        """Track the effectiveness of a lesson's usage.
        
        Args:
            lesson_content: The content of the lesson to track.
            success: Whether the lesson was successfully applied.
        """
        for lesson in self.lessons:
            if lesson.content == lesson_content:
                lesson.update_effectiveness(success)
                lesson.last_used = datetime.now()
                self._save_lessons()
                break
    
    def _save_lessons(self) -> None:
        """Save lessons to the lessons file."""
        try:
            # Read existing content
            if self.lessons_file.exists():
                with open(self.lessons_file, 'r') as f:
                    content = f.read()
            else:
                content = ""
            
            # Prepare lessons section with metadata
            lessons_section = "## Cursor learned\n\n"
            lessons_section += "<!--\n"
            lessons_section += json.dumps([lesson.to_dict() for lesson in self.lessons], indent=2)
            lessons_section += "\n-->\n\n"
            
            # Add visible lessons
            for lesson in self.lessons:
                lessons_section += f"- {lesson.content}\n"
            
            # Update or add lessons section
            if "## Cursor learned" in content:
                parts = content.split("## Cursor learned")
                before_lessons = parts[0]
                after_lessons = parts[1].split("\n# ", 1)[1] if len(parts) > 1 and "\n# " in parts[1] else ""
                updated_content = f"{before_lessons}{lessons_section}\n# {after_lessons}" if after_lessons else f"{before_lessons}{lessons_section}"
            else:
                updated_content = f"{content}\n\n{lessons_section}"
            
            # Write updated content
            with open(self.lessons_file, 'w') as f:
                f.write(updated_content)
                
            logger.info("Lessons saved successfully")
        except Exception as e:
            logger.error(f"Error saving lessons: {e}") 