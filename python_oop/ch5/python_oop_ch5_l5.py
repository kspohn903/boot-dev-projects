class Human():
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


## don't touch above this line


class Archer(Human):
    def __init__(self, name, num_arrows):
        super().__init__(name)
        self.__num_arrows = num_arrows

    def get_num_arrows(self):
        return self.__num_arrows

    def use_arrows(self, n_arrows):
        if(self.get_num_arrows() - n_arrows < 0):
           raise ValueError("not enough arrows")
        
        self.__num_arrows -= n_arrows


class Crossbowman(Archer):
    def __init__(self, name, num_arrows):
        super().__init__(name, num_arrows)

    def triple_shot(self, target, n=3):
        self.use_arrows(n)
        return f"{target.get_name()} was shot by {n} crossbow bolts"

