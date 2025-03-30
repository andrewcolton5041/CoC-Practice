import dice_roll as dr

def improvement_check(stat):
    """
    Rolls 1D100 and checks if it's greater than the given stat.
    Used for education improvement in CoC rules.
    """
    return dr.roll_dice("1D100") > stat

def success_check(stat):
    """
    Rolls 1D100 and determines success level based on the character's stat.

    Returns:
        One of: "Extreme Success", "Hard Success", "Regular Success", or "Fumble"
    """
    roll = dr.roll_dice("1D100")

    if roll <= stat / 5:
        return "Extreme Success"
    elif roll <= stat / 2:
        return "Hard Success"
    elif roll <= stat:
        return "Regular Success"
    elif (stat <= 50 and 96 <= roll <= 100) or (stat > 50 and roll == 100):
        return "Fumble"
    else:
        return "Failure"