import json


def process_cache_files():
    # Get file paths
    file_path = 'C:/Users/lenha/Desktop/cee89851be302475_01'
    # Usage:
    with open(file_path, "rb") as f:
        content = f.read()
        content = get_json(content)


def get_json(content):
    content = content.decode('utf8')
    content = content.split('\r')[0].split('https:')[1].split('ØA')[0]
    bracket = content.find('{')
    brace = content.find('[')

    start_start = brace if brace < bracket else bracket
    content = content[start_start:]
    content = json.loads(content)

    return content


