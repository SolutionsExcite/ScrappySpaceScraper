from models.translation_type import TranslationType


class Translation:
    def __init__(self):
        self.translation_type = TranslationType.Ships
        self.translation_regex_match = '/v1/translations/en/' + self.translation_type.value

