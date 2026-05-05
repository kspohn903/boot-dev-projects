class Hero:
    def __init__(self, name, health):
        self.__name = name
        self.__health = health

    def get_name(self):
        return self.__name

    def get_health(self):
        return self.__health

    def take_damage(self, damage):
        if(self.get_health() - damage < 0):
          raise ValueError(f"{self.__name} died")
        self.__health -= damage

class Archer(Hero):
    def __init__(self, name, health, num_arrows):
        super().__init__(name, health)
        self.__num_arrows = num_arrows

    def shoot(self, target, n=1, dmg_per_arrow=10):
        if self.__num_arrows <= 0:
           raise Exception("not enough arrows")
        self.__num_arrows -= n
        target.take_damage(n * dmg_per_arrow)

# don't touch above this line

class Wizard(Hero):
    def __init__(self, name, health, mana):
        super().__init__(name, health)
        self.__mana = mana

    def cast(self, target, mp_consumed=25):
        if(self.__mana < mp_consumed):
           raise ValueError("not enough mana")
        self.__mana -= mp_consumed
        target.take_damage(mp_consumed)
            
