import json
from collections.abc import Iterator
from os import DirEntry, scandir, walk

from models.trek_object import TrekObject


def process_cache_files():
    # Get correct directory
    directory_path = get_correct_directory()

    directory_items = scandir(directory_path)
    files = filter(lambda x: x.is_file(), directory_items)

    # path_to_save = 'C:/Users/lenha/Desktop/stfc-objects/json_objects/test/'

    file_count = 1
    for file in files:
        with open(file.path, "rb") as f:
            trek_object = TrekObject()
            trek_object.create_model(f.read())
            # json_content = get_json(content)
            saving = trek_object.get_saving_types()
            if trek_object.model == '' or trek_object.trek_object_type not in saving:
                break
            with open(trek_object.trek_object_folder_path +
                      f'{trek_object.trek_object_type.value + file_count}.json', "w") as w:
                w.write(json.dumps(trek_object.model))
                file_count += 1


def get_correct_directory():
    file_path = 'C:/Users/lenha/AppData/Local/Google/Chrome/User Data/ScrappySpaceScraper/' \
                'Default/Service Worker/CacheStorage/'

    # Find only directories
    cache: Iterator[DirEntry] = scandir(file_path)
    cache_folder = ''
    for entry in cache:
        if entry.is_dir():
            cache_folder = entry.path

    sub_items: Iterator[DirEntry] = scandir(cache_folder + '/')
    correct_directory_path = ''
    for entry in sub_items:
        if entry.is_dir():
            _, _, files = next(walk(entry.path + '/'))
            if len(files) > 100:
                correct_directory_path = entry.path
                break

    return correct_directory_path


def get_json(content):
    content_content = content.decode('utf8', errors="replace")
    try:
        content_part = content_content.split('https:')[1].split('�A')[0]
    except IndexError:
        content_part = ''
    else:
        bracket = content_part.find('{')
        brace = content_part.find('[')

        start_start = brace if brace < bracket else bracket
        content_part = content_part[start_start:]
        content_part = json.loads(content_part)

    return content_part



