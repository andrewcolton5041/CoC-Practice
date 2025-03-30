import dice_roll as dr


def get_age_modifiers(age):
    """
    Returns a dictionary of age-based modifications based on Call of Cthulhu rules.

    Keys:
        edu_checks: Number of EDU improvement attempts
        app_loss: Appearance loss in points
        phys_loss: Total physical stat loss to STR/CON/DEX
        teen_mods: Boolean flag for special age <= 19 modifiers
    """
    if age <= 19:
        return {"edu_checks": 0, "app_loss": 0, "phys_loss": 0, "teen_mods": True}
    elif age <= 39:
        return {"edu_checks": 1, "app_loss": 0, "phys_loss": 0, "teen_mods": False}
    elif age <= 49:
        return {"edu_checks": 2, "app_loss": 5, "phys_loss": 5, "teen_mods": False}
    elif age <= 59:
        return {"edu_checks": 3, "app_loss": 10, "phys_loss": 10, "teen_mods": False}
    elif age <= 69:
        return {"edu_checks": 4, "app_loss": 15, "phys_loss": 20, "teen_mods": False}
    elif age <= 79:
        return {"edu_checks": 4, "app_loss": 20, "phys_loss": 40, "teen_mods": False}
    elif age <= 89:
        return {"edu_checks": 4, "app_loss": 25, "phys_loss": 80, "teen_mods": False}
    else:
        raise ValueError("Age must be between 15 and 89.")


def apply_edu_improvement(attributes, attempts):
    """
    Attempts to improve the Education stat up to a maximum of 99.

    Parameters:
        attributes (dict): Character's attribute dictionary
        attempts (int): Number of times to attempt EDU improvement
    """
    for _ in range(attempts):
        edu = attributes.get("Education", 0)
        if edu < 99 and improvement_check(edu):
            gain = dr.roll_dice("1D10")
            attributes["Education"] = min(99, edu + gain)


def apply_teen_modifiers(attributes):
    """
    Applies stat penalties and rerolls best of 2 for Luck if character is 15-19 years old.

    Parameters:
        attributes (dict): Character's attribute dictionary
    """
    attributes["Strength"] -= 5
    attributes["Size"] -= 5
    attributes["Education"] -= 5

    # Roll luck twice and keep the better result
    luck1 = dr.roll_dice("3D6 * 5")
    luck2 = dr.roll_dice("3D6 * 5")
    attributes["Luck"] = max(luck1, luck2)


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
