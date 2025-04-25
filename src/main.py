import os
import glob
import datetime
import shutil
import calendar
import re
import getpass
from config import load_config
from directory_reader import DirectoryReader
from services.summarizer import Summarizer
from utils.file_organizer import FileOrganizer
from utils.file_handler import ensure_directory_exists


def get_api_key():
    """Prompt for and return the OpenAI API key."""
    print("\nPlease enter your OpenAI API key:")
    return getpass.getpass("API Key: ")


def setup_services(config):
    """Initialize and return the directory reader and summarizer services."""
    print("\nInitializing services...")
    # Ensure OUTPUT_DIR exists
    ensure_directory_exists(config['OUTPUT_DIR'])
    reader = DirectoryReader(config)
    summarizer = Summarizer(config)
    print("✓ Services initialized")
    return reader, summarizer


def collect_dates(reader, bee_files, limitless_files):
    """Extract and return unique dates from the files in a more efficient way."""
    print("\nExtracting dates from files...")
    
    # Combine files from both sources
    all_files = bee_files + limitless_files
    if not all_files:
        print("❌ No files to process")
        return []
    
    # Extract all dates at once using regex
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")
    all_dates = set()
    
    # Process files in batches to avoid memory issues with very large datasets
    batch_size = 1000
    for i in range(0, len(all_files), batch_size):
        batch_files = all_files[i:i+batch_size]
        
        # Join all filenames in the batch with a separator for efficient regex processing
        combined_paths = "\n".join(batch_files)
        
        # Find all dates in the combined string
        for match in date_pattern.finditer(combined_paths):
            all_dates.add(match.group(1))
    
    # Exclude today's date
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    if today_str in all_dates:
        print(f"Skipping files dated today: {today_str}")
        all_dates.remove(today_str)

    if not all_dates:
        print("❌ No valid dates found in files")
        return []

    # Convert to list and sort chronologically
    all_dates = sorted(list(all_dates))
    print(f"\nFound {len(all_dates)} dates to process: {', '.join(all_dates)}")
    return all_dates


def process_dates(reader, summarizer, all_dates):
    """Process data for each date and return success counts."""
    processed_count = 0
    failed_count = 0
    skipped_count = 0

    # Read supplementary data first
    print("\nReading facts and errors...")
    facts = reader.read_facts()
    errors = reader.read_errors()
    print("✓ Facts and errors loaded")

    # Process each date
    for date in all_dates:
        print(f"\nChecking data for {date}...")
        
        # Skip if a journal file already exists for this date
        if summarizer.file_exists_for_date(date):
            print(f"✓ Journal entry already exists for {date}, skipping...")
            skipped_count += 1
            continue
        
        # Read the data for this date
        bee_data = reader.read_bee_data_for_date(date)
        limitless_data = reader.read_limitless_data_for_date(date)
        
        # Skip this date if we don't have data
        if not bee_data and not limitless_data:
            print(f"⚠️ No data found for {date}, skipping...")
            continue
        
        # Process the data
        if summarizer.process_all(bee_data, limitless_data, facts, errors, date):
            processed_count += 1
        else:
            failed_count += 1

    return processed_count, failed_count, skipped_count


def print_results(processed_count, failed_count, skipped_count, config):
    """Print processing results and debug information."""
    print(f"\n=== AI Summarizer Complete ===")
    print(f"Successfully processed: {processed_count} date(s)")
    if skipped_count > 0:
        print(f"Skipped existing: {skipped_count} date(s)")
    if failed_count > 0:
        print(f"Failed to process: {failed_count} date(s)")

    # Debug: Count files in output directory
    result_files = glob.glob(os.path.join(config['OUTPUT_DIR'], '*.md'))
    print(f"\nDebug: Found {len(result_files)} files in output directory")
    for file in result_files:
        print(f"- {os.path.basename(file)}")


def main():
    """Main entry point for the AI Summarizer application."""
    print("\n=== Starting AI Summarizer ===")
    
    # 1. Load configuration
    print("\nLoading configuration...")
    config = load_config()
    config['OPENAI_API_KEY'] = get_api_key()
    print("✓ Configuration loaded with API key")
    
    # 2. Organize directories
    print("\nOrganizing directory structure...")
    file_organizer = FileOrganizer()
    file_organizer.organize_all_directories(config)
    
    # 3. Initialize services
    reader, summarizer = setup_services(config)

    # 4. Collect files
    print("\nCollecting available files...")
    bee_files = reader.get_bee_files()
    limitless_files = reader.get_limitless_files()
    
    if not bee_files and not limitless_files:
        print("❌ No source files found")
        return

    # 5. Extract dates and process
    all_dates = collect_dates(reader, bee_files, limitless_files)
    if not all_dates:
        return
        
    processed_count, failed_count, skipped_count = process_dates(reader, summarizer, all_dates)
    
    # 6. Print results
    print_results(processed_count, failed_count, skipped_count, config)


if __name__ == "__main__":
    main()