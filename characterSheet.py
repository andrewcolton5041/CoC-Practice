from cocCharStatGen import chargen_str, chargen_con, chargen_siz, chargen_dex, chargen_app, chargen_int, chargen_pow, chargen_edu, chargen_luck

class Character:
  def __init__(self, name, age):
    self.name = name
    self.age = age
    self.strength = chargen_str()
    self.constitution = chargen_con()
    self.size = chargen_siz()
    self.dexterity = chargen_dex()
    self.appearance = chargen_app()
    self.intelligence = chargen_int()
    self.power = chargen_pow()
    self.education = chargen_edu()
    self.luck = chargen_luck()

  def print(self):
    print(f"Name: {self.name}")
    print(f"Age: {self.age}")
    print(f"Strength: {self.strength}")
    print(f"Constitution: {self.constitution}")
    print(f"Size: {self.size}")
    print(f"Dexterity: {self.dexterity}")
    print(f"Appearance: {self.appearance}")
    print(f"Intelligence: {self.intelligence}")
    print(f"Power: {self.power}")
    print(f"Education: {self.education}")
    print(f"Luck: {self.luck}")
    