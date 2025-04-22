def main():
    from config import load_config
    from directory_reader import DirectoryReader
    from services.summarizer import Summarizer
    import os
    import glob
    import datetime
    import shutil
    import calendar
    import re
    import getpass  # For secure password input

    print("\n=== Starting AI Summarizer ===")
    
    print("\nLoading configuration...")
    config = load_config()
    
    # Prompt for OpenAI API key
    print("\nPlease enter your OpenAI API key:")
    api_key = getpass.getpass("API Key: ")
    
    # Add the API key to the config
    config['OPENAI_API_KEY'] = api_key  
    
    print("✓ Configuration loaded with API key")
    
    print("\nOrganizing directory structure...")
    
    def organize_directory(directory_path):
        # Get only files at the root level that need organization
        root_files = [f for f in os.listdir(directory_path) 
                  if os.path.isfile(os.path.join(directory_path, f))]
        
        if not root_files:
            return 0  # No files need organizing
        
        # Pattern to extract date from filenames (assuming YYYY-MM-DD format)
        date_pattern = re.compile(r'(\d{4})-(\d{2})-\d{2}')
        
        organized_count = 0
        for file in root_files:
            match = date_pattern.search(file)
            if match:
                year, month_num = match.groups()
                # Convert month number to name
                month_name = calendar.month_name[int(month_num)]
                
                # Create year directory if it doesn't exist
                year_dir = os.path.join(directory_path, year)
                os.makedirs(year_dir, exist_ok=True)
                
                # Create month directory if it doesn't exist
                month_dir = os.path.join(year_dir, month_name)
                os.makedirs(month_dir, exist_ok=True)
                
                # Move the file to the appropriate directory
                source_path = os.path.join(directory_path, file)
                target_path = os.path.join(month_dir, file)
                
                # Only move if file isn't already in the correct location
                if source_path != target_path:
                    shutil.move(source_path, target_path)
                    organized_count += 1
        
        return organized_count

    # Check if organization is needed before running
    bee_root_files = [f for f in os.listdir(config['BEE_DATA']) 
                    if os.path.isfile(os.path.join(config['BEE_DATA'], f))]
    limitless_root_files = [f for f in os.listdir(config['LIMITLESS_DATA']) 
                          if os.path.isfile(os.path.join(config['LIMITLESS_DATA'], f))]

    # Create OUTPUT_DIR if it doesn't exist
    os.makedirs(config['OUTPUT_DIR'], exist_ok=True)
    output_root_files = [f for f in os.listdir(config['OUTPUT_DIR']) 
                       if os.path.isfile(os.path.join(config['OUTPUT_DIR'], f))]

    if bee_root_files or limitless_root_files or output_root_files:
        print("\nOrganizing new files found in root directories...")
        bee_organized = organize_directory(config['BEE_DATA'])
        limitless_organized = organize_directory(config['LIMITLESS_DATA'])
        output_organized = organize_directory(config['OUTPUT_DIR'])
        print(f"✓ Organized {bee_organized} BEE files, {limitless_organized} LIMITLESS files, and {output_organized} OUTPUT files")
    else:
        print("\nNo new files to organize in root directories")
    
    print("\nInitializing services...")
    # Ensure OUTPUT_DIR exists
    os.makedirs(config['OUTPUT_DIR'], exist_ok=True)
    reader = DirectoryReader(config)
    summarizer = Summarizer(config)
    print("✓ Services initialized")

    print("\nCollecting available files...")
    # Get all available dates from both sources
    bee_files = reader.get_bee_files()
    limitless_files = reader.get_limitless_files()
    
    if not bee_files and not limitless_files:
        print("❌ No source files found")
        return

    # Process each date's files
    processed_count = 0
    failed_count = 0

    # Combine and deduplicate dates from both sources
    all_dates = set()
    for file in bee_files + limitless_files:
        date = reader.extract_date_from_filename(file)
        if date:
            all_dates.add(date)
        else:
            print(f"⚠️ Could not extract date from file: {file}")

    # Exclude today's date
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    if today_str in all_dates:
        print(f"Skipping files dated today: {today_str}")
        all_dates.remove(today_str)

    if not all_dates:
        print("❌ No valid dates found in files")
        return

    print(f"\nFound {len(all_dates)} unique dates to process")
    
    # Convert to list and sort (newest first)
    all_dates = sorted(list(all_dates), reverse=True)

    # Reverse back to chronological order for processing
    all_dates.sort()  

    print(f"\nFound {len(all_dates)} dates to process: {', '.join(all_dates)}")

    # In main.py, before processing dates, read the facts and errors:
    print("\nReading facts and errors...")
    facts = reader.read_facts()
    errors = reader.read_errors()
    print("✓ Facts and errors loaded")

    # Now process only these 5 days
    for date in all_dates:
        print(f"\nProcessing data for {date}...")
        
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

    print(f"\n=== AI Summarizer Complete ===")
    print(f"Successfully processed: {processed_count} date(s)")
    if failed_count > 0:
        print(f"Failed to process: {failed_count} date(s)")

    # Debug: Count files in output directory
    result_files = glob.glob(os.path.join(config['OUTPUT_DIR'], '*.md'))
    print(f"\nDebug: Found {len(result_files)} files in output directory")
    for file in result_files:
        print(f"- {os.path.basename(file)}")

if __name__ == "__main__":
    main()