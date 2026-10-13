import dataclasses
from typing import override, TYPE_CHECKING

from BaseClasses import CollectionState, MultiWorld, Location, Region, Item
from .Regions import connect_regions
from Options import Toggle
from rule_builder.rules import Has, Rule

if TYPE_CHECKING:
    from . import FNaFB2World


CAMERA_LOCATIONS = (
    "Show Stage - Camera",
    "Game Room - Camera",
    "Prize Corner - Camera",
    "Main Hall - Camera",
    "Kid's Cove - Camera",
    "Parts/Service - Camera",
    "Office - Camera",
    "Left Vent - Camera",
    "Right Vent - Camera",
    "Party Room 1 - Camera",
    "Party Room 2 - Camera",
    "Party Room 3 - Camera",
    "Party Room 4 - Camera",
)


@dataclasses.dataclass()
class FightStage(Rule["FNaFB2World"], game="Five Nights at Fuckboy's 2"):
    stage: str

    def _instantiate(self, world: "FNaFB2World") -> Rule.Resolved:
        return self.Resolved(self.stage, world.options.scenario.value, player=world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        stage: str
        scenario: int

        def _evaluate(self, state: CollectionState) -> bool:
            return _can_fight(self.stage, self.scenario, state, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            item_names = (
                "Toy Bonnie", "Toy Chica", "Mangle", "Withered Freddy", "Withered Bonnie",
                "Withered Chica", "Withered Foxy", "The Puppet",
                "Progressive Microphone", "Progressive Rod of Femininity", "Progressive Dragon Dildo",
                "Progressive Guitar", "Progressive Cupcakes", "Progressive Hook",
                "Progressive Body Endoskeletons", "Progressive Head Endoskeletons",
                "Progressive Pizza Shields", "Progressive Caffeine Sodas",
                "Progressive Tophat Slash", "Progressive Tophat Dash", "Progressive Tophat Crash",
                "Progressive Tophat Smash", "Grab Bag", "Status Bomb", "Spread Bomb",
                "Healing Wing", "Curing Wing", "Raising Wing", "Recovery Wing",
                "Electroshock", "Paravolt", "Somnojolt", "Lightningbolt",
                "Token Throw", "Flying Fright", "B.B. - Curing Wing", "B.B. - Poison Lens",
                "B.B. - Smoke Lens", "B.B. - Confusion Lens", "B.B. - Spread Bomb",
                "The Puppet - Curing Wing", "The Puppet - Poison Lens", "The Puppet - Spread Bomb",
                "The Puppet - Smoke Lens", "The Puppet - Confusion Lens", "Death", "Toreador March",
            )
            return {item_name: {id(self)} for item_name in item_names}


@dataclasses.dataclass()
class CameraCount(Rule["FNaFB2World"], game="Five Nights at Fuckboy's 2"):
    count: int

    def _instantiate(self, world: "FNaFB2World") -> Rule.Resolved:
        return self.Resolved(
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        count: int

        def _evaluate(self, state: CollectionState) -> bool:
            return sum(state.can_reach_location(name, self.player) for name in CAMERA_LOCATIONS) >= self.count

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {location_name: {id(self)} for location_name in CAMERA_LOCATIONS}


def party_count(world: "FNaFB2World", state: CollectionState, player: int) -> int:
    return _party_count(world.options.scenario.value, state, player)


def _party_count(scenario: int, state: CollectionState, player: int) -> int:
    if scenario == 0:
        return (
            state.count("Toy Bonnie", player)
            + state.count("Toy Chica", player) 
            + state.count("Mangle", player)
            + state.count("Withered Freddy", player)
            + state.count("Withered Bonnie", player)
            + state.count("Withered Chica", player)
            + state.count("Withered Foxy", player)
            + 1 # Toy Freddy
        )
    else:
        return 1 + state.count("The Puppet", player)

def freddy_attack(state: CollectionState, player: int) -> int:
    mic = state.count("Progressive Microphone", player)
    rod = state.count("Progressive Rod of Femininity", player)
    dragon = state.count("Progressive Dragon Dildo", player)

    mic_table = [0, 1, 2, 3, 4, 5, 6]
    rod_table = [0, 5, 6]
    dragon_table = [0, 3, 4, 5, 5, 6, 6]

    mic_damage = mic_table[min(mic, len(mic_table) - 1)]
    rod_damage = rod_table[min(rod, len(rod_table) - 1)]
    dragon_damage = dragon_table[min(dragon, len(dragon_table) - 1)]

    return max(mic_damage, rod_damage, dragon_damage)

# Check if the player has the party members before adding their power to the calculation
def total_attack(state: CollectionState, player: int) -> int:
    return (
        freddy_attack(state, player)
        + state.count("Toy Bonnie", player) * state.count("Progressive Guitar", player)
        + state.count("Toy Chica", player) * max((state.count("Progressive Cupcakes", player) - 1), 0) # -1 for the first cupcake
        + state.count("Mangle", player) * state.count("Progressive Hook", player)
        # Withered Animatronics start with Kingly Weapons
        + state.count("Withered Freddy", player) * 5
        + state.count("Withered Bonnie", player) * 5
        + state.count("Withered Chica", player) * 5
        + state.count("Withered Foxy", player) * 5
    )
    
# Endoskeletons provide more defense so we should treat it as such
def total_defense(state: CollectionState, player: int) -> int:
    return (
        (1 + state.count("Toy Bonnie", player) + state.count("Toy Chica", player) + state.count("Mangle", player)) * (
            state.count("Progressive Body Endoskeletons", player) * 4
            + state.count("Progressive Head Endoskeletons", player) * 4
            + state.count("Progressive Pizza Shields", player)
            + state.count("Progressive Caffeine Sodas", player)
        )
        # Each Withered starts with best defense items
        + state.count("Withered Freddy", player) * 40
        + state.count("Withered Bonnie", player) * 40
        + state.count("Withered Chica", player) * 40
        + state.count("Withered Foxy", player) * 40
    )

def skills(world: "FNaFB2World", state: CollectionState, player: int) -> int:
    return _skills(world.options.scenario.value, state, player)


def _skills(scenario: int, state: CollectionState, player: int) -> int:
    if scenario == 0:
        return (
            (
                state.count("Progressive Tophat Slash", player)
                + state.count("Progressive Tophat Dash", player)
                + state.count("Progressive Tophat Crash", player)
                + state.count("Progressive Tophat Smash", player)
            ) 
            + state.count("Toy Bonnie", player) * (
                state.count("Grab Bag", player)
                + state.count("Status Bomb", player)
                + state.count("Spread Bomb", player)
            )
            + state.count("Toy Chica", player) * (
                state.count("Healing Wing", player)
                + state.count("Curing Wing", player)
                + state.count("Raising Wing", player)
                + state.count("Recovery Wing", player)
            )
            + state.count("Mangle", player) * (
                state.count("Electroshock", player)
                + state.count("Paravolt", player)
                + state.count("Somnojolt", player)
                + state.count("Lightningbolt", player)
            )
            # Withered Animatronics start with 3 skills
            + state.count("Withered Freddy", player) * 3
            + state.count("Withered Bonnie", player) * 3
            + state.count("Withered Chica", player) * 3
            + state.count("Withered Foxy", player) * 3
        )
    else:
        return (
            state.count("Token Throw", player)
            + state.count("Flying Fright", player)
            + state.count("Raising Wing", player)
            + state.count("B.B. - Curing Wing", player)
            + state.count("B.B. - Poison Lens", player)
            + state.count("B.B. - Smoke Lens", player)
            + state.count("B.B. - Confusion Lens", player)
            + state.count("B.B. - Spread Bomb", player)
            + state.count("The Puppet", player) * (
                state.count("The Puppet - Curing Wing", player)
                + state.count("The Puppet - Poison Lens", player)
                + state.count("The Puppet - Spread Bomb", player)
                + state.count("The Puppet - Smoke Lens", player)
                + state.count("The Puppet - Confusion Lens", player)
                + state.count("Death", player) * 5 # Death has a 70% chance to instakill every enemy including bosses
                + state.count("Toreador March", player)
            )
        )

def can_fight_earlygame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("earlygame", world.options.scenario.value, state, player)


def can_fight_midgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("midgame", world.options.scenario.value, state, player)


def can_fight_postmidgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("postmidgame", world.options.scenario.value, state, player)


def can_fight_almostlategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("almostlategame", world.options.scenario.value, state, player)


def can_fight_lategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("lategame", world.options.scenario.value, state, player)


def can_fight_endgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    return _can_fight("endgame", world.options.scenario.value, state, player)


def _can_fight(stage: str, scenario: int, state: CollectionState, player: int) -> bool:
    if scenario == 0:
        if stage == "earlygame":
            return total_attack(state, player) >= 1 and total_defense(state, player) >= 4 and _skills(0, state, player) >= 1
        if stage == "midgame":
            return total_attack(state, player) >= 3 and total_defense(state, player) >= 8 and _party_count(0, state, player) >= 2 and _skills(0, state, player) >= 2
        if stage == "postmidgame":
            return total_attack(state, player) >= 6 and total_defense(state, player) >= 12 and _party_count(0, state, player) >= 3 and _skills(0, state, player) >= 4
        if stage == "almostlategame":
            return total_attack(state, player) >= 10 and total_defense(state, player) >= 20 and _party_count(0, state, player) >= 4 and _skills(0, state, player) >= 6
        if stage == "lategame":
            return total_attack(state, player) >= 24 and total_defense(state, player) >= 160 and _party_count(0, state, player) >= 6 and _skills(0, state, player) >= 20
        if stage == "endgame":
            return total_attack(state, player) >= 40 and total_defense(state, player) >= 300 and _party_count(0, state, player) >= 7 and _skills(0, state, player) >= 25
    else:
        if stage == "earlygame":
            return True
        if stage == "midgame":
            return _skills(1, state, player) >= 2
        if stage == "postmidgame":
            return _party_count(1, state, player) > 1 and _skills(1, state, player) >= 4
        if stage == "almostlategame":
            return _party_count(1, state, player) > 1 and _skills(1, state, player) >= 8
        if stage == "lategame":
            return _party_count(1, state, player) > 1 and _skills(1, state, player) >= 12
        if stage == "endgame":
            return _party_count(1, state, player) > 1 and _skills(1, state, player) >= 15 and state.has("Death", player)
    raise ValueError(f"Unknown fight stage: {stage}")


def set_rules(world: "FNaFB2World", player: int):
    from .Q_Rules import set_q_rules
    from .TF_Rules import set_tf_rules

    if world.options.scenario.value == 0:
        set_tf_rules(world, player)
    else:
        set_q_rules(world, player)
    
    # Connect regions at rule runtime
    connect_regions(world, "Menu", "Show Stage")
    connect_regions(world, "Show Stage", "Kid's Cove")
    connect_regions(world, "Show Stage", "Main Hall")
    if world.options.trade_quest == Toggle.option_true:
        connect_regions(world, "Show Stage", "Trade Machine")
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        connect_regions(world, "Show Stage", "Levelsanity")
    connect_regions(world, "Show Stage", "Grindy")
    connect_regions(world, "Main Hall", "Men's Bathroom")
    if world.options.fem_rods == Toggle.option_true or world.options.scenario.value == 1:
        connect_regions(world, "Main Hall", "Women's Bathroom")
    else:
        connect_regions(world, "Main Hall", "Women's Bathroom", FightStage("endgame"))
    connect_regions(world, "Main Hall", "Parts/Service")
    connect_regions(world, "Main Hall", "Office Hall")
    connect_regions(world, "Office Hall", "Party Room 4")
    connect_regions(world, "Office Hall", "Party Room 3")
    connect_regions(world, "Office Hall", "Party Room 1")
    connect_regions(world, "Office Hall", "Party Room 2")
    connect_regions(world, "Office Hall", "Office")
    connect_regions(world, "Party Room 1", "Left Vent")
    connect_regions(world, "Party Room 2", "Right Vent")
    connect_regions(world, "Left Vent", "Office")
    connect_regions(world, "Right Vent", "Office")
    essence = "B.B.'s Essence" if world.options.scenario.value == 0 else "Toy Animatronics' Essence"
    connect_regions(world, "Office", "Cave of the Past", FightStage("endgame") & Has(essence, count=4))
    connect_regions(world, "Cave of the Past", "B.B.'s Lair")
    connect_regions(world, "B.B.'s Lair", "B.B. Giygas")
    if world.options.difficulty.value > 0:
        connect_regions(world, "Show Stage", "Show Stage Proud")
        connect_regions(world, "Kid's Cove", "Kid's Cove Proud")
        connect_regions(world, "Women's Bathroom", "Women's Bathroom Proud")
        connect_regions(world, "Men's Bathroom", "Men's Bathroom Proud")
        connect_regions(world, "Parts/Service", "Parts/Service Proud")
        connect_regions(world, "Office Hall", "Office Hall Proud")
        connect_regions(world, "Party Room 1", "Party Room 1 Proud")
        connect_regions(world, "Party Room 2", "Party Room 2 Proud")
        connect_regions(world, "Party Room 3", "Party Room 3 Proud")
        connect_regions(world, "Party Room 4", "Party Room 4 Proud")
        connect_regions(world, "Office", "Office Proud")
    if world.options.difficulty.value == 2:
        connect_regions(world, "Kid's Cove", "Kid's Cove Critical")
        connect_regions(world, "Women's Bathroom", "Women's Bathroom Critical")
        connect_regions(world, "Men's Bathroom", "Men's Bathroom Critical")
        connect_regions(world, "Party Room 1", "Party Room 1 Critical")
        connect_regions(world, "Party Room 2", "Party Room 2 Critical")
        connect_regions(world, "Party Room 3", "Party Room 3 Critical")
        connect_regions(world, "Party Room 4", "Party Room 4 Critical")
        connect_regions(world, "Office", "Office Critical")
    if world.options.scenario.value == 0:
        connect_regions(world, "Kid's Cove", "Kid's Cove B.B.", Has("Kid's Cove B.B.") & FightStage("almostlategame"))
        connect_regions(world, "Main Hall", "Main Hall B.B.", Has("Main Hall B.B.") & FightStage("earlygame"))
        connect_regions(world, "Party Room 3", "Party Room 3 B.B.", Has("Party Room 3 B.B.") & FightStage("midgame"))
        connect_regions(world, "Office", "Office B.B.", Has("Office B.B.") & FightStage("lategame"))
        if world.options.goal.value == 1:
            connect_regions(world, "B.B. Giygas", "Refurbs")

    world.set_completion_rule(Has("Victory"))