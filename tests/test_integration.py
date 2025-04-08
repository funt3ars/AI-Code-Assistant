"""
Integration tests for the Planner and Executor components.
"""
import unittest
from datetime import datetime
from devin_integration import Planner, Executor

class TestPlannerExecutorIntegration(unittest.TestCase):
    """Test cases for Planner and Executor integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.planner = Planner()
        self.executor = Executor()
    
    def test_create_task_workflow(self):
        """Test complete workflow for a creation task."""
        # Define test task
        task = "Create a new authentication module"
        
        # Get task analysis
        analysis = self.planner.analyze_task(task)
        
        # Verify analysis structure
        self.assertEqual(analysis['description'], task)
        self.assertIn('steps', analysis)
        self.assertIn('success_criteria', analysis)
        
        # Verify steps are properly structured
        for step in analysis['steps']:
            self.assertIn('description', step)
            self.assertIn('type', step)
            self.assertIn('estimated_complexity', step)
        
        # Execute the task
        result = self.executor.execute(analysis)
        
        # Verify execution result
        self.assertEqual(result['description'], task)
        self.assertEqual(result['status'], 'completed')
        self.assertIn('steps_completed', result)
        
        # Verify each completed step
        for step in result['steps_completed']:
            self.assertIn('status', step)
            self.assertIn('step', step)
            self.assertIn('result', step)
            self.assertIn('timestamp', step)
            
            # Verify timestamp format
            try:
                datetime.fromisoformat(step['timestamp'])
            except ValueError:
                self.fail("Invalid timestamp format")
    
    def test_fix_task_workflow(self):
        """Test complete workflow for a fix/debug task."""
        task = "Fix authentication bug in login module"
        
        analysis = self.planner.analyze_task(task)
        
        # Verify fix-specific steps
        step_descriptions = [step['description'].lower() for step in analysis['steps']]
        self.assertTrue(any('root cause' in desc for desc in step_descriptions))
        
        result = self.executor.execute(analysis)
        self.assertEqual(result['status'], 'completed')
    
    def test_test_task_workflow(self):
        """Test complete workflow for a testing task."""
        task = "Test the new authentication module"
        
        analysis = self.planner.analyze_task(task)
        
        # Verify test-specific steps
        step_descriptions = [step['description'].lower() for step in analysis['steps']]
        self.assertTrue(any('test' in desc for desc in step_descriptions))
        
        result = self.executor.execute(analysis)
        self.assertEqual(result['status'], 'completed')
    
    def test_task_with_empty_description(self):
        """Test handling of empty task description."""
        with self.assertRaises(ValueError):
            self.planner.analyze_task("")
    
    def test_task_with_invalid_analysis(self):
        """Test executor handling of invalid analysis input."""
        invalid_analysis = {'description': 'test', 'invalid_key': []}
        
        with self.assertRaises(KeyError):
            self.executor.execute(invalid_analysis)

if __name__ == '__main__':
    unittest.main() 