class Hero():
    def __init__(self, name, health):
        self.__name = name
        self.__health = health

    def set_name(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    def set_health(self, health):
        self.__health = health

    def get_health(self):
        return self.__health

    def take_damage(self, damage):
        if(self.__health - damage <= 0):
          raise ValueError(f"{self.get_name()} died")
        self.__health -= damage

# don't touch above this line

class Archer(Hero):
    def __init__(self, name, health, num_arrows):
        super().__init__(name, health)
        self.__num_arrows = num_arrows

    def get_num_arrows(self):
        return self.__num_arrows
    
    def shoot(self, target, n=1, dmg_per_arrow=10):
        # Check if enough arrows are available
        if self.get_num_arrows() - n < 0:
          raise ValueError("not enough arrows")
        
        # Deduct arrows
        self.__num_arrows -= n
        
        # Calculate total damage
        total_damage = n * dmg_per_arrow
        
        # Use the hero's method to apply damage[cite: 4]
        target.take_damage(total_damage)
