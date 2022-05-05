from FlightRadar24.flight import Flight
import time

from geo_math import extrapolate_velocity, eyeball_calculation, azimuth, angle_to_compass, feet_to_miles, kts_to_mph


def angle_with_compass(angle):
    return f'{angle:.2f}º ({angle_to_compass(angle)})'


class PlaneSpot:
    def __init__(self, home, flight: Flight):
        self.flight = flight
        self.time_diff = time.time() - flight.time

        # Use ground speed to approximate current position
        self.estimated_position = extrapolate_velocity((flight.latitude, flight.longitude), flight.ground_speed,
                                                       flight.heading, self.time_diff)

        # Compute azimuth and angle above horizon
        self.azimuth_angle = azimuth(home, self.estimated_position)
        self.horizon_angle, self.eyeball_distance = eyeball_calculation(home, self.estimated_position, flight.altitude)

        if self.azimuth_angle < 0:
            self.azimuth_angle += 360

    def location_str(self):
        return f'{self.estimated_position[0]:.4f}º, {self.estimated_position[1]:.4f}º, {self.flight.altitude} ft'

    def speed_str(self):
        return f'{kts_to_mph(self.flight.ground_speed):.0f} mph'

    def print(self):
        print(f'Flight {self.flight.callsign} {self.flight.aircraft_code} @ ({self.location_str()})')
        print(f'\tTraveling at {self.speed_str()}, {angle_with_compass(self.flight.heading)}')
        print(f'\tAzimuth angle: {angle_with_compass(self.azimuth_angle)}')
        print(f'\tHorizon angle: {self.horizon_angle:.2f}º')
        print(f'\tEyeball distance: {feet_to_miles(self.eyeball_distance):.2f} mi')
