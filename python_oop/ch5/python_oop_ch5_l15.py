class Siege:
    def __init__(self, max_speed, efficiency):
        # Initialize public instance variables
        self.max_speed = max_speed
        self.efficiency = efficiency

    def get_trip_cost(self, distance, food_price):
        # Formula: (distance / efficiency) * food_price
        return (distance / self.efficiency) * food_price

    def get_cargo_volume(self):
        # Child classes will override this
        pass


class BatteringRam(Siege):
    def __init__(
        self,
        max_speed,
        efficiency,
        load_weight,
        bed_area,
    ):
        # Call the parent constructor
        super().__init__(max_speed, efficiency)
        # Set battering-ram-only instance variables
        self.load_weight = load_weight
        self.bed_area = bed_area

    def get_trip_cost(self, distance, food_price):
        # Formula: parent cost + (load_weight * 0.01)
        base_cost = super().get_trip_cost(distance, food_price)
        return base_cost + (self.load_weight * 0.01)

    def get_cargo_volume(self):
        # Formula: bed_area * depth (which is always 2)
        return self.bed_area * 2


class Catapult(Siege):
    def __init__(self, max_speed, efficiency, cargo_volume):
        # Call the parent constructor
        super().__init__(max_speed, efficiency)
        # Set catapult-only instance variable
        self.cargo_volume = cargo_volume

    def get_cargo_volume(self):
        # Returns the cargo capacity set in the constructor
        return self.cargo_volume
