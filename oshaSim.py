import math
import csv
from matplotlib import pyplot as plt 
#Change values if needed

class oshaSim:
    def __init__(self):
        # Constants
        self.gravity = 9.81  # m/s^2, gravitational acceleration
        self.air_density = 1.225  # kg/m^3, at sea level
        self.burn_time = 5.685  # s
        self.avg_thrust = 613  # N
        self.max_thrust = 953.2100  # N
        self.mass_wet = 8.602  # kg
        self.mass_dry = 6.000  # kg
        self.Cd = 0.450  # Drag coefficient
        self.cs_area = 0.0062  # m^2, cross-sectional area
        self.sound_speed = 343  # m/s, speed of sound at sea level
        
        # State variables
        self.time_step = 0.1  # s
        self.time = 0  # s
        self.altitude = 445.9224  # m, initial altitude
        self.velocity = 0  # m/s
        self.acceleration = 0  # m/s^2
        self.mass = self.mass_wet  # initial mass
        self.max_altitude = 0
        self.max_speed = 0
        self.max_acceleration = 0
        self.time_at_apogee = None
        self.mach_number = 0
        self.time_at_mach_08 = None

        # Data storage for CSV
        self.simulation_data = []

    def calculate_drag(self):
        return 0.5 * self.Cd * self.cs_area * self.air_density * (self.velocity ** 2)

    def update_physics(self):
        thrust = self.avg_thrust if self.time <= self.burn_time else 0
        drag = self.calculate_drag()
        gravity_force = self.mass * self.gravity
        net_force = thrust - gravity_force - drag
        self.acceleration = net_force / self.mass

        self.velocity += self.acceleration * self.time_step
        self.altitude += self.velocity * self.time_step

        # Track the maximums and significant events
        if self.altitude > self.max_altitude:
            self.max_altitude = self.altitude

        current_speed = abs(self.velocity)
        if current_speed > self.max_speed:
            self.max_speed = current_speed

        if abs(self.acceleration) > self.max_acceleration:
            self.max_acceleration = abs(self.acceleration)

        if self.velocity < 0 and self.time_at_apogee is None:
            self.time_at_apogee = self.time

        self.mach_number = current_speed / self.sound_speed
        if self.mach_number >= 0.8 and self.time_at_mach_08 is None:
            self.time_at_mach_08 = self.time

        self.time += self.time_step

        # Collect data for each step
        self.simulation_data.append([self.time, self.altitude, self.velocity, self.acceleration, self.mach_number])

    def simulate(self):
        print("Starting simulation...")
        while self.altitude > 0:
            self.update_physics()
        print("Simulation ended.")
        self.write_to_csv()

    def display_results(self):
        # Print results
        print(f"Max Altitude: {self.max_altitude:.2f} m ({self.max_altitude * 3.28084:.2f} ft)")
        print(f"Max Speed: {self.max_speed:.2f} m/s ({self.max_speed * 3.28084:.2f} ft/s)")
        print(f"Max Acceleration: {self.max_acceleration:.2f} m/s^2 ({self.max_acceleration * 3.28084:.2f} ft/s^2)")
        print(f"Max Thrust: {self.max_thrust:.2f} N")
        if self.time_at_apogee is not None:
            print(f"Time at Apogee: {self.time_at_apogee:.2f} s")
        if self.time_at_mach_08 is not None:
            print(f"Time at Mach 0.8: {self.time_at_mach_08:.2f} s")
        print(f"Max Mach Number: {self.mach_number:.2f}")

    def write_to_csv(self):
        # Write simulation data to CSV
        with open('rocket_simulation_data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Time (s)', 'Altitude (m)', 'Velocity (m/s)', 'Acceleration (m/s^2)', 'Mach Number'])
            writer.writerows(self.simulation_data)
        print("Data written to rocket_simulation_data.csv")
    
    # def display_thrust(self):
    #     thrust_data = []
    #     for data in self.simulation_data:
    #         time = data[0]
    #         thrust = self.avg_thrust if time <= self.burn_time else 0
    #         thrust_data.append([time, thrust])
    #     print("Thrust over time:")
    #     for data in thrust_data:
    #         print(f"Time: {data[0]:.2f} s, Thrust: {data[1]:.2f} N")


#PLOT DATA FUNCTION CHANGE IF NEEDED# 
    def plot_data(self):
            print("Available plots:")
            print("1. Altitude vs Time")
            print("2. Velocity vs Time")
            print("3. Acceleration vs Time")
            print("4. Mach Number vs Time")
            
            choice = input("Enter the number of the plot you want to see: ")
            
            plt.figure(figsize=(10, 6))
            if choice == '1':
                x = [data[0] for data in self.simulation_data]
                y = [data[1] for data in self.simulation_data]
                plt.plot(x, y)
                plt.title("Altitude vs Time")
                plt.xlabel("Time (s)")
                plt.ylabel("Altitude (m)")
            elif choice == '2':
                x = [data[0] for data in self.simulation_data]
                y = [data[2] for data in self.simulation_data]
                plt.plot(x, y)
                plt.title("Velocity vs Time")
                plt.xlabel("Time (s)")
                plt.ylabel("Velocity (m/s)")
            elif choice == '3':
                x = [data[0] for data in self.simulation_data]
                y = [data[3] for data in self.simulation_data]
                plt.plot(x, y)
                plt.title("Acceleration vs Time")
                plt.xlabel("Time (s)")
                plt.ylabel("Acceleration (m/s^2)")
            elif choice == '4':
                x = [data[0] for data in self.simulation_data]
                y = [data[4] for data in self.simulation_data]
                plt.plot(x, y)
                plt.title("Mach Number vs Time")
                plt.xlabel("Time (s)")
                plt.ylabel("Mach Number")
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
                return
            
            plt.grid(True)
            plt.show()

    def simulate(self):
        print("Starting simulation...")
        while self.altitude > 0:
            self.update_physics()
        print("Simulation ended.")
        self.write_to_csv()
        self.display_results()
        self.plot_data()
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


# Usage
simulator = oshaSim()
simulator.simulate()
