from BaseClasses import CollectionState, MultiWorld, Location, Region, Item
from typing import TYPE_CHECKING
from .Options import Toggle

if TYPE_CHECKING:
    from . import FNaFB2World

# I LOVE CIRCULAR IMPORTS WOOOOOOOOO
def _can_fight_earlygame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_earlygame
    return can_fight_earlygame(world, state, player)

def _can_fight_midgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_midgame
    return can_fight_midgame(world, state, player)

def _can_fight_postmidgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_postmidgame
    return can_fight_postmidgame(world, state, player)

def _can_fight_almostlategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_almostlategame
    return can_fight_almostlategame(world, state, player)

def _can_fight_lategame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_lategame
    return can_fight_lategame(world, state, player)

def _can_fight_endgame(world: "FNaFB2World", state: CollectionState, player: int) -> bool:
    from .Rules import can_fight_endgame
    return can_fight_endgame(world, state, player)


def set_q_rules(world: "FNaFB2World", player: int):
    # Bosses
    world.get_location("Party Room 4 - Withered Foxy").access_rule = \
        lambda state: _can_fight_midgame(world, state, player) and state.has("Sex Toy", player)
    world.get_location("Party Room 1 - Withered Bonnie").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 2 - Withered Chica").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 3 - Withered Freddy").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 4 - Withered Foxy Rematch").access_rule = \
        lambda state: _can_fight_lategame(world, state, player)
    
    # Cameras
    world.get_location("Show Stage - Camera").access_rule = \
        lambda state: _can_fight_earlygame(world, state, player)
    world.get_location("Game Room - Camera").access_rule = \
        lambda state: _can_fight_earlygame(world, state, player)
    world.get_location("Prize Corner - Camera").access_rule = \
        lambda state: _can_fight_earlygame(world, state, player)
    world.get_location("Main Hall - Camera").access_rule = \
        lambda state: _can_fight_midgame(world, state, player)
    world.get_location("Kid's Cove - Camera").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Parts/Service - Camera").access_rule = \
        lambda state: _can_fight_midgame(world, state, player)
    world.get_location("Office - Camera").access_rule = \
        lambda state: _can_fight_endgame(world, state, player)
    world.get_location("Left Vent - Camera").access_rule = \
        lambda state: _can_fight_lategame(world, state, player)
    world.get_location("Right Vent - Camera").access_rule = \
        lambda state: _can_fight_lategame(world, state, player)
    world.get_location("Party Room 1 - Camera").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 2 - Camera").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 3 - Camera").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)
    world.get_location("Party Room 4 - Camera").access_rule = \
        lambda state: _can_fight_almostlategame(world, state, player)

    # General
    if world.options.difficulty.value > 0:
        world.get_location("Show Stage - Lucky Soda Chest").access_rule = \
            lambda state: _can_fight_almostlategame(world, state, player)
        world.get_location("Show Stage - Double Pizza Chest").access_rule = \
            lambda state: _can_fight_lategame(world, state, player)
    world.get_location("Right Vent - Toy Bonnie").access_rule = \
        lambda state: state.has("Stick", player)
    world.get_location("Show Stage - The Puppet").access_rule = \
        lambda state: _can_fight_earlygame(world, state, player)
    world.get_location("Show Stage - The Second Puppet").access_rule = \
        lambda state: _can_fight_earlygame(world, state, player)

    # Story Quests
    world.get_location("Kid's Cove - Taunt Mangle with Sex Toy").access_rule = \
        lambda state: state.has("Sex Toy", player, 2)
    world.get_location("Vending Machine - Turn in Sex Toy Voucher").access_rule = \
        lambda state: state.has("Sex Toy Voucher", player) and _can_fight_lategame(world, state, player)

    # Enemy Trade Item Drops
    if world.options.trade_quest == Toggle.option_true:
        world.get_location("Dining Area - Trade Beta Voucher").access_rule = \
            lambda state: _can_fight_earlygame(world, state, player)
        world.get_location("Dining Area - Trade Gamma Voucher").access_rule = \
            lambda state: _can_fight_midgame(world, state, player)
        world.get_location("Dining Area - Trade Delta Voucher").access_rule = \
            lambda state: _can_fight_almostlategame(world, state, player)
        world.get_location("Dining Area - Trade Omega Voucher").access_rule = \
            lambda state: _can_fight_lategame(world, state, player)

    # Cassettes
    if world.options.difficulty.value > 0:
        world.get_location("Show Stage - Cassette Radar Chest").access_rule = \
            lambda state: _can_fight_lategame(world, state, player)
        world.get_location("Kid's Cove - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Parts/Service - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Men's Bathroom - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Women's Bathroom - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Office - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Office Hall - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Party Room 1 - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Party Room 2 - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Party Room 3 - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Party Room 4 - Cassette").access_rule = \
            lambda state: state.has("Cassette Radar", player)
        world.get_location("Office - Rap God").access_rule = \
            lambda state: _can_fight_endgame(world, state, player) and state.has("Cassette Radar", player) and state.has("Cassette", player, 10)

    # Levelsanity
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        for i in range(1, 21):
            if i < 6:
                world.get_location(f"Puppet - Level {i}").access_rule = \
                    lambda state: state.has("Puppet", player)
            elif i < 11:
                world.get_location(f"B.B. - Level {i}").access_rule = \
                    lambda state: _can_fight_earlygame(world, state, player)
                world.get_location(f"The Puppet - Level {i}").access_rule = \
                    lambda state: _can_fight_earlygame(world, state, player) and state.has("The Puppet", player)
            elif i < 16:
                world.get_location(f"B.B. - Level {i}").access_rule = \
                    lambda state: _can_fight_postmidgame(world, state, player)
                world.get_location(f"The Puppet - Level {i}").access_rule = \
                    lambda state: _can_fight_postmidgame(world, state, player) and state.has("The Puppet", player)
            else:
                world.get_location(f"B.B. - Level {i}").access_rule = \
                    lambda state: _can_fight_lategame(world, state, player)
                world.get_location(f"The Puppet - Level {i}").access_rule = \
                    lambda state: _can_fight_lategame(world, state, player) and state.has("The Puppet", player)
