import characterSheet as cs

name = input("What is your characters name?  ")
age = int(input("What is your characters age?  "))

c = cs.Character(name, age)

print(c)