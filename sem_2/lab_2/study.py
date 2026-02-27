class Hero:
    def __init__(self, name: str) -> None:
        self.name = name
        self.damage = 5
        self._health = 100
        self.level = 1

    def __str__(self):
        return f"Class:{self.__class__.__name__} | Name: {self.name} | HP: {self.health}"

    @property
    def health(self) -> int:
        return self._health
    
    @health.setter
    def health(self, new_value:int) -> int:
        if new_value < 0:
            self._health = 0
            print(f"{self.name} death!")
        elif new_value > 100:
            self._health = 100
        else:
            self._health = new_value
    
    def attack(self, enemy: 'Hero') -> None:
        print(f"{self.name} attacks {enemy.name} and deals {self.damage} damage.")
        enemy.health -= self.damage

class Warrior(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 15

    def shout(self):
        print(f"{self.name}: for the horde!!!")

class Mage(Hero):
    def __init__(self, name):
        super().__init__(name)
        self.damage = 3
        self._mana = 100

    def __str__(self):
        return f"Class:{self.__class__.__name__} | Name: {self.name} | HP: {self.health} | Mana: {self.mana}"

    @property
    def mana(self):
        return self._mana
    
    @mana.setter
    def mana(self, new_value):
        if new_value < 0:
            self._mana = 0
            print("Death!")
        elif new_value > 100:
            self._mana = 100
        else:
            self._mana = new_value

    def cast_spell(self, enemy):
        if self.mana >= 20:
            print(f"{self.name} cast 'The thunderbolt' for 30 damage.")
            enemy.health -= 30
            self.mana -= 20
        else:
            print(f"Don't have enoughtf mana.")

def main():
    conan = Warrior("Conan")
    gendalf = Mage("Gendalf")
    conan.attack(gendalf)
    gendalf.cast_spell(conan)
    conan.shout()
    print(f"Gendalf: {gendalf.health}")
    print(f"Conan: {conan.health}")  
    print(gendalf.mana)

if __name__ == "__main__":
    main()