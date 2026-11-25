
class BaseWarrior():

    personnage_count: int = 0
    max_ki: int = 10000

    def __init__(self, name: str, hp: int, ki: int=50, attack_power: int=50) -> None:
        self.name: str = name
        if(hp<=0):
            raise ValueError("Points de vie négatifs ")
        else:
            self.max_hp: int = hp
            self.hp: int = hp
        
        self.ki: int = ki
        self.attack_power: int = attack_power

        BaseWarrior.personnage_count+=1

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp=max(0,min(value,self.max_hp))

    def attaquer(self, defenseur):
        defenseur.hp-=self.attack_power/2
        self.ki-=10

class Saiyan(BaseWarrior):

    def __init__(self, name: str, hp: int, ki: int=50, attack_power: int=100, rage: int=2):
        super().__init__(name, hp, ki, attack_power)
        if rage<=0:
            raise InvalidStatError("la rage doit être >0")

    def attaquer(self, defenseur):
        defenseur.hp-=self.attack_power*self.rage
        self.ki-=30

class WarriorError(Exception):
    pass

class InvalidStatError(WarriorError):
    pass

    

Humain=BaseWarrior("humain", 100, 1000, 500)
Goku=Saiyan("Goku", 1000, 1000, 1000, 3)

Humain.attaquer(Goku)
Goku.attaquer(Humain)
print(Goku.ki)
print(Goku.hp)
print(Humain.hp)

try:
    Vegeta=Saiyan("vegeta", -1000, 1000, 900,4)
except InvalidStatError:
    print("gestion de l'erreur invalidstaterror")
except WarriorError:
    print("")
else:
    print("le code est executé sans erreur")
finally:
    print("execute dans tous les cas")




