import json
import os

def load_config():
    """Load configuration from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"Error loading config: {e}")