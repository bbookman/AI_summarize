def read_file(file_path):
    """Read the contents of a file and return it."""
    print(f"\nReading file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print(f"✓ Successfully read file ({len(content)} chars)")
            return content
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        raise
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None

def write_file(file_path, content):
    """Write content to a file."""
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")

def file_exists(file_path):
    """Check if a file exists."""
    import os
    return os.path.isfile(file_path)