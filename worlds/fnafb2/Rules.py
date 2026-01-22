from BaseClasses import CollectionState, MultiWorld, Location, Region, Item
from .Regions import connect_regions
from Options import Toggle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .__init__ import FNaFB2World

def party_count(state: CollectionState, player: int) -> int:
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

# Check if the player has the party members before adding their power to the calculation
def attack_power(state: CollectionState, player: int) -> int:
    return (
    state.count("Progressive Microphone", player)
    + state.count("Toy Bonnie", player) * state.count("Progressive Guitar", player)
    + state.count("Toy Chica", player) * max((state.count("Progressive Cupcakes", player) - 1), 0) # -1 for the first cupcake
    + state.count("Mangle", player) * state.count("Progressive Hook", player)
    # Withered Animatronics start with Kingly Weapons
    + state.count("Withered Freddy", player) * 5
    + state.count("Withered Bonnie", player) * 5
    + state.count("Withered Chica", player) * 5
    + state.count("Withered Foxy", player) * 5
    )

# This one's a bit of a mess, might have to rethink it at a later time
def skills(state: CollectionState, player: int) -> int:
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


def can_fight_earlygame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 1
        and total_defense(state, player) >= 4 
        and skills(state, player) >= 1
    )


def can_fight_midgame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 3 
        and total_defense(state, player) >= 8
        and party_count(state, player) >= 2
        and skills(state, player) >= 2
    )
    
def can_fight_postmidgame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 6
        and total_defense(state, player) >= 12
        and party_count(state, player) >= 3
        and skills(state, player) >= 4
    )

def can_fight_almostlategame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 10
        and total_defense(state, player) >= 20
        and party_count(state, player) >= 4
        and skills(state, player) >= 6
    )

def can_fight_lategame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 24
        and total_defense(state, player) >= 160
        and party_count(state, player) >= 4
        and skills(state, player) >= 20
    )


def can_fight_endgame(state: CollectionState, player: int) -> bool:
    return (
        attack_power(state, player) >= 40
        and total_defense(state, player) >= 300
        and party_count(state, player) >= 8
        and skills(state, player) >= 25
    )


