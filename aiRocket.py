import math
import numpy as np
from sklearn.linear_model import LinearRegression

class RocketSimulator:
    def __init__(self):
        self.gravity = 9.81  # m/s^2
        self.cs_area = 0.0366  # m^2
        self.mass_dry = 70  # kg
        self.time_step = 0.01  # s
        self.initial_altitude = 1219.2  # m
        self.altitude = 0
        self.velocity = 0
        self.acceleration = 0
        self.model = LinearRegression()
        self.air_temp = 15  #sea level in Celsius

    def calculate_air_density(self, altitude):
        if altitude < 11000:
            self.air_temp = -0.0092485 * altitude + (33.95 + 11.2734)
            air_pres = 101.29 * (((self.air_temp + 273.15) / 288.08) ** 5.256)
        else:
            self.air_temp = -56.46
            air_pres = 22.65 * math.exp(1.73 - (0.000157 * altitude))
        return air_pres / (0.2869 * (self.air_temp + 273.1))

    def calculate_drag(self, Cd, velocity, air_density):
        return 0.5 * Cd * self.cs_area * air_density * velocity ** 2

    def update_physics(self, thrust):
        self.altitude += self.velocity * self.time_step
        air_density = self.calculate_air_density(self.initial_altitude + self.altitude)
        speed_of_sound = math.sqrt(1.4 * 8.3145 * (self.air_temp + 273.15) / 0.028964)
        mach_number = abs(self.velocity / speed_of_sound)
        Cd = self.calculate_coefficient_of_drag(mach_number)
        drag_force = self.calculate_drag(Cd, self.velocity, air_density)
        mass_cur = self.mass_dry  # Add propellant mass here if variable
        weight = mass_cur * self.gravity
        total_force = thrust - weight - drag_force
        self.acceleration = total_force / mass_cur
        self.velocity += self.acceleration * self.time_step

def calculate_coefficient_of_drag(self, mach_number):
    if mach_number < 0.8:
        # polynomial fit for subsonic regime
        return 0.6 - 0.1 * mach_number
    elif 0.8 <= mach_number <= 1.2:
        # Higher drag around transonic speed
        return 0.8 + 0.4 * (mach_number - 0.8)
    elif 1.2 < mach_number < 5:
        # Decrease as speed increases in supersonic regime
        return 1.2 - 0.08 * (mach_number - 1.2)
    else:
        # approximate hypersonic regime, simplified
        return 0.6 + 0.1 * (mach_number - 5)


def simulate(self):
    while self.velocity >= 0:
        thrust = 1000  # Placeholder for thrust force change if you'd like
        self.update_physics(thrust)
        print(f"Altitude: {self.altitude:.2f} m, Velocity: {self.velocity:.2f} m/s, Acceleration: {self.acceleration:.2f} m/s²")
        if self.altitude < 0:
            break

# Usage
simulator = RocketSimulator()
simulator.simulate()
