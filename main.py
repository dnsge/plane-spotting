#!/usr/bin/env python3
import sys

from FlightRadar24.api import FlightRadar24API

from plane_spotting import PlaneSpot


def create_zone(origin, deg_range):
    return {
        'tl_x': origin[1] - deg_range,
        'tl_y': origin[0] + deg_range,
        'br_x': origin[1] + deg_range,
        'br_y': origin[0] - deg_range
    }


def in_flight_filter(spot: PlaneSpot):
    return spot.flight.altitude > 100 and spot.flight.ground_speed > 50


def spot_horizon_angle(spot: PlaneSpot):
    return spot.horizon_angle


def run(origin_location, deg_range):
    origin_zone = create_zone(origin_location, deg_range)
    fr_api = FlightRadar24API()
    bounds = fr_api.get_bounds(origin_zone)

    while True:
        flights = fr_api.get_flights(bounds=bounds)
        spotted = list(filter(in_flight_filter, map(lambda f: PlaneSpot(origin_location, f), flights)))
        spotted = sorted(spotted, key=spot_horizon_angle, reverse=True)

        print(f'Spotted {len(spotted)} nearby flights')
        for spot in spotted:
            spot.print()

        try:
            input('\n[ENTER] to refresh ')
        except (KeyboardInterrupt, EOFError):
            return


def main():
    args = sys.argv
    if len(args) not in (3, 4):
        print(f'Usage: {args[0]} [lat] [lon] <deg_range=0.2>')
        sys.exit(1)

    lat = float(args[1].strip(',°'))
    lon = float(args[2].strip(',°'))
    deg_range = 0.2
    if len(args) == 4:
        deg_range = float(args[3])

    run((lat, lon), deg_range)


if __name__ == '__main__':
    main()
