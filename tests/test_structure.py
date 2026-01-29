import unittest
import os
import sys

# Add examples to path so we can import them
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestExamples(unittest.TestCase):
    def test_example_files_exist(self):
        """Sanity check to ensure all example examples exists."""
        required_files = [
            'examples/basic_spatial_query.py',
            'examples/task_decomposition.py',
            'examples/tool_use_recycling.py',
            'examples/video_anomaly_detection.py'
        ]
        for f in required_files:
            self.assertTrue(os.path.exists(f), f"Missing example file: {f}")

    def test_requirements_file(self):
        """Ensure requirements.txt is present for users."""
        self.assertTrue(os.path.exists("requirements.txt"))

if __name__ == '__main__':
    unittest.main()
