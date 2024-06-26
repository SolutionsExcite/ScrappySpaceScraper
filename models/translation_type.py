from enum import Enum


class TranslationType(Enum):
    def __str__(self):
        return str(self.value)

    Blueprints = 'blueprints/'
    Buildings = 'buildings/'
    BuildingBuffs = 'building_buffs/'
    Consumables = 'consumables/'
    Factions = 'factions/'
    Hostiles = 'hostiles/'
    Materials = 'materials/'
    Missiontasks = 'mission_tasks/'
    Missions = 'missions/'
    Officers = 'officers/'
    OfficerDivision = 'officer_division/'
    OfficerSynergy = 'officer_synergy/'
    Research = 'research/'
    ShipComponents = 'ship_components/'
    ShipType = 'ship_type/'
    Ships = 'ships/'
    Syndicate = 'syndicate/'
    Systems = 'systems/'
    Traits = 'traits/'