def set_rules(world: "FNaFB2World", player: int):
    # Bosses
    world.get_location("Party Room 4 - Withered Foxy").access_rule = \
        lambda state: can_fight_midgame(state, player) and state.has("Sex Toy", player)

    # You can only fight Splash Woman with toy freddy
    world.get_location("Women's Bathroom - Splash Woman").access_rule = \
        lambda state: (
            (state.count("Progressive Tophat Slash", player)
            + state.count("Progressive Tophat Dash", player)
            + state.count("Progressive Tophat Crash", player)
            + state.count("Progressive Tophat Smash", player)) >= 3
            and state.count("Progressive Microphone", player) >= 3
            and (
                state.count("Progressive Body Endoskeletons", player)
                + state.count("Progressive Head Endoskeletons", player)
                + state.count("Progressive Pizza Shields", player)
                + state.count("Progressive Caffeine Sodas", player)
                ) >= 10
        )

    world.get_location("The Puppet").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("The Puppet - Rod of Femininity A").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("Party Room 1 - Withered Bonnie").access_rule = \
        lambda state: can_fight_lategame(state, player) and state.has("Toy Bonnie", player)
    world.get_location("Party Room 2 - Withered Chica").access_rule = \
        lambda state: can_fight_lategame(state, player) and state.has("Toy Chica", player)
    world.get_location("Party Room 3 - Withered Freddy").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("Party Room 4 - Withered Foxy Rematch").access_rule = \
        lambda state: can_fight_lategame(state, player) and state.has("Mangle", player)
    world.get_location("The Second Puppet").access_rule = \
        lambda state: can_fight_endgame(state, player)
    world.get_location("The Second Puppet - Rod of Femininity B").access_rule = \
        lambda state: can_fight_endgame(state, player)
    world.get_location("Boss Rush").access_rule = \
        lambda state: can_fight_endgame(state, player)
    # Shops
    world.get_location("Kid's Cove - Protection Hat").access_rule = \
        lambda state: can_fight_almostlategame(state, player)
    world.get_location("Main Hall - Protection Hat").access_rule = \
        lambda state: can_fight_earlygame(state, player)
    world.get_location("Party Room 3 - Protection Hat").access_rule = \
        lambda state: can_fight_midgame(state, player)
    world.get_location("Office - Protection Hat").access_rule = \
        lambda state: can_fight_lategame(state, player)
    
    # Cameras
    world.get_location("Show Stage - Camera").access_rule = \
        lambda state: can_fight_midgame(state, player)
    world.get_location("Game Room - Camera").access_rule = \
        lambda state: can_fight_midgame(state, player)
    world.get_location("Prize Corner - Camera").access_rule = \
        lambda state: can_fight_midgame(state, player)
    world.get_location("Main Hall - Camera").access_rule = \
        lambda state: can_fight_midgame(state, player)
    world.get_location("Kid's Cove - Camera").access_rule = \
        lambda state: can_fight_almostlategame(state, player)
    world.get_location("Parts/Service - Camera").access_rule = \
        lambda state: can_fight_almostlategame(state, player)
    world.get_location("Office - Camera").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("Left Vent - Camera").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("Right Vent - Camera").access_rule = \
        lambda state: can_fight_lategame(state, player)
    world.get_location("Party Room 1 - Camera").access_rule = \
        lambda state: can_fight_postmidgame(state, player)
    world.get_location("Party Room 2 - Camera").access_rule = \
        lambda state: can_fight_postmidgame(state, player)
    world.get_location("Party Room 3 - Camera").access_rule = \
        lambda state: can_fight_postmidgame(state, player)
    world.get_location("Party Room 4 - Camera").access_rule = \
        lambda state: can_fight_postmidgame(state, player)

    # General
    if world.options.difficulty.value > 0:
        world.get_location("Show Stage - Lucky Soda Chest").access_rule = \
            lambda state: can_fight_almostlategame(state, player)
        world.get_location("Show Stage - Double Pizza Chest").access_rule = \
            lambda state: can_fight_lategame(state, player)
    world.get_location("Women's Bathroom - Toy Chica").access_rule = \
        lambda state: state.can_reach_location("Women's Bathroom - Splash Woman", player) and (state.has("Progressive Cupcakes", player) or can_fight_lategame(state, player))
    world.get_location("Right Vent - Toy Bonnie").access_rule = \
        lambda state: state.has("Stick", player)

    world.get_location("Cave of the Past - Dragon Dildo A").access_rule = \
        lambda state: state.has("Stick", player)
    world.get_location("Cave of the Past - Dragon Dildo B").access_rule = \
        lambda state: state.has("Progressive Dragon Dildo", player)
    world.get_location("Cave of the Past - Dragon Dildo C").access_rule = \
        lambda state: state.has("Progressive Dragon Dildo", player, 2)
    world.get_location("Cave of the Past - Dragon Dildo D").access_rule = \
        lambda state: state.has("Progressive Dragon Dildo", player, 3)
    world.get_location("Cave of the Past - Dragon Dildo E").access_rule = \
        lambda state: state.has("Progressive Dragon Dildo", player, 4)
    world.get_location("Cave of the Past - Dragon Dildo F").access_rule = \
        lambda state: state.has("Progressive Dragon Dildo", player, 5)

    # Story Quests
    world.get_location("Turn in Sex Toy Voucher to B.B.").access_rule = \
        lambda state: state.can_reach_location("Kid's Cove - Protection Hat", player) \
            and state.has("Kid's Cove B.B.", player) and state.has("Sex Toy Voucher", player)
    world.get_location("Kid's Cove - Return Sex Toy").access_rule = \
        lambda state: state.has("Sex Toy", player, 2)
    world.get_location("Vending Machine - Turn in Sex Toy Voucher").access_rule = \
        lambda state: state.has("Sex Toy Voucher", player) and can_fight_lategame(state, player)

    # Enemy Trade Item Drops
    if world.options.trade_quest == Toggle.option_true:
        world.get_location("Dining Area - Trade Beta Voucher").access_rule = \
            lambda state: can_fight_earlygame(state, player)
        world.get_location("Dining Area - Trade Gamma Voucher").access_rule = \
            lambda state: can_fight_midgame(state, player)
        world.get_location("Dining Area - Trade Delta Voucher").access_rule = \
            lambda state: can_fight_almostlategame(state, player)
        world.get_location("Dining Area - Trade Omega Voucher").access_rule = \
            lambda state: can_fight_lategame(state, player)

    # Cassettes
    if world.options.difficulty.value > 0:
        world.get_location("Show Stage - Cassette Radar Chest").access_rule = \
            lambda state: can_fight_lategame(state, player)
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
            lambda state: can_fight_endgame(state, player) and state.has("Cassette Radar", player) and state.has("Cassette", player, 10)

    # Keystones
    world.get_location("Kid's Cove - Chest").access_rule = \
        lambda state: can_fight_almostlategame(state, player) and state.has("Mangle", player)
    world.get_location("Women's Bathroom - Chest").access_rule = \
        lambda state: can_fight_almostlategame(state, player) and state.has("Toy Chica", player)
    world.get_location("Office - Left Chest").access_rule = \
        lambda state: can_fight_lategame(state, player) and state.has("Toy Bonnie", player)
    world.get_location("Office - Right Chest").access_rule = \
        lambda state: can_fight_lategame(state, player)
        
    # Critical mode
    if world.options.difficulty.value == 2:
        # You can't fight shadow bonnie with toy animatronics and withered freddy in the party
        world.get_location("Women's Bathroom - Shadow Bonnie").access_rule = \
            lambda state: (
                state.has("Progressive Microphone", player, 6)
                and (state.count("Progressive Tophat Slash", player)
                     + state.count("Progressive Tophat Dash", player)
                     + state.count("Progressive Tophat Crash", player)
                     + state.count("Progressive Tophat Smash", player)) >= 10
                and state.has("Progressive Body Endoskeletons", player, 4)
                and state.has("Progressive Head Endoskeletons", player, 4)
                and state.has("Progressive Pizza Shields", player, 4)
                and state.has("Progressive Caffeine Sodas", player, 4)
                and state.has("Withered Bonnie", player)
                and state.has("Withered Chica", player)
                and state.has("Withered Foxy", player)
            )
        world.get_location("Kid's Cove - Status Bomb Gem").access_rule = \
            lambda state: state.has("Toy Bonnie", player)
        world.get_location("Men's Bathroom - Paravolt Gem").access_rule = \
            lambda state: state.has("Mangle", player)
        world.get_location("Women's Bathroom - Grab Bag Gem").access_rule = \
            lambda state: state.has("Toy Bonnie", player)
        world.get_location("Women's Bathroom - Somnojolt Gem").access_rule = \
            lambda state: state.has("Mangle", player)
        world.get_location("Office - Electroshock Gem").access_rule = \
            lambda state: state.has("Mangle", player)
        world.get_location("Office - Recovery Wing Gem").access_rule = \
            lambda state: state.has("Toy Chica", player)
        world.get_location("Office - Spread Bomb Gem").access_rule = \
            lambda state: state.has("Toy Bonnie", player)
        world.get_location("Party Room 1 - Timer Flip Gem").access_rule = \
            lambda state: state.has("Toy Bonnie", player)
        world.get_location("Party Room 2 - Healing Wing Gem").access_rule = \
            lambda state: state.has("Toy Chica", player)
        world.get_location("Party Room 3 - Curing Wing Gem").access_rule = \
            lambda state: state.has("Toy Chica", player)
        world.get_location("Party Room 4 - Raising Wing Gem").access_rule = \
            lambda state: state.has("Toy Chica", player)
        world.get_location("Party Room 4 - Lightningbolt Gem").access_rule = \
            lambda state: state.has("Mangle", player)

    # Levelsanity
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        for i in range(1, 21):
            if i < 6:
                world.get_location(f"Toy Bonnie - Level {i}").access_rule = \
                    lambda state: state.has("Toy Bonnie", player)
                world.get_location(f"Toy Chica - Level {i}").access_rule = \
                    lambda state: state.has("Toy Chica", player)
                world.get_location(f"Mangle - Level {i}").access_rule = \
                    lambda state: state.has("Mangle", player)
            elif i < 11:
                world.get_location(f"Toy Freddy - Level {i}").access_rule = \
                    lambda state: can_fight_earlygame(state, player)
                world.get_location(f"Toy Bonnie - Level {i}").access_rule = \
                    lambda state: can_fight_earlygame(state, player) and state.has("Toy Bonnie", player)
                world.get_location(f"Toy Chica - Level {i}").access_rule = \
                    lambda state: can_fight_earlygame(state, player) and state.has("Toy Chica", player)
                world.get_location(f"Mangle - Level {i}").access_rule = \
                    lambda state: can_fight_earlygame(state, player) and state.has("Mangle", player)
            elif i < 16:
                world.get_location(f"Toy Freddy - Level {i}").access_rule = \
                    lambda state: can_fight_midgame(state, player)
                world.get_location(f"Toy Bonnie - Level {i}").access_rule = \
                    lambda state: can_fight_midgame(state, player) and state.has("Toy Bonnie", player)
                world.get_location(f"Toy Chica - Level {i}").access_rule = \
                    lambda state: can_fight_midgame(state, player) and state.has("Toy Chica", player)
                world.get_location(f"Mangle - Level {i}").access_rule = \
                    lambda state: can_fight_midgame(state, player) and state.has("Mangle", player)
            else:
                world.get_location(f"Toy Freddy - Level {i}").access_rule = \
                    lambda state: can_fight_almostlategame(state, player)
                world.get_location(f"Toy Bonnie - Level {i}").access_rule = \
                    lambda state: can_fight_almostlategame(state, player) and state.has("Toy Bonnie", player)
                world.get_location(f"Toy Chica - Level {i}").access_rule = \
                    lambda state: can_fight_almostlategame(state, player) and state.has("Toy Chica", player)
                world.get_location(f"Mangle - Level {i}").access_rule = \
                    lambda state: can_fight_almostlategame(state, player) and state.has("Mangle", player)
        
        world.get_location("Toy Freddy - Tophat Dash").access_rule = \
            lambda state: can_fight_earlygame(state, player)
        world.get_location("Toy Freddy - Tophat Crash").access_rule = \
            lambda state: can_fight_midgame(state, player)
        world.get_location("Toy Freddy - Tophat Smash").access_rule = \
            lambda state: can_fight_lategame(state, player)
        world.get_location("Toy Freddy - Use Tophat Slash 20 times").access_rule = \
            lambda state: state.has("Progressive Tophat Slash", player)
        world.get_location("Toy Freddy - Use Tophat Slash 40 times").access_rule = \
            lambda state: state.has("Progressive Tophat Slash", player)
        world.get_location("Toy Freddy - Use Tophat Dash 20 times").access_rule = \
            lambda state: state.has("Progressive Tophat Dash", player)
        world.get_location("Toy Freddy - Use Tophat Dash 40 times").access_rule = \
            lambda state: state.has("Progressive Tophat Dash", player)
        world.get_location("Toy Freddy - Use Tophat Crash 20 times").access_rule = \
            lambda state: state.has("Progressive Tophat Crash", player)
        world.get_location("Toy Freddy - Use Tophat Dash 40 times").access_rule = \
            lambda state: state.has("Progressive Tophat Crash", player)
        world.get_location("Toy Freddy - Use Tophat Smash 20 times").access_rule = \
            lambda state: state.has("Progressive Tophat Smash", player)
        world.get_location("Toy Freddy - Use Tophat Smash 40 times").access_rule = \
            lambda state: state.has("Progressive Tophat Smash", player)

        world.get_location("Mangle - Electroshock").access_rule = \
            lambda state: state.has("Mangle", player)
        world.get_location("Mangle - Paravolt").access_rule = \
            lambda state: can_fight_earlygame(state, player) and state.has("Mangle", player)
        world.get_location("Mangle - Somnojolt").access_rule = \
            lambda state: can_fight_midgame(state, player) and state.has("Mangle", player)
        world.get_location("Mangle - Lightningbolt").access_rule = \
            lambda state: can_fight_almostlategame(state, player) and state.has("Mangle", player)
        
        world.get_location("Toy Chica - Healing Wing").access_rule = \
            lambda state: state.has("Toy Chica", player)
        world.get_location("Toy Chica - Curing Wing").access_rule = \
            lambda state: can_fight_earlygame(state, player) and state.has("Toy Chica", player)
        world.get_location("Toy Chica - Raising Wing").access_rule = \
            lambda state: can_fight_midgame(state, player) and state.has("Toy Chica", player)
        world.get_location("Toy Chica - Recovery Wing").access_rule = \
            lambda state: can_fight_almostlategame(state, player) and state.has("Toy Chica", player)
        
        world.get_location("Toy Bonnie - Grab Bag").access_rule = \
            lambda state: state.has("Toy Bonnie", player)
        world.get_location("Toy Bonnie - Status Bomb").access_rule = \
            lambda state: can_fight_earlygame(state, player) and state.has("Toy Bonnie", player)
        world.get_location("Toy Bonnie - Spread Bomb").access_rule = \
            lambda state: can_fight_midgame(state, player) and state.has("Toy Bonnie", player)
        world.get_location("Toy Bonnie - Timer Flip").access_rule = \
            lambda state: can_fight_almostlategame(state, player) and state.has("Toy Bonnie", player)
        
        world.get_location("Toy Freddy - Death Inhale").access_rule = \
            lambda state: state.has("Tophat Keystone", player)
        world.get_location("Toy Bonnie - Terror Fever").access_rule = \
            lambda state: state.has("Terror Keystone", player) and state.has("Toy Bonnie", player)
        world.get_location("Toy Chica - Avian Strike").access_rule = \
            lambda state: state.has("Avian Keystone", player) and state.has("Toy Chica", player)
        world.get_location("Mangle - Disassembly").access_rule = \
            lambda state: state.has("Assembly Keystone", player) and state.has("Mangle", player)

    # Connect regions at rule runtime
    connect_regions(world, "Menu", "Show Stage")
    connect_regions(world, "Show Stage", "Kid's Cove")
    connect_regions(world, "Show Stage", "Kid's Cove B.B.", lambda state: state.has("Kid's Cove B.B.", player))
    connect_regions(world, "Show Stage", "Main Hall")
    if world.options.trade_quest == Toggle.option_true:
        connect_regions(world, "Show Stage", "Trade Machine")
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        connect_regions(world, "Show Stage", "Levelsanity")
    connect_regions(world, "Show Stage", "Grindy")
    connect_regions(world, "Main Hall", "Main Hall B.B.", lambda state: state.has("Main Hall B.B.", player))
    connect_regions(world, "Main Hall", "Men's Bathroom") 
    if world.options.fem_rods == Toggle.option_true:
        connect_regions(world, "Main Hall", "Women's Bathroom")
    else:
        connect_regions(world, "Main Hall", "Women's Bathroom", lambda state: can_fight_endgame(state, player))
    connect_regions(world, "Main Hall", "Parts/Service")
    connect_regions(world, "Main Hall", "Office Hall")
    connect_regions(world, "Office Hall", "Party Room 4")
    connect_regions(world, "Office Hall", "Party Room 3")
    connect_regions(world, "Party Room 3", "Party Room 3 B.B.", lambda state: state.has("Party Room 3 B.B.", player))
    connect_regions(world, "Office Hall", "Party Room 1")
    connect_regions(world, "Office Hall", "Party Room 2")
    connect_regions(world, "Office Hall", "Office")
    connect_regions(world, "Party Room 1", "Left Vent")
    connect_regions(world, "Party Room 2", "Right Vent")
    connect_regions(world, "Left Vent", "Office")
    connect_regions(world, "Right Vent", "Office")
    connect_regions(world, "Office", "Office B.B.", lambda state: state.has("Office B.B.", player))
    connect_regions(world, "Office", "Cave of the Past", lambda state: can_fight_endgame(state, player) and state.has("B.B.'s Essence", player, 4))
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
    if world.options.goal.value == 1:
        connect_regions(world, "B.B. Giygas", "Refurbs")


    # Win Condition
    world.options.completion_condition = lambda state: state.has("Victory", player)