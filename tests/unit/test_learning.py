"""Unit tests for the learning module."""

import pytest
from pathlib import Path
from datetime import datetime
from devin_integration.learning import LessonManager, Lesson

@pytest.fixture
def sample_lessons_file(tmp_path):
    """Create a sample lessons file."""
    file_path = tmp_path / ".cursorrules"
    content = """# Multi-Agent Scratchpad

## Background and Motivation
Test background

## Cursor learned
- Always use pathlib.Path for cross-platform path handling in Python
- When dealing with file uploads, normalize paths to use forward slashes
- Store file paths in the database using relative paths
- Use tempfile.mkdtemp() for creating temporary upload directories
- Implement file size and type validation before starting the upload

## Next Steps
Test next steps
"""
    file_path.write_text(content)
    return file_path

@pytest.fixture
def lesson_manager(sample_lessons_file):
    """Create a LessonManager instance with the sample file."""
    return LessonManager(str(sample_lessons_file))

def test_load_lessons(lesson_manager):
    """Test loading lessons from file."""
    assert len(lesson_manager.lessons) == 5
    assert all(isinstance(lesson, Lesson) for lesson in lesson_manager.lessons)
    
    # Check first lesson content and tags
    first_lesson = lesson_manager.lessons[0]
    assert "pathlib.Path" in first_lesson.content
    assert "python" in first_lesson.context_tags
    assert "path_handling" in first_lesson.context_tags
    
    # Check other lessons have appropriate tags
    assert any("file_operations" in lesson.context_tags for lesson in lesson_manager.lessons)
    assert any("database" in lesson.context_tags for lesson in lesson_manager.lessons)

def test_extract_context_tags():
    """Test context tag extraction."""
    manager = LessonManager()
    tags = manager._extract_context_tags("Use pathlib.Path for file operations in Python")
    assert "python" in tags
    assert "file_operations" in tags
    assert "path_handling" in tags

def test_get_relevant_lessons(lesson_manager):
    """Test getting relevant lessons."""
    context = {
        "tags": ["python", "file_operations"]
    }
    relevant_lessons = lesson_manager.get_relevant_lessons(context)
    assert len(relevant_lessons) > 0
    assert all(any(tag in context["tags"] for tag in lesson.context_tags) 
              for lesson in relevant_lessons)

def test_apply_lessons(lesson_manager):
    """Test applying lessons."""
    context = {
        "tags": ["python", "file_operations"]
    }
    applied_lessons = lesson_manager.apply_lessons(context)
    assert len(applied_lessons) > 0
    assert all(isinstance(lesson, str) for lesson in applied_lessons)
    assert all(lesson.startswith("- ") for lesson in applied_lessons)

def test_add_lesson(lesson_manager):
    """Test adding a new lesson."""
    new_lesson = "Test new lesson about Python"
    lesson_manager.add_lesson(new_lesson)
    
    # Check if lesson was added to memory
    assert any(lesson.content == new_lesson for lesson in lesson_manager.lessons)
    
    # Check if lesson was saved to file
    with open(lesson_manager.lessons_file, 'r') as f:
        content = f.read()
        assert new_lesson in content

def test_save_lessons(lesson_manager, tmp_path):
    """Test saving lessons to file."""
    # Create a new lesson
    new_lesson = "Test save lesson"
    lesson_manager.add_lesson(new_lesson)
    
    # Create a new manager to load from the saved file
    new_manager = LessonManager(str(lesson_manager.lessons_file))
    
    # Verify the lesson was saved and loaded correctly
    assert any(lesson.content == new_lesson for lesson in new_manager.lessons)

def test_track_lesson_effectiveness(lesson_manager):
    """Test tracking lesson effectiveness."""
    # Get a lesson to track
    context = {"tags": ["python", "path_handling"]}
    lessons = lesson_manager.get_relevant_lessons(context)
    assert len(lessons) > 0
    
    lesson = lessons[0]
    initial_score = lesson.effectiveness_score
    
    # Report successful application
    lesson_manager.track_lesson_usage(lesson.content, success=True)
    assert lesson.success_count == 1
    assert lesson.failure_count == 0
    assert lesson.effectiveness_score > initial_score
    
    # Report failed application
    lesson_manager.track_lesson_usage(lesson.content, success=False)
    assert lesson.success_count == 1
    assert lesson.failure_count == 1
    assert lesson.effectiveness_score < 1.0
    
    # Verify the scores are persisted
    new_manager = LessonManager(str(lesson_manager.lessons_file))
    saved_lesson = next(l for l in new_manager.lessons if l.content == lesson.content)
    assert saved_lesson.success_count == 1
    assert saved_lesson.failure_count == 1
    assert saved_lesson.effectiveness_score == lesson.effectiveness_score 