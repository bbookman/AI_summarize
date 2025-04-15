import os
import re
from datetime import datetime
from utils.file_handler import read_file, write_file
from utils.openai_handler import OpenAIHandler

class DirectoryReader:
    def __init__(self, config):
        print("\nInitializing Directory Reader...")
        self.config = config
        print("✓ Directory Reader initialized")

    def get_bee_files(self):
        """Gets all files from the BEE_DATA directory."""
        return self._get_files(self.config['BEE_DATA'])

    def get_limitless_files(self):
        """Gets all files from the LIMITLESS_DATA directory."""
        return self._get_files(self.config['LIMITLESS_DATA'])

    def extract_date_from_filename(self, file_path):
        """Public wrapper for _extract_date method."""
        return self._extract_date(file_path)

    def read_bee_data_for_date(self, date):
        """Read bee data for a specific date."""
        bee_files = self.get_bee_files()
        for file in bee_files:
            if date in file:
                return read_file(file)
        return None

    def read_limitless_data_for_date(self, date):
        """Read limitless data for a specific date."""
        limitless_files = self.get_limitless_files()
        for file in limitless_files:
            if date in file:
                return read_file(file)
        return None

    def _get_files(self, directory):
        """Gets a list of files in the given directory."""
        try:
            return [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        except FileNotFoundError:
            return []

    def _extract_date(self, file_path):
        """Extracts the date from the filename using a regular expression."""
        match = re.search(r"(\d{4}-\d{2}-\d{2})", file_path)
        return match.group(1) if match else None

    def read_facts(self):
        """Read contents of a single text file from the FACTS directory."""
        facts_dir = self.config['FACTS']
        facts_file = os.path.join(facts_dir, 'facts.md')
        
        try:
            if not os.path.exists(facts_file):
                return None
            return read_file(facts_file)
        except Exception as e:
            print(f"Error reading facts file: {e}")
            return None

    def read_errors(self):
        """Read contents of a single text file from the ERRORS directory."""
        errors_dir = self.config['ERRORS']
        errors_file = os.path.join(errors_dir, 'errors.md')
        
        try:
            if not os.path.exists(errors_file):
                return None
            return read_file(errors_file)
        except Exception as e:
            print(f"Error reading errors file: {e}")
            return None