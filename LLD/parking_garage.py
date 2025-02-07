from datetime import datetime, timedelta

class ParkingGarage:
    def __init__(self, standard_spots, ev_spots, motorcycle_spots):
        self.available_spots = {
            'standard': list(range(1, standard_spots + 1)),
            'ev': list(range(1, ev_spots + 1)),
            'motorcycle': list(range(1, motorcycle_spots + 1))
        }
        
        self.total_spots = {
            'standard': standard_spots,
            'ev': ev_spots,
            'motorcycle': motorcycle_spots
        }
        
        self.tickets = {}  # Will store {spot_id: {'entry_time': time, 'vehicle_type': type}}
        self.hourly_rate = 3
        self.lost_ticket_fee = 20
        self.overnight_fee = 30
        self.grace_period = timedelta(minutes=10)
    
    def assign_spot(self, vehicle_type):
        if not self.available_spots[vehicle_type]:
            return "No spots available for this vehicle type."
        
        spot_id = self.available_spots[vehicle_type].pop(0)
        self.tickets[spot_id] = {
            'entry_time': datetime.now(),
            'vehicle_type': vehicle_type  # Store the vehicle type with the ticket
        }
        return spot_id
    
    def exit_garage(self, spot_id, vehicle_type, lost_ticket=False, overnight=False):
        if lost_ticket:
            fee = self.lost_ticket_fee
        elif spot_id not in self.tickets:
            return "Invalid ticket."
        else:
            entry_time = self.tickets[spot_id]['entry_time']
            parked_duration = datetime.now() - entry_time
            if parked_duration <= self.grace_period:
                fee = 0
            else:
                parked_hours = parked_duration.seconds // 3600 + 1
                fee = parked_hours * self.hourly_rate
                if overnight:
                    fee = self.overnight_fee
        if spot_id in self.tickets:
            # Get the vehicle type from the ticket before removing it
            # vehicle_type = self.tickets[spot_id]['vehicle_type']
            # Remove the ticket
            self.tickets.pop(spot_id)
            # Return the spot to the correct vehicle type's available spots
            self.available_spots[vehicle_type].insert(0, spot_id)
            self.available_spots[vehicle_type].sort()  # Keep spots in numerical order
        
        return fee
    
    def check_availability(self):
        return {key: len(self.available_spots[key]) for key in self.available_spots}
    
    def display_occupancy(self):
        available_spots = sum(len(spots) for spots in self.available_spots.values())
        total_spots = sum(self.total_spots.values())
        occupied_spots = total_spots - available_spots
        return f"Occupied spots: {occupied_spots}, Available spots: {available_spots}"

class Vehicle:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type
        self.parking_spot = None
        self.entry_time = None
    
    def enter_garage(self, garage):
        spot_id = garage.assign_spot(self.vehicle_type)
        if isinstance(spot_id, int):
            self.parking_spot = spot_id
            self.entry_time = datetime.now()
            return f"Vehicle parked at spot {spot_id}"
        return spot_id
    
    def exit_garage(self, garage, lost_ticket=False, overnight=False):
        if self.parking_spot is None:
            return "Vehicle is not parked."
        fee = garage.exit_garage(self.parking_spot, self.vehicle_type, lost_ticket, overnight)
        self.parking_spot = None
        self.entry_time = None
        return f"Total fee: ${fee}"
    


# Initialize the parking garage with 10 standard, 2 EV, and 1 motorcycle spots
garage = ParkingGarage(10, 2, 1)

# Create vehicle instances
vehicle1 = Vehicle('standard')
vehicle2 = Vehicle('standard')
vehicle3 = Vehicle('motorcycle')

# Vehicles enter the garage
print(vehicle1.enter_garage(garage))
print(vehicle2.enter_garage(garage))
print(vehicle3.enter_garage(garage))

vehicle4 = Vehicle('standard')

print(vehicle1.exit_garage(garage))
print(vehicle4.enter_garage(garage))


# Check availability
print("Availability:", garage.check_availability())

# Display real-time occupancy
print("Occupancy:", garage.display_occupancy())