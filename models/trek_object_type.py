from enum import Enum


class TrekObjectType(Enum):
    def __str__(self):
        return str(self.value)

    Building = 'building/'
    Hostile = 'hostile/'
    Mission = 'mission/'
    MissionChain = 'mission/chain/'
    Officer = 'officer/'
    Research = 'research/'
    Ship = 'ship/'
    System = 'system/'
    Translations = 'translations/'

