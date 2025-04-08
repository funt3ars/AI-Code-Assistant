"""Learning and lesson management module."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid

@dataclass
class Lesson:
    """Represents a learned lesson with metadata."""
    content: str
    context_tags: List[str]
    category: str
    priority: int = 1
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    last_used_at: Optional[datetime] = None
    usage_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    is_deprecated: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert lesson to dictionary for serialization."""
        return {
            'id': self.id,
            'content': self.content,
            'context_tags': self.context_tags,
            'category': self.category,
            'priority': self.priority,
            'version': self.version,
            'created_at': self.created_at.isoformat(),
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None,
            'usage_count': self.usage_count,
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'is_deprecated': self.is_deprecated
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Lesson':
        """Create lesson from dictionary."""
        return cls(
            id=data['id'],
            content=data['content'],
            context_tags=data['context_tags'],
            category=data['category'],
            priority=data['priority'],
            version=data['version'],
            created_at=datetime.fromisoformat(data['created_at']),
            last_used_at=datetime.fromisoformat(data['last_used_at']) if data['last_used_at'] else None,
            usage_count=data['usage_count'],
            success_count=data['success_count'],
            failure_count=data['failure_count'],
            is_deprecated=data['is_deprecated']
        )

class LessonManager:
    """Manages lessons and their lifecycle."""
    
    def __init__(self):
        """Initialize the lesson manager."""
        self.lessons: List[Lesson] = []
    
    def add_lesson(self, lesson: Lesson) -> None:
        """Add a new lesson to the manager."""
        self.lessons.append(lesson)
    
    def get_lesson_by_id(self, lesson_id: str) -> Optional[Lesson]:
        """Get a lesson by its ID."""
        for lesson in self.lessons:
            if lesson.id == lesson_id:
                return lesson
        return None
    
    def get_lessons_by_category(self, category: str) -> List[Lesson]:
        """Get all lessons in a category."""
        return [lesson for lesson in self.lessons if lesson.category == category]
    
    def match_lessons_by_tags(self, tags: List[str]) -> List[Lesson]:
        """Get lessons matching any of the given tags."""
        return [
            lesson for lesson in self.lessons
            if not lesson.is_deprecated and
            any(tag in lesson.context_tags for tag in tags)
        ]
    
    def match_lessons_by_priority(self, min_priority: int = 1) -> List[Lesson]:
        """Get lessons with priority >= min_priority."""
        return [
            lesson for lesson in self.lessons
            if not lesson.is_deprecated and
            lesson.priority >= min_priority
        ]
    
    def track_lesson_usage(self, lesson_id: str, success: bool) -> None:
        """Track usage of a lesson and update its statistics."""
        lesson = self.get_lesson_by_id(lesson_id)
        if lesson:
            lesson.usage_count += 1
            if success:
                lesson.success_count += 1
            else:
                lesson.failure_count += 1
            lesson.last_used_at = datetime.now()
    
    def calculate_effectiveness(self, lesson_id: str) -> float:
        """Calculate the effectiveness of a lesson."""
        lesson = self.get_lesson_by_id(lesson_id)
        if not lesson or lesson.usage_count == 0:
            return 0.0
        return lesson.success_count / lesson.usage_count
    
    def deprecate_lesson(self, lesson_id: str) -> None:
        """Mark a lesson as deprecated."""
        lesson = self.get_lesson_by_id(lesson_id)
        if lesson:
            lesson.is_deprecated = True
    
    def update_lesson(self, lesson_id: str, **kwargs) -> None:
        """Update a lesson's properties."""
        lesson = self.get_lesson_by_id(lesson_id)
        if lesson:
            for key, value in kwargs.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            lesson.version += 1
    
    def merge_lessons(self, lesson_ids: List[str]) -> Lesson:
        """Merge multiple lessons into a new one."""
        lessons = [self.get_lesson_by_id(id) for id in lesson_ids]
        lessons = [l for l in lessons if l is not None]
        
        if not lessons:
            raise ValueError("No valid lessons to merge")
        
        # Use the first lesson as base
        base = lessons[0]
        merged = Lesson(
            content="\n\n".join(l.content for l in lessons),
            context_tags=list(set(tag for l in lessons for tag in l.context_tags)),
            category=base.category,
            priority=max(l.priority for l in lessons)
        )
        
        self.add_lesson(merged)
        return merged 