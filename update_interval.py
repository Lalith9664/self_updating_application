import re
import json

# Update config.json
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    if 'check_interval_minutes' in config.get('auto_update', {}):
        val = config['auto_update'].pop('check_interval_minutes')
        config['auto_update']['check_interval_seconds'] = 30
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
except Exception as e:
    print(f"Skipping config.json: {e}")

# Update api.py
with open('api.py', 'r') as f:
    api_content = f.read()
api_content = api_content.replace('"check_interval_minutes": 1', '"check_interval_seconds": 30')
with open('api.py', 'w') as f:
    f.write(api_content)

# Update index.html
with open('app/templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('Check Interval (minutes)', 'Check Interval (seconds)')
html = html.replace('checkIntervalMinutes:', 'checkIntervalSeconds:')
html = html.replace('check_interval_minutes', 'check_interval_seconds')
html = html.replace('checkIntervalMinutes =', 'checkIntervalSeconds =')
html = html.replace('.checkIntervalMinutes', '.checkIntervalSeconds')
html = html.replace('checkIntervalMinutes * 60 * 1000', 'checkIntervalSeconds * 1000')
html = html.replace('minutes`);', 'seconds`);')

# Make sure the default is 30 instead of 5 in the UI inputs
html = html.replace('checkIntervalSeconds: 5', 'checkIntervalSeconds: 30')
html = html.replace("getElementById('checkInterval').value) || 5", "getElementById('checkInterval').value) || 30")

with open('app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Interval configuration changed to 30 seconds.")
