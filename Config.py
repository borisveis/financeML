import json
import os

# Define the path relative to the project root
configfilepath = 'config/config.json'


def load_config():
    if not os.path.exists(configfilepath):
        print(f"Error: Configuration file not found at {configfilepath}")
        return {}

    with open(configfilepath, 'r') as config_file:
        return json.load(config_file)


# This object will be imported by other scripts
config = load_config()

# Keep your existing logic for the OpenAI key if needed for other modules
openai_key = config.get('openai', {}).get('key')