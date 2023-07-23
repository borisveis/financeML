import json
configfilepath='config/config.json'
# Load the JSON configuration file
with open(configfilepath, 'r') as config_file:
    config = json.load(config_file)
openai = config['openai']
openai_key = openai['key']
print(openai_key)
