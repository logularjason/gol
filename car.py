class Car:
    def __init__(self, model, tankCapacity):
        self.model = model 
        self.tankCapacity = tankCapacity
        self.fuelLevel = 0

    def print(self):
        print(self.model, self.tankCapacity, self.fuelLevel, sep="---")


    def fill(self, amount):
        self.fuelLevel += amount


dadsCar = Car("toyota", 72)
laurasCar = Car("porsche", 50)


dadsCar.print()
laurasCar.print()


dadsCar.fill(30)
laurasCar.fill(50)
laurasCar.fill(10)

dadsCar.print()
laurasCar.print()