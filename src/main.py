def main():
    from config import load_config
    from directory_reader import DirectoryReader
    from services.summarizer import Summarizer
    import os
    import glob

    print("\n=== Starting AI Summarizer ===")
    
    print("\nLoading configuration...")
    config = load_config()
    print("✓ Configuration loaded")

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

    if not all_dates:
        print("❌ No valid dates found in files")
        return

    print(f"\nFound {len(all_dates)} unique dates to process")
    
    for date in sorted(all_dates):
        print(f"\nProcessing data for {date}...")
        bee_data = reader.read_bee_data_for_date(date)
        limitless_data = reader.read_limitless_data_for_date(date)

        # Only process if at least one of bee_data or limitless_data is present
        if not bee_data and not limitless_data:
            print(f"⚠️ No data found for date: {date}")
            failed_count += 1
            continue

        facts = reader.read_facts()
        errors = reader.read_errors()

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