from typing import TYPE_CHECKING
from .Options import Toggle
from rule_builder.rules import CanReachLocation, Has, HasFromList

if TYPE_CHECKING:
    from . import FNaFB2World

def set_tf_rules(world: "FNaFB2World", player: int):
    from .Rules import CameraCount, FightStage

    def set_rule(location_name: str, rule) -> None:
        world.set_rule(world.get_location(location_name), rule)

    early = FightStage("earlygame")
    mid = FightStage("midgame")
    postmid = FightStage("postmidgame")
    almostlate = FightStage("almostlategame")
    late = FightStage("lategame")
    end = FightStage("endgame")

    # Bosses
    set_rule("Party Room 4 - Withered Foxy", mid & Has("Sex Toy"))

    # You can only fight Splash Woman with toy freddy
    set_rule("Women's Bathroom - Splash Woman", 
        HasFromList(
            "Progressive Tophat Slash",
            "Progressive Tophat Dash",
            "Progressive Tophat Crash",
            "Progressive Tophat Smash",
            count=3,
        ) & Has("Progressive Microphone", count=3) 
        & HasFromList(
            "Progressive Body Endoskeletons",
            "Progressive Head Endoskeletons",
            "Progressive Pizza Shields",
            "Progressive Caffeine Sodas",
            count=10,
        ),
    )
    set_rule("Show Stage - The Puppet", late)
    set_rule("Women's Bathroom - The Puppet (Rod of Femininity A)", late)
    set_rule("Party Room 1 - Withered Bonnie", CameraCount(10) & Has("Toy Bonnie"))
    set_rule("Party Room 2 - Withered Chica", CameraCount(11) & Has("Toy Chica"))
    set_rule("Party Room 3 - Withered Freddy", CameraCount(12))
    set_rule("Party Room 4 - Withered Foxy Rematch", CameraCount(13) & Has("Mangle"))
    set_rule("Show Stage - The Second Puppet", end)
    set_rule("Women's Bathroom - The Second Puppet (Rod of Femininity B)", end)
    set_rule("Parts/Service - Boss Rush", end)

    # Shops
    set_rule("Kid's Cove - Protection Hat", almostlate)
    set_rule("Main Hall - Protection Hat", early)
    set_rule("Party Room 3 - Protection Hat", mid)
    set_rule("Office - Protection Hat", late)
    
    # Cameras
    for location_name in (
        "Show Stage - Camera",
        "Game Room - Camera",
        "Prize Corner - Camera",
        "Main Hall - Camera",
        "Parts/Service - Camera",
    ):
        set_rule(location_name, mid)
    for location_name in (
        "Party Room 1 - Camera",
        "Party Room 2 - Camera",
        "Party Room 3 - Camera",
        "Party Room 4 - Camera",
    ):
        set_rule(location_name, postmid)
    set_rule("Kid's Cove - Camera", almostlate)
    for location_name in ("Office - Camera", "Left Vent - Camera", "Right Vent - Camera"):
        set_rule(location_name, late)

    # General
    if world.options.difficulty.value > 0:
        set_rule("Show Stage - Lucky Soda Chest", almostlate)
        set_rule("Show Stage - Double Pizza Chest", late)
    set_rule(
        "Women's Bathroom - Toy Chica",
        CanReachLocation("Women's Bathroom - Splash Woman")
        & (Has("Progressive Cupcakes") | late),
    )
    set_rule("Right Vent - Toy Bonnie", Has("Stick"))

    set_rule("Cave of the Past - Dragon Dildo A", Has("Stick"))
    for count, suffix in enumerate(("B", "C", "D", "E", "F"), start=1):
        set_rule(f"Cave of the Past - Dragon Dildo {suffix}", Has("Progressive Dragon Dildo", count=count))

    # Story Quests
    set_rule(
        "Kid's Cove - Turn in Sex Toy Voucher to B.B.",
        CanReachLocation("Kid's Cove - Protection Hat") & Has("Kid's Cove B.B.") & Has("Sex Toy Voucher"),
    )
    set_rule("Kid's Cove - Return Sex Toy", Has("Sex Toy", count=2))
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

    # Keystones
    set_rule("Kid's Cove - Chest", almostlate & Has("Mangle"))
    set_rule("Women's Bathroom - Chest", almostlate & Has("Toy Chica"))
    set_rule("Office - Left Chest", late & Has("Toy Bonnie"))
    set_rule("Office - Right Chest", late)
        
    # Critical mode
    if world.options.difficulty.value == 2:
        # You can't fight shadow bonnie with toy animatronics and withered freddy in the party
        set_rule(
            "Women's Bathroom - Shadow Bonnie",
            Has("Progressive Microphone", count=6)
            & HasFromList(
                "Progressive Tophat Slash",
                "Progressive Tophat Dash",
                "Progressive Tophat Crash",
                "Progressive Tophat Smash",
                count=10,
            )
            & Has("Progressive Body Endoskeletons", count=4)
            & Has("Progressive Head Endoskeletons", count=4)
            & Has("Progressive Pizza Shields", count=4)
            & Has("Progressive Caffeine Sodas", count=4)
            & Has("Withered Bonnie")
            & Has("Withered Chica")
            & Has("Withered Foxy"),
        )
        for location_name, character in (
            ("Kid's Cove - Status Bomb Gem", "Toy Bonnie"),
            ("Men's Bathroom - Paravolt Gem", "Mangle"),
            ("Women's Bathroom - Grab Bag Gem", "Toy Bonnie"),
            ("Women's Bathroom - Somnojolt Gem", "Mangle"),
            ("Office - Electroshock Gem", "Mangle"),
            ("Office - Recovery Wing Gem", "Toy Chica"),
            ("Office - Spread Bomb Gem", "Toy Bonnie"),
            ("Party Room 1 - Timer Flip Gem", "Toy Bonnie"),
            ("Party Room 2 - Healing Wing Gem", "Toy Chica"),
            ("Party Room 3 - Curing Wing Gem", "Toy Chica"),
            ("Party Room 4 - Raising Wing Gem", "Toy Chica"),
            ("Party Room 4 - Lightningbolt Gem", "Mangle"),
        ):
            set_rule(location_name, Has(character))

    # Levelsanity
    if world.options.levelsanity == Toggle.option_true and world.options.difficulty.value < 2:
        for i in range(1, 21):
            if i < 6:
                set_rule(f"Toy Bonnie - Level {i}", Has("Toy Bonnie"))
                set_rule(f"Toy Chica - Level {i}", Has("Toy Chica"))
                set_rule(f"Mangle - Level {i}", Has("Mangle"))
            elif i < 11:
                stage = early
                set_rule(f"Toy Freddy - Level {i}", stage)
                set_rule(f"Toy Bonnie - Level {i}", stage & Has("Toy Bonnie"))
                set_rule(f"Toy Chica - Level {i}", stage & Has("Toy Chica"))
                set_rule(f"Mangle - Level {i}", stage & Has("Mangle"))
            elif i < 16:
                stage = mid
                set_rule(f"Toy Freddy - Level {i}", stage)
                set_rule(f"Toy Bonnie - Level {i}", stage & Has("Toy Bonnie"))
                set_rule(f"Toy Chica - Level {i}", stage & Has("Toy Chica"))
                set_rule(f"Mangle - Level {i}", stage & Has("Mangle"))
            else:
                stage = almostlate
                set_rule(f"Toy Freddy - Level {i}", stage)
                set_rule(f"Toy Bonnie - Level {i}", stage & Has("Toy Bonnie"))
                set_rule(f"Toy Chica - Level {i}", stage & Has("Toy Chica"))
                set_rule(f"Mangle - Level {i}", stage & Has("Mangle"))
        
        set_rule("Toy Freddy - Learn Tophat Dash", early)
        set_rule("Toy Freddy - Learn Tophat Crash", mid)
        set_rule("Toy Freddy - Learn Tophat Smash", late)
        for name in ("Slash", "Dash", "Crash", "Smash"):
            item_name = f"Progressive Tophat {name}"
            for uses in (20, 40):
                set_rule(f"Toy Freddy - Use Tophat {name} {uses} times", Has(item_name))

        set_rule("Mangle - Learn Electroshock", Has("Mangle"))
        set_rule("Mangle - Learn Paravolt", early & Has("Mangle"))
        set_rule("Mangle - Learn Somnojolt", mid & Has("Mangle"))
        set_rule("Mangle - Learn Lightningbolt", almostlate & Has("Mangle"))
        
        set_rule("Toy Chica - Learn Healing Wing", Has("Toy Chica"))
        set_rule("Toy Chica - Learn Curing Wing", early & Has("Toy Chica"))
        set_rule("Toy Chica - Learn Raising Wing", mid & Has("Toy Chica"))
        set_rule("Toy Chica - Learn Recovery Wing", almostlate & Has("Toy Chica"))
        
        set_rule("Toy Bonnie - Learn Grab Bag", Has("Toy Bonnie"))
        set_rule("Toy Bonnie - Learn Status Bomb", early & Has("Toy Bonnie"))
        set_rule("Toy Bonnie - Learn Spread Bomb", mid & Has("Toy Bonnie"))
        set_rule("Toy Bonnie - Learn Timer Flip", almostlate & Has("Toy Bonnie"))
        
        set_rule("Toy Freddy - Learn Death Inhale", Has("Tophat Keystone"))
        set_rule("Toy Bonnie - Learn Terror Fever", Has("Terror Keystone") & Has("Toy Bonnie"))
        set_rule("Toy Chica - Learn Avian Strike", Has("Avian Keystone") & Has("Toy Chica"))
        set_rule("Mangle - Learn Disassembly", Has("Assembly Keystone") & Has("Mangle"))