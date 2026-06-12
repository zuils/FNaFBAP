from BaseClasses import CollectionState, MultiWorld, Location, Region, Item
from .Regions import connect_regions
from .Normal_Rules import set_normal_rules
from .Q_Rules import set_q_rules
from Options import Toggle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import FNaFB2World

def party_count(world: "FNaFB2World", state: CollectionState, player: int) -> int:
    if world.options.scenario.value == 0:
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
    
    mic_damage = [0, 1, 2, 3, 4, 5, 6][mic]
    rod_damage = [0, 5, 6][rod]
    dragon_damage = [0, 3, 4, 5, 5, 6, 6][dragon]
    
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

# This one's a bit of a mess, might have to rethink it at a later time
def skills(world: "FNaFB2World", state: CollectionState, player: int) -> int:
    if world.options.scenario.value == 0:
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
            + state.count("The Puppet", player) * (
                state.count("Poison Lens", player)
                + state.count("Spread Bomb", player)
                + state.count("Smoke Lens", player)
                + state.count("Confusion Lens", player)
                + state.count("Death", player) * 5 # Death has a 70% chance to instakill every enemy including bosses
                + state.count("Toredor March", player)
            )
        )

def can_fight_earlygame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 1
            and total_defense(state, player) >= 4 
            and skills(world, state, player) >= 1
        )
    else:
        return True

def can_fight_midgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 3 
            and total_defense(state, player) >= 8
            and party_count(world, state, player) >= 2
            and skills(world, state, player) >= 2
        )
    else:
        return skills(world, state, player) >= 2

def can_fight_postmidgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 6
            and total_defense(state, player) >= 12
            and party_count(world, state, player) >= 3
            and skills(world, state, player) >= 4
        )
    else:
        return party_count(world, state, player) > 1 and skills(world, state, player) >= 4

def can_fight_almostlategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 10
            and total_defense(state, player) >= 20
            and party_count(world, state, player) >= 4
            and skills(world, state, player) >= 6
        )
    else:
        return party_count(world, state, player) > 1 and skills(world, state, player) >= 6

def can_fight_lategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 24
            and total_defense(state, player) >= 160
            and party_count(world, state, player) >= 6
            and skills(world, state, player) >= 20
        )
    else:
        return party_count(world, state, player) > 1 and skills(world, state, player) >= 8

def can_fight_endgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    if world.options.scenario.value == 0:
        return (
            total_attack(state, player) >= 40
            and total_defense(state, player) >= 300
            and party_count(world, state, player) >= 7
            and skills(world, state, player) >= 25
        )
    else:
        return party_count(world, state, player) > 1 and skills(world, state, player) >= 10

def set_rules(world: "FNaFB2World", player: int):
    if world.options.scenario.value == 0:
        set_normal_rules(world, player)
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
        connect_regions(world, "Main Hall", "Women's Bathroom", lambda state: can_fight_endgame(world, state, player))
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
    connect_regions(world, "Office", "Cave of the Past", lambda state: can_fight_endgame(world, state, player) \
        and state.has("B.B.'s Essence" if world.options.scenario.value == 0 else "Toy Animatronics' Essence", player, 4))
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
        connect_regions(world, "Kid's Cove", "Kid's Cove B.B.", lambda state: state.has("Kid's Cove B.B.", player))
        connect_regions(world, "Main Hall", "Main Hall B.B.", lambda state: state.has("Main Hall B.B.", player))
        connect_regions(world, "Party Room 3", "Party Room 3 B.B.", lambda state: state.has("Party Room 3 B.B.", player))
        connect_regions(world, "Office", "Office B.B.", lambda state: state.has("Office B.B.", player))
        if world.options.goal.value == 1:
            connect_regions(world, "B.B. Giygas", "Refurbs")

    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)