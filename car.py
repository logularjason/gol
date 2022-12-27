class Battery:
    def __init__(self):
        self.charge = 12

    def drive(self, km):
        self.charge += km * 0.02
        if self.charge > 13.8:
            self.charge = 13.8

    def park(self, months):
        self.charge -= months * 0.05
        if self.charge < 0:
            self.charge = 0

class FuelSystem:
    def __init__(self, tankCapacity):
        self.tankCapacity = tankCapacity
        self.fuelLevel = 0

    def fill(self, amount):
        self.fuelLevel += amount

    def drive(self, km, litersPerKm):
        self.fuelLevel -= km * litersPerKm

class Car:
    def __init__(self, model, tankCapacity, litresPerKm):
        self.model = model 
        self.litresPerKm = litresPerKm
        self.battery = Battery()
        self.fuelSystem = FuelSystem(tankCapacity)

    def print(self, message):
        print(message, " model=", self.model, ", tankCapacity=", self.fuelSystem.tankCapacity, ", batteryCharge=", self.battery.charge, ", fuelLevel=", self.fuelSystem.fuelLevel, sep="")

    def fill(self, amount):
        self.fuelSystem.fill(amount)

    def park(self, months):
        self.battery.park(months)

    def drive(self, km):
        self.battery.drive(km)
        self.fuelSystem.drive(km, self.litresPerKm)
  

dadsCar = Car("toyota", 72, 0.1)
laurasCar = Car("porsche", 50, 0.05)

dadsCar.print("Begin     ")
laurasCar.print("Begin     ")

dadsCar.fill(30)
laurasCar.fill(50)
laurasCar.fill(10)

dadsCar.print("After fill")
laurasCar.print("After fill")

dadsCar.park(4)
laurasCar.park(3)

dadsCar.print("After park")
laurasCar.print("After park")

dadsCar.drive(200)
laurasCar.drive(1)

dadsCar.print("After driv")
laurasCar.print("After driv")