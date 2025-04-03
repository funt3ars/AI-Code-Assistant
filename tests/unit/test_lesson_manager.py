"""Unit tests for the LessonManager class."""

import pytest
from datetime import datetime
from typing import Dict, Any
from devin_integration.learning import LessonManager, Lesson

@pytest.fixture
def lesson_manager():
    """Create a LessonManager instance for testing."""
    return LessonManager()

@pytest.fixture
def sample_lesson():
    """Create a sample lesson for testing."""
    return Lesson(
        content="Test lesson content",
        context_tags=["test", "example"],
        category="testing",
        priority=1,
        version=1,
        created_at=datetime.now(),
        last_used_at=None,
        usage_count=0,
        success_count=0,
        failure_count=0
    )

class TestLessonManagerBasics:
    """Tests for basic LessonManager functionality."""
    
    def test_initialization(self, lesson_manager):
        """Test that LessonManager initializes correctly."""
        assert lesson_manager.lessons == []
        assert isinstance(lesson_manager.lessons, list)
    
    def test_add_lesson(self, lesson_manager, sample_lesson):
        """Test adding a lesson to the manager."""
        lesson_manager.add_lesson(sample_lesson)
        assert len(lesson_manager.lessons) == 1
        assert lesson_manager.lessons[0] == sample_lesson
    
    def test_get_lesson_by_id(self, lesson_manager, sample_lesson):
        """Test retrieving a lesson by ID."""
        lesson_manager.add_lesson(sample_lesson)
        retrieved = lesson_manager.get_lesson_by_id(sample_lesson.id)
        assert retrieved == sample_lesson
    
    def test_get_lessons_by_category(self, lesson_manager, sample_lesson):
        """Test retrieving lessons by category."""
        lesson_manager.add_lesson(sample_lesson)
        lessons = lesson_manager.get_lessons_by_category("testing")
        assert len(lessons) == 1
        assert lessons[0] == sample_lesson

class TestLessonMatching:
    """Tests for lesson matching functionality."""
    
    def test_match_lessons_by_tags(self, lesson_manager, sample_lesson):
        """Test matching lessons by context tags."""
        lesson_manager.add_lesson(sample_lesson)
        matches = lesson_manager.match_lessons_by_tags(["test"])
        assert len(matches) == 1
        assert matches[0] == sample_lesson
    
    def test_match_lessons_by_priority(self, lesson_manager):
        """Test matching lessons by priority."""
        high_priority = Lesson(
            content="High priority",
            context_tags=["test"],
            category="testing",
            priority=3
        )
        low_priority = Lesson(
            content="Low priority",
            context_tags=["test"],
            category="testing",
            priority=1
        )
        lesson_manager.add_lesson(high_priority)
        lesson_manager.add_lesson(low_priority)
        
        matches = lesson_manager.match_lessons_by_priority(min_priority=2)
        assert len(matches) == 1
        assert matches[0] == high_priority

class TestLessonEffectiveness:
    """Tests for lesson effectiveness tracking."""
    
    def test_track_lesson_usage(self, lesson_manager, sample_lesson):
        """Test tracking lesson usage."""
        lesson_manager.add_lesson(sample_lesson)
        lesson_manager.track_lesson_usage(sample_lesson.id, success=True)
        
        updated = lesson_manager.get_lesson_by_id(sample_lesson.id)
        assert updated.usage_count == 1
        assert updated.success_count == 1
        assert updated.failure_count == 0
        assert updated.last_used_at is not None
    
    def test_calculate_effectiveness(self, lesson_manager, sample_lesson):
        """Test calculating lesson effectiveness."""
        lesson_manager.add_lesson(sample_lesson)
        lesson_manager.track_lesson_usage(sample_lesson.id, success=True)
        lesson_manager.track_lesson_usage(sample_lesson.id, success=False)
        
        effectiveness = lesson_manager.calculate_effectiveness(sample_lesson.id)
        assert effectiveness == 0.5  # 1 success / 2 total uses

class TestLessonLifecycle:
    """Tests for lesson lifecycle management."""
    
    def test_deprecate_lesson(self, lesson_manager, sample_lesson):
        """Test deprecating a lesson."""
        lesson_manager.add_lesson(sample_lesson)
        lesson_manager.deprecate_lesson(sample_lesson.id)
        
        updated = lesson_manager.get_lesson_by_id(sample_lesson.id)
        assert updated.is_deprecated
    
    def test_update_lesson(self, lesson_manager, sample_lesson):
        """Test updating a lesson."""
        lesson_manager.add_lesson(sample_lesson)
        new_content = "Updated content"
        lesson_manager.update_lesson(sample_lesson.id, content=new_content)
        
        updated = lesson_manager.get_lesson_by_id(sample_lesson.id)
        assert updated.content == new_content
        assert updated.version == 2
    
    def test_merge_lessons(self, lesson_manager):
        """Test merging similar lessons."""
        lesson1 = Lesson(
            content="First lesson",
            context_tags=["test"],
            category="testing"
        )
        lesson2 = Lesson(
            content="Second lesson",
            context_tags=["test"],
            category="testing"
        )
        lesson_manager.add_lesson(lesson1)
        lesson_manager.add_lesson(lesson2)
        
        merged = lesson_manager.merge_lessons([lesson1.id, lesson2.id])
        assert merged.content == "First lesson\n\nSecond lesson"
        assert len(lesson_manager.lessons) == 3  # Original two plus merged 