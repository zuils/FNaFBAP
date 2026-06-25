from typing import List

from BaseClasses import Tutorial, Location, LocationProgressType, CollectionState, MultiWorld, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Items import FNaFB2Item, FNaFB2ItemData, get_items_by_category, item_table
from .Locations import FNaFB2Location, location_table
from .Options import FNaFB2Options, Toggle
from .Regions import create_regions
from .Rules import set_rules


class FNaFB2Web(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Five Nights at Fuckboy's 2 client for use with Archipelago.",
        "English",
        "fnafb2_en.md",
        "fnafb2/en",
        ["Zuils and Scrungip"]
    )]


class FNaFB2World(World):
    """
    Are you Freddy for ready?
    """
    game = "Five Nights at Fuckboy's 2"
    options_dataclass = FNaFB2Options
    options = FNaFB2Options
    topology_present = True
    data_version = 4
    required_client_version = (0, 5, 0)
    web = FNaFB2Web()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    def generate_early(self):
        if self.options.levelsanity.value == Toggle.option_false:
            self.options.grindy.value = Toggle.option_false

    def fill_slot_data(self) -> dict:
        return self.options.as_dict("scenario", "goal", "trade_quest", "difficulty", "fem_rods", "extra_checks",
                                    "shadow_bonnie", "levelsanity", "grindy", "copyright", "shop")

    def create_items(self):
        if self.options.scenario.value == 0:
            if self.options.goal == 0:
                boss_loc = self.multiworld.get_location("B.B. Giygas - B.B.", self.player)
            else:
                boss_loc = self.multiworld.get_location("Refurbs", self.player)
        else:
            boss_loc = self.multiworld.get_location("B.B. Giygas - Toy Animatronics", self.player)
        
        boss_loc.place_locked_item(self.create_item("Victory"))
        
        item_pool: List[FNaFB2Item] = []
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for name, data in item_table.items():
            quantity = data.max_quantity
            category = data.category
            
            # If difficulty is standard, remove the cassettes, lucky soda, and double pizza
            if self.options.difficulty.value == 0 and (category == "Cassette" \
                or "Lucky Soda" in name or "Double Pizza" in name):
                continue
            
            # Ignore filler and goal, filler will be added in a later stage.
            if category in ("Filler", "Goal"):
                continue
            
            # BB Scenario items
            if self.options.scenario.value == 0 and "BBScenario" in category:
                continue
            elif self.options.scenario.value == 1 and "TFScenario" in category:
                continue

            item_pool += [self.create_item(name) for _ in range(quantity)]
        while len(item_pool) < total_locations:
            item_pool.append(self.create_item(self.get_filler_item_name()))

        self.multiworld.itempool += item_pool

    def get_filler_item_name(self) -> str:
        fillers = get_items_by_category("Filler")
        weights = [data.weight for data in fillers.values()]
        return self.multiworld.random.choices(list(fillers.keys()), weights, k=1)[0]

    def create_item(self, name: str) -> FNaFB2Item:
        data = item_table[name]
        return FNaFB2Item(name, data.classification, data.code, self.player)
    
    def create_regions(self):
        create_regions(self)

    def set_rules(self):
        set_rules(self, self.player)