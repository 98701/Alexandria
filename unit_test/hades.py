zag = {"life": 100, "attack": 50}

class Boon:

    def __init__(self, god, rarity):
        self.god = god
        self.rarity = rarity

    def use(self):
        if self.god == "Chaos":
            zag["life"] -= 21

        if self.rarity == "rare":
            zag["attack"] += 50
        else: 
            zag["attack"] += 20


divine_flourish = Boon("Athena", "rare")
cursed_slash = Boon("Chaos", "common")



divine_flourish.use()
cursed_slash.use()
print(zag)



