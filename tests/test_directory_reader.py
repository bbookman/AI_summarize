import unittest
from src.directory_reader import DirectoryReader

class TestDirectoryReader(unittest.TestCase):

    def setUp(self):
        self.reader = DirectoryReader()

    def test_read_bee_data(self):
        data = self.reader.read_bee_data()
        self.assertIsNotNone(data)
        # Add more assertions based on expected data structure

    def test_read_limitless_data(self):
        data = self.reader.read_limitless_data()
        self.assertIsNotNone(data)
        # Add more assertions based on expected data structure

    def test_read_facts(self):
        data = self.reader.read_facts()
        self.assertIsNotNone(data)
        # Add more assertions based on expected data structure

    def test_read_errors(self):
        data = self.reader.read_errors()
        self.assertIsNotNone(data)
        # Add more assertions based on expected data structure

if __name__ == '__main__':
    unittest.main()