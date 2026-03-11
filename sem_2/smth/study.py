from typing import Optional

class Hero:
    def __init__(self, name: str) -> None:
        self.name = name
        self._health = 100
        self.weapon: Optional['Weapon'] = None

    def __str__(self):
        return f"Class: {self.__class__.__name__} | Name: {self.name} | HP: {self.health}"

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
    
    #def equip_weapon(self, weapon: 'Weapon'):

    def attack(self, enemy: 'Hero') -> None:
        print(f"{self.name} attacks {enemy.name} and deals {self.damage} damage.")
        enemy.health -= self.damage

class Weapon:
    def __init__(self, damage: int, name: str)->None:
        self.name = name
        self.damage = damage

    def __str__(self)->str:
        return f"{self.name} have {self.damage} DMG."

    def get_damage(self)->int:
        return self.damage

class Sword(Weapon):
    def __init__(self)->None:
        super().__init__(45)

class Warrior(Hero):
    def __init__(self, name: str)->None:
        super().__init__(name)
        self.weapon = None

    def take_weapon(self, weapon_object: 'Weapon')->None:
        self.weapon = weapon_object

    def attack(self, enemy: 'Hero')->None:
        if self.weapon is None:
            damage = 1
            print(f"{self.name} punches {enemy.name} for {damage} damage.")
        else:
            damage = self.weapon.get_damage()
            print(f"{self.name} attacks with weapon for {damage} damage.")
        
        enemy.health -= damage

    def shout(self)->None:
        print(f"{self.name}: for the horde!!!")


class Mage(Hero):
    def __init__(self, name: str)->None:
        super().__init__(name)
        self.damage = 3
        self._mana = 100

    def __str__(self):
        return f"Class: {self.__class__.__name__} | Name: {self.name} | HP: {self.health} | Mana: {self.mana}"

    @property
    def mana(self)->int:
        return self._mana
    
    @mana.setter
    def mana(self, new_value:int)->int:
        if new_value < 0:
            self._mana = 0
            print("Death!")
        elif new_value > 100:
            self._mana = 100
        else:
            self._mana = new_value

    def cast_spell(self, enemy: 'Hero')->None:
        if self.mana >= 20:
            print(f"{self.name} cast 'The thunderbolt' for 30 damage.")
            enemy.health -= 30
            self.mana -= 20
        else:
            print(f"Don't have enoughtf mana.")

def main():
    conan = Warrior("Conan")
    gendalf = Mage("Gendalf")
    sword = Sword()
    conan.take_weapon(sword)
    print("---Before fight---")
    print(conan)
    print(gendalf)
    print("---Fight---")
    conan.attack(gendalf)
    gendalf.cast_spell(conan)
    conan.shout()
    print("---After fight---")
    print(conan)
    print(gendalf)
    
if __name__ == "__main__":
    main()