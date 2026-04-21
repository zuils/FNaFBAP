from typing import Dict, List, NamedTuple, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .__init__ import FNaFB2World
from BaseClasses import MultiWorld, Region, LocationProgressType
from .Locations import FNaFB2Location, location_table, has_category
from Options import Toggle


class FNaFB2RegionData(NamedTuple):
    locations: Optional[List[str]]


def create_regions(world: "FNaFB2World"):
    regions: Dict[str, FNaFB2RegionData] = {
        "Menu":                         FNaFB2RegionData(None),

        "Show Stage":                   FNaFB2RegionData([]),
        
        "Show Stage Proud":             FNaFB2RegionData([]),
        
        "Levelsanity":                  FNaFB2RegionData([]),
        
        "Grindy":                       FNaFB2RegionData([]),

        "Trade Machine":                FNaFB2RegionData([]),

        "Kid's Cove":                   FNaFB2RegionData([]),

        "Kid's Cove B.B.":              FNaFB2RegionData([]),
        
        "Kid's Cove Proud":             FNaFB2RegionData([]),
        
        "Kid's Cove Critical":          FNaFB2RegionData([]),

        "Main Hall":                    FNaFB2RegionData([]),

        "Main Hall B.B.":               FNaFB2RegionData([]),

        "Women's Bathroom":             FNaFB2RegionData([]),
        
        "Women's Bathroom Proud":       FNaFB2RegionData([]),
        
        "Women's Bathroom Critical":    FNaFB2RegionData([]),

        "Men's Bathroom":               FNaFB2RegionData([]),

        "Men's Bathroom Proud":         FNaFB2RegionData([]),

        "Men's Bathroom Critical":      FNaFB2RegionData([]),

        "Parts/Service":                FNaFB2RegionData([]),

        "Parts/Service Proud":          FNaFB2RegionData([]),

        "Office Hall":                  FNaFB2RegionData([]),

        "Office Hall Proud":            FNaFB2RegionData([]),

        "Party Room 3":                 FNaFB2RegionData([]),

        "Party Room 3 B.B.":            FNaFB2RegionData([]),
        
        "Party Room 3 Proud":           FNaFB2RegionData([]),
        
        "Party Room 3 Critical":        FNaFB2RegionData([]),

        "Party Room 4":                 FNaFB2RegionData([]),
        
        "Party Room 4 Proud":           FNaFB2RegionData([]),
        
        "Party Room 4 Critical":        FNaFB2RegionData([]),
        
        "Party Room 1":                 FNaFB2RegionData([]),
        
        "Party Room 1 Proud":           FNaFB2RegionData([]),
        
        "Party Room 1 Critical":        FNaFB2RegionData([]),
        
        "Left Vent":                    FNaFB2RegionData([]),

        "Party Room 2":                 FNaFB2RegionData([]),

        "Party Room 2 Proud":           FNaFB2RegionData([]),

        "Party Room 2 Critical":        FNaFB2RegionData([]),

        "Right Vent":                   FNaFB2RegionData([]),

        "Office":                       FNaFB2RegionData([]),
        
        "Office B.B.":                  FNaFB2RegionData([]),

        "Office Proud":                 FNaFB2RegionData([]),

        "Office Critical":              FNaFB2RegionData([]),

        "Cave of the Past":             FNaFB2RegionData([]),
        
        "B.B.'s Lair":                  FNaFB2RegionData([]),
        
        "B.B. Giygas":                  FNaFB2RegionData([]),
        
        "Refurbs":                      FNaFB2RegionData([])
    }

    # Category hell
    for name, data in location_table.items():
        if isinstance(data.category, str):
            regions[data.category].locations.append(name)
        else:
            if world.options.scenario.value == 0 and has_category(data, "NotBBScenario"):
                regions[data.category[1]].locations.append(name)
            elif world.options.scenario.value == 1 and has_category(data, "BBScenario"):
                regions[data.category[1]].locations.append(name)

    for name, data in regions.items():
        if name == "Trade Machine" and world.options.trade_quest == Toggle.option_false:
            continue
        if name == "Levelsanity" and (world.options.levelsanity == Toggle.option_false or world.options.difficulty.value == 2):
            continue
        if "Critical" in name and world.options.difficulty.value < 2:
            continue
        if "Proud" in name and world.options.difficulty.value < 1:
            continue
        if name == "Refurbs" and world.options.goal.value == 0:
            continue
        world.multiworld.regions.append(create_region(world, world.player, name, data))


def create_region(world: "FNaFB2World", player: int, name: str, data: FNaFB2RegionData):
    region = Region(name, player, world.multiworld)
    if data.locations:
        for loc_name in data.locations:
            loc_data = location_table.get(loc_name)
            location = FNaFB2Location(player, loc_name, loc_data.code if loc_data else None, region)
            if (
                ("Rod of Femininity" in loc_name and world.options.fem_rods == Toggle.option_true)
                or (loc_name == "Boss Rush" and world.options.extra_checks == Toggle.option_true and world.options.goal == 0)
                or (loc_name == "Cave of the Past - Dragon Dildo F" and world.options.extra_checks == Toggle.option_true and world.options.goal == 0)
                or ("Shadow Bonnie" in loc_name and world.options.shadow_bonnie == Toggle.option_true and world.options.difficulty.value == 2)
                or ("Toy Freddy - Use" in loc_name and world.options.grindy == Toggle.option_true)
                ):
                location.progress_type = LocationProgressType.EXCLUDED
            region.locations.append(location)

    return region
    
def connect_regions(multiworld: MultiWorld, source: str, target: List[str], rule=None):
    sourceRegion = multiworld.get_region(source)
    targetRegion = multiworld.get_region(target)
    sourceRegion.connect(targetRegion, rule=rule)