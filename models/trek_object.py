import json

from models.translation import Translation
from models.translation_type import TranslationType
from models.trek_object_type import TrekObjectType


class TrekObject:
    def __init__(self):
        self.content_string: str = ''
        self.content_bytes: bytes = bytes()
        self.regex_match: str = ''
        self.base_folder_path: str = 'C:/Users/lenha/Desktop/stfc-objects/json_objects/'
        self.trek_object_type: TrekObjectType = TrekObjectType.Ship
        self.trek_object_folder_path: str = ''
        self.is_translation: bool = False
        self.model: str = ''
        self.translation: Translation = Translation()

    def create_model(self, content: bytes):
        self.content_bytes: bytes = content
        self.model: str = self.get_json()
        self.check_type()

    def get_json(self) -> str:
        self.content_string: str = self.content_bytes.decode('utf8', errors="replace")
        try:
            content_part = self.content_string.split('https:')[1].split('�A')[0]
        except IndexError:
            content_part = ''
        else:
            bracket = content_part.find('{')
            brace = content_part.find('[')

            start_start = brace if brace < bracket else bracket
            content_part = content_part[start_start:]
            content_part = json.loads(content_part)

        return content_part

    def check_type(self):
        matched_object_type = self.get_trek_object_type()
        if matched_object_type is not None:
            self.trek_object_type: TrekObjectType = matched_object_type
            trek_type_value = TrekObjectType(self.trek_object_type).value
            self.trek_object_folder_path = self.base_folder_path + trek_type_value
            self.regex_match = '/v1/' + trek_type_value
            if self.trek_object_type == TrekObjectType.Translations:
                # Fill out translation model
                matched_translation_type = self.get_trek_translation_type()
                if matched_translation_type is not None:
                    self.translation.translation_type = matched_translation_type

    def get_trek_object_type(self):
        object_type_list: list[TrekObjectType] = [e for e in TrekObjectType]

        def check(object_type: TrekObjectType) -> TrekObjectType:
            index = self.content_string.find('v1/' + object_type.value)
            if index > 0:
                return object_type

        matched_object_type = list(filter(check, object_type_list))
        if len(matched_object_type) > 0:
            return matched_object_type[0]
        return None

    def get_trek_translation_type(self):
        object_type_list: list[TranslationType] = [e for e in TranslationType]

        def check(object_type: TranslationType) -> TranslationType:
            index = self.content_string.find('/v1/translations/en/' + object_type.value)
            if index > 0:
                return object_type

        matched_object_type = list(filter(check, object_type_list))
        if len(matched_object_type) > 0:
            return matched_object_type[0]
        return None

    @staticmethod
    def get_saving_types() -> list[TrekObjectType]:
        saving_type_list = list()
        saving_type_list.append(TrekObjectType.Ship)
        saving_type_list.append(TrekObjectType.Hostile)
        saving_type_list.append(TrekObjectType.Translations)
        saving_type_list.append(TrekObjectType.Officer)
        return saving_type_list


