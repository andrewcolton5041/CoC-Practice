import cocCharStatGen as gen
import coc_rules as rules
import dice_roll as dr


class Character:
    def __init__(self, name, age):
        if not (15 <= age <= 89):
            raise ValueError("Age must be between 15 and 89 for character creation.")

        self.name = name
        self.age = age

        # Generate base attributes
        self.attributes = {
            "Strength": gen.chargen_funcs["str"](),
            "Constitution": gen.chargen_funcs["con"](),
            "Size": gen.chargen_funcs["siz"](),
            "Dexterity": gen.chargen_funcs["dex"](),
            "Appearance": gen.chargen_funcs["app"](),
            "Intelligence": gen.chargen_funcs["int"](),
            "Power": gen.chargen_funcs["pow"](),
            "Education": gen.chargen_funcs["edu"](),
            "Luck": gen.chargen_funcs["luck"](),
        }

        # Derived stats
        power = self.attributes["Power"]
        self.attributes["Sanity"] = power
        self.attributes["Magic"] = int(power / 5)

        # Apply age-based changes
        self.apply_age_modifiers()

        #Calculate damage bonus and build
        self.calculate_damage_bonus_and_build()

        #Calculate HP
        self.attributes["HP"] = int((self.attributes["Constitution"] + self.attributes["Size"]) / 10)

        #Calculate Movement
        self.calculate_mov()

    def apply_age_modifiers(self):
        mods = rules.get_age_modifiers(self.age)

        if mods.get("teen_mods"):
            rules.apply_teen_modifiers(self.attributes)
        else:
            rules.apply_edu_improvement(self.attributes, mods["edu_checks"])
            self.attributes["Appearance"] -= mods["app_loss"]

            if mods["phys_loss"] > 0:
                self.allocate_physical_losses(mods["phys_loss"])

    def allocate_physical_losses(self, points_to_deduct):
        """
        Prompts the player to divide physical loss points across STR, CON, DEX.
        """
        print(f"\nDue to your age, you must deduct a total of {points_to_deduct} points.")
        print("Distribute them across Strength, Constitution, and Dexterity.\n")

        stats = ["Strength", "Constitution", "Dexterity"]
        deductions = {}
        remaining = points_to_deduct

        for stat in stats:
            while True:
                try:
                    prompt = f"Points remaining: {remaining} — How many points to deduct from {stat}? "
                    amount = int(input(prompt))

                    if amount < 0:
                        print("You cannot deduct a negative number.")
                    elif amount > remaining:
                        print(f"You only have {remaining} points left to allocate.")
                    else:
                        deductions[stat] = amount
                        remaining -= amount
                        break
                except ValueError:
                    print("Please enter a valid number.")

        # If any points remain unallocated, assign them to Strength by default
        if remaining > 0:
            print(f"\nYou have {remaining} unallocated point(s). Applying the rest to Strength by default.")
            deductions["Strength"] += remaining

        # Apply deductions
        for stat, amount in deductions.items():
            self.attributes[stat] -= amount


    def calculate_damage_bonus_and_build(self):
        """
        Determines the character's damage bonus and build from STR + SIZ.
        """
        total = self.attributes["Strength"] + self.attributes["Size"]

        if total <= 64:
            self.attributes["Damage Bonus"] = "–2"
            self.attributes["Build"] = -2
        elif total <= 84:
            self.attributes["Damage Bonus"] = "–1"
            self.attributes["Build"] = -1
        elif total <= 124:
            self.attributes["Damage Bonus"] = "None"
            self.attributes["Build"] = 0
        elif total <= 164:
            self.attributes["Damage Bonus"] = "+1D4"
            self.attributes["Build"] = 1
        elif total <= 204:
            self.attributes["Damage Bonus"] = "+1D6"
            self.attributes["Build"] = 2
        elif total <= 284:
            self.attributes["Damage Bonus"] = "+2D6"
            self.attributes["Build"] = 3
        elif total <= 364:
            self.attributes["Damage Bonus"] = "+3D6"
            self.attributes["Build"] = 4
        elif total <= 444:
            self.attributes["Damage Bonus"] = "+4D6"
            self.attributes["Build"] = 5
        elif total <= 524:
            self.attributes["Damage Bonus"] = "+5D6"
            self.attributes["Build"] = 6
        else:
            bonus_d6 = 5 + ((total - 524 + 79) // 80)
            build = 6 + ((total - 524 + 79) // 80)
            self.attributes["Damage Bonus"] = f"+{bonus_d6}D6"
            self.attributes["Build"] = build

    def calculate_mov(self):

        if self.attributes["Dexterity"] < self.attributes["Size"] and self.attributes["Strength"] < self.attributes["Size"]:
            self.attributes["Movement"] = 7
        elif self.attributes["Dexterity"] >= self.attributes["Size"] or self.attributes["Strength"] >= self.attributes["Size"]:
            self.attributes["Movement"] = 8
        elif self.attributes["Dexterity"] > self.attributes["Size"] and self.attributes["Strength"] > self.attributes["Size"]:
            self.attributes["Movement"] = 9
        
        if self.age >= 40 and self.age <= 49:
            self.attributes["Movement"] -= 1
        elif self.age >= 50 and self.age <= 59:
            self.attributes["Movement"] -= 2
        elif self.age >= 60 and self.age <= 69:
            self.attributes["Movement"] -= 3
        elif self.age >= 70 and self.age <= 79:
            self.attributes["Movement"] -= 4
        elif self.age >= 80:
            self.attributes["Movement"] -= 5
            

    def __str__(self):
        lines = [f"Name: {self.name}", f"Age: {self.age}"]
        lines.extend(f"{key}: {value}" for key, value in self.attributes.items())
        return "\n".join(lines)
