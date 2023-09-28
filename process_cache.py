import json
from collections.abc import Iterator
from os import DirEntry, scandir, walk
from models.trek_object import TrekObject
from models.trek_object_type import TrekObjectType


def process_cache_files():
    # Get correct directory
    directory_path = get_correct_directory()

    directory_items: list[DirEntry] = list(scandir(directory_path))
    files = list(filter(lambda x: x.is_file(), directory_items))

    file_count = 0
    files_skipped = 0
    saving: list[TrekObjectType] = TrekObject.get_saving_types()

    for i in range(len(files)):
        file = files[i]
        file_count += 1
        with open(file.path, "rb") as f:
            data = f.read()

        trek_object = TrekObject()
        trek_object.create_model(data)
        if trek_object.model == '' or trek_object.trek_object_type not in saving:
            files_skipped += 1
            continue
        else:
            write_file(trek_object, file_count)
            print(f'Files Written: {file_count}  | Files Skipped: {files_skipped}')


def write_file(trek_object: TrekObject, file_count: int):
    if trek_object.trek_object_type != TrekObjectType.Translations:
        file_type_name = trek_object.trek_object_type.value.replace("/", "_")
    else:
        file_type_name = trek_object.translation.translation_type.value.replace("/", "_")

    with open(trek_object.trek_object_folder_path +
              f'{file_type_name + str(file_count)}.json', "w") as w:
        w.write(json.dumps(trek_object.model))


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
