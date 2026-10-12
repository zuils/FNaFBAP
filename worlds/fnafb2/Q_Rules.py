from typing import TYPE_CHECKING

from .Options import Toggle
from rule_builder.rules import Has

if TYPE_CHECKING:
    from . import FNaFB2World


def set_q_rules(world: "FNaFB2World", player: int):
    from .Rules import CameraCount, FightStage

    def set_rule(location_name: str, rule) -> None:
        world.set_rule(world.get_location(location_name), rule)

    early = FightStage("earlygame")
    mid = FightStage("midgame")
    almostlate = FightStage("almostlategame")
    late = FightStage("lategame")
    end = FightStage("endgame")

    # Bosses
    set_rule("Party Room 4 - Withered Foxy", mid & Has("Sex Toy"))
    set_rule("Party Room 1 - Withered Bonnie", CameraCount(10))
    set_rule("Party Room 2 - Withered Chica", CameraCount(11))
    set_rule("Party Room 3 - Withered Freddy", CameraCount(12))
    set_rule("Party Room 4 - Withered Foxy Rematch", CameraCount(13))

    # Cameras
    for location_name in ("Show Stage - Camera", "Game Room - Camera", "Prize Corner - Camera"):
        set_rule(location_name, early)
    set_rule("Main Hall - Camera", mid)
    set_rule("Kid's Cove - Camera", almostlate)
    set_rule("Parts/Service - Camera", mid)
    set_rule("Office - Camera", end)
    set_rule("Left Vent - Camera", late)
    set_rule("Right Vent - Camera", late)
    for location_name in ("Party Room 1 - Camera", "Party Room 2 - Camera", "Party Room 3 - Camera", "Party Room 4 - Camera"):
        set_rule(location_name, almostlate)

    # General
    if world.options.difficulty.value > 0:
        set_rule("Show Stage - Lucky Soda Chest", almostlate)
        set_rule("Show Stage - Double Pizza Chest", late)
    set_rule("Right Vent - Toy Bonnie", Has("Stick"))
    set_rule("Show Stage - The Puppet", early)
    set_rule("Show Stage - The Second Puppet", early)

    # Story Quests
    set_rule("Kid's Cove - Taunt Mangle with the Sex Toy", Has("Sex Toy", count=2))
    set_rule("Vending Machine - Turn in Sex Toy Voucher", Has("Sex Toy Voucher") & late)

    # Enemy Trade Item Drops
    if world.options.trade_quest == Toggle.option_true:
        set_rule("Dining Area - Trade Beta Voucher", early)
        set_rule("Dining Area - Trade Gamma Voucher", mid)
        set_rule("Dining Area - Trade Delta Voucher", almostlate)
        set_rule("Dining Area - Trade Omega Voucher", late)

    # Cassettes
    if world.options.difficulty.value > 0:
        set_rule("Show Stage - Cassette Radar Chest", late)
        for location_name in (
            "Kid's Cove - Cassette", "Parts/Service - Cassette", "Men's Bathroom - Cassette",
            "Women's Bathroom - Cassette", "Office - Cassette", "Office Hall - Cassette",
            "Party Room 1 - Cassette", "Party Room 2 - Cassette", "Party Room 3 - Cassette",
            "Party Room 4 - Cassette",
        ):
            set_rule(location_name, Has("Cassette Radar"))
        set_rule("Office - Rap God", end & Has("Cassette Radar") & Has("Cassette", count=10))

    # Levelsanity
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        for i in range(1, 21):
            if i < 11:
                set_rule(f"The Puppet - Level {i}", Has("The Puppet"))
            else:
                set_rule(f"B.B. - Level {i}", Has("Token Throw") | Has("Flying Fright"))
                set_rule(f"The Puppet - Level {i}", late & Has("The Puppet"))

        for location_name, min_cameras in (
            ("B.B. - Learn Curing Wing", 1),
            ("B.B. - Learn Smoke Lens", 3),
            ("B.B. - Learn Poison Lens", 5),
            ("B.B. - Learn Raising Wing", 7),
            ("B.B. - Learn Confusion Lens", 9),
            ("B.B. - Learn Spread Bomb", 11),
        ):
            set_rule(location_name, CameraCount(min_cameras))
