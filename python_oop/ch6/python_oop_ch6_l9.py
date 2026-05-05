class Sword:
    def __init__(self, sword_type):
        self.sword_type = sword_type

    def __add__(self, other):
        # Check if both are bronze to craft iron
        if self.sword_type == "bronze" and other.sword_type == "bronze":
            return Sword("iron")
        
        # Check if both are iron to craft steel
        if self.sword_type == "iron" and other.sword_type == "iron":
            return Sword("steel")
        
        # If the combination doesn't match the recipes, raise an exception
        raise Exception("cannot craft")
