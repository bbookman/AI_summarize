import os
import re
import calendar
import shutil
from utils.file_handler import ensure_directory_exists


class FileOrganizer:
    """
    Handles organization of files into a year/month directory structure
    based on dates in filenames.
    """
    
    def __init__(self):
        # Pattern to extract date from filenames (assuming YYYY-MM-DD format)
        self.date_pattern = re.compile(r'(\d{4})-(\d{2})-\d{2}')
    
    def organize_directory(self, directory_path):
        """
        Organizes files in a directory by moving them into a year/month structure
        based on dates in the filenames.
        
        Args:
            directory_path (str): Path to directory containing files to organize
            
        Returns:
            int: Number of files organized
        """
        # Get only files at the root level that need organization
        try:
            root_files = [f for f in os.listdir(directory_path) 
                      if os.path.isfile(os.path.join(directory_path, f))]
        except FileNotFoundError:
            print(f"Directory not found: {directory_path}")
            return 0
            
        if not root_files:
            return 0  # No files need organizing
        
        organized_count = 0
        for file in root_files:
            match = self.date_pattern.search(file)
            if match:
                year, month_num = match.groups()
                # Convert month number to name and format as "MM-MonthName"
                month_name = calendar.month_name[int(month_num)]
                month_dir_name = f"{month_num}-{month_name}"
                
                # Create year directory if it doesn't exist
                year_dir = os.path.join(directory_path, year)
                ensure_directory_exists(year_dir)
                
                # Create month directory if it doesn't exist
                month_dir = os.path.join(year_dir, month_dir_name)
                ensure_directory_exists(month_dir)
                
                # Move the file to the appropriate directory
                source_path = os.path.join(directory_path, file)
                target_path = os.path.join(month_dir, file)
                
                # Only move if file isn't already in the correct location
                if source_path != target_path:
                    shutil.move(source_path, target_path)
                    organized_count += 1
        
        return organized_count
    
    def organize_all_directories(self, config):
        """
        Organizes files in all configured directories (BEE_DATA, LIMITLESS_DATA, OUTPUT_DIR).
        
        Args:
            config (dict): Application configuration containing directory paths
            
        Returns:
            tuple: Count of organized files in each directory (bee, limitless, output)
        """
        # Check if organization is needed
        bee_organized = self.organize_directory(config['BEE_DATA'])
        limitless_organized = self.organize_directory(config['LIMITLESS_DATA'])
        
        # Ensure OUTPUT_DIR exists
        ensure_directory_exists(config['OUTPUT_DIR'])
        output_organized = self.organize_directory(config['OUTPUT_DIR'])
        
        if bee_organized or limitless_organized or output_organized:
            print(f"✓ Organized {bee_organized} BEE files, {limitless_organized} LIMITLESS files, and {output_organized} OUTPUT files")
        else:
            print("No new files to organize in root directories")
            
        return (bee_organized, limitless_organized, output_organized)