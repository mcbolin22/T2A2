# Encapsulation
class Car:
    # Constructor
    def __init__(self, color, make):
        self._color = color
        self.make = make
        print("Hello")
        print(self)

    def get_color(self):
        # conditions fulfilled
        return self._color
    
    def set_color(self, color):
        # conditions fulfilled
        self._color = color

    def run(self):
        print(f"{self.make} is running! Vroom Vrooom!!!")
        

# Object of class
my_car = Car("black", "honda")

print(my_car.get_color())

my_car.set_color("red")

print(my_car.get_color())

# print(my_car.color)
# my_car.color = "red"
# print(my_car.color)
# print(my_car.make)

# my_car.run()

# your_car = Car("white", "Toyota")
# print(your_car.make)

# your_car.run()

# Inheritance
class PetrolCar(Car):
    def __init__(self, color, make, tank_capacity):
        super().__init__(color, make)
        self.tank_capacity = tank_capacity

    def make_turn(self):
        print("I am making a turn")

my_petrol_car = PetrolCar("silver", "BMW", 40)

print(my_petrol_car.make)

print(my_petrol_car.tank_capacity)

my_petrol_car.run()
my_petrol_car.make_turn()

# Polymorphism - Function Overloading and Function Overriding
class ElectricCar(Car):
    # Overriding
    def run(self):
        print("I run silently. No Vroom!")

    # def run(self, distance):
        #print(f"I ran for {distance} km")

my_electric_car = ElectricCar("yellow", "Tesla")

my_electric_car.run()
# my_electric_car.run(10)

# Abstraction
class 