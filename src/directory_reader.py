import os
import re
from datetime import datetime
from utils.file_handler import read_file, write_file
from utils.openai_handler import OpenAIHandler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter # Added import

# Download stopwords if not already downloaded
try:
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))

# Download punkt tokenizer if not already downloaded (needed for word_tokenize)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Download punkt_tab tokenizer if not already downloaded (sometimes needed)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

def _remove_stopwords(text):
    """Remove stop words from a given text."""
    if not text:
        return text
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    return " ".join(filtered_sentence)

def _remove_repetitive_phrases(text, n=2, threshold=0.2):
    """Remove repetitive phrases from a given text."""
    if not text:
        return text
    
    # Tokenize the text into words
    words = word_tokenize(text)
    
    # Avoid processing if text is too short for n-grams
    if len(words) < n:
        return text

    # Generate n-grams (phrases of n words)
    ngrams = list(nltk.ngrams(words, n))
    
    # Avoid division by zero if no n-grams are generated
    if not ngrams:
        return text

    # Count the frequency of each n-gram
    ngram_counts = Counter(ngrams)
    
    # Calculate the total number of n-grams
    total_ngrams = len(ngrams)
    
    # Identify repetitive n-grams based on the threshold
    repetitive_ngrams = {ngram: count for ngram, count in ngram_counts.items()
                         if count / total_ngrams > threshold}
    
    # Remove repetitive n-grams from the text
    filtered_words = []
    i = 0
    while i < len(words):
        found_repetitive = False
        # Check only if there are enough words left for an n-gram
        if i <= len(words) - n:
            current_ngram = tuple(words[i:i+n])
            if current_ngram in repetitive_ngrams:
                i += n  # Skip the entire n-gram
                found_repetitive = True
        
        if not found_repetitive:
            filtered_words.append(words[i])
            i += 1
    
    # Join the filtered words back into a text
    return " ".join(filtered_words)


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
        """Read bee data for a specific date, remove stop words and repetitive phrases."""
        # Find files matching the date pattern
        bee_files = self.get_bee_files()
        matching_files = []
        
        for file in bee_files:
            file_date = self.extract_date_from_filename(file)
            if file_date == date:
                matching_files.append(file)
        
        if not matching_files:
            print(f"No BEE data found for {date}")
            return None
        
        # Read and combine the content
        combined_content = ""
        for file in matching_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Truncate extremely large files if needed

                    if len(content) > 30000:  # Arbitrary limit to prevent context explosion
                        print(f"⚠️ Truncating large BEE file: {file}")
                        print(f"File size: {len(content)} characters")
                        content = content[:30000] + "\n...[content truncated due to size]..."
                    
                    # Remove stop words
                    content_without_stopwords = _remove_stopwords(content)
                    # Remove repetitive phrases
                    final_content = _remove_repetitive_phrases(content_without_stopwords)
                    combined_content += f"\n\n--- File: {os.path.basename(file)} ---\n{final_content}"
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        return combined_content

    def read_limitless_data_for_date(self, date):
        """Read limitless data for a specific date, remove stop words and repetitive phrases."""
        # Find files matching the date pattern
        limitless_files = self.get_limitless_files()
        matching_files = []
        
        for file in limitless_files:
            file_date = self.extract_date_from_filename(file)
            if file_date == date:
                matching_files.append(file)
        
        if not matching_files:
            print(f"No LIMITLESS data found for {date}")
            return None
        
        # Read and combine the content
        combined_content = ""
        for file in matching_files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Truncate extremely large files if needed
                    if len(content) > 30000:  # Arbitrary limit to prevent context explosion
                        print(f"⚠️ Truncating large LIMITLESS file: {file}")
                        print(f"File size: {len(content)} characters")
                        content = content[:30000] + "\n...[content truncated due to size]..."
                    
                    # Remove stop words
                    content_without_stopwords = _remove_stopwords(content)
                    # Remove repetitive phrases
                    final_content = _remove_repetitive_phrases(content_without_stopwords)
                    combined_content += f"\n\n--- File: {os.path.basename(file)} ---\n{final_content}"
            except Exception as e:
                print(f"Error reading {file}: {e}")
        
        return combined_content

    def _get_files(self, directory):
        """Gets a list of files recursively from the given directory and its subdirectories."""
        try:
            all_files = []
            # Walk through directory tree
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # Add full path to each file
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            return all_files
        except FileNotFoundError:
            print(f"Directory not found: {directory}")
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