import math

from haversine import haversine, Unit
from haversine.haversine import get_avg_earth_radius

EARTH_RADIUS = get_avg_earth_radius(Unit.FEET)


def coord_to_rads(coord):
    return math.radians(coord[0]), math.radians(coord[1])


def kts_to_fps(kts):
    return kts * 1.68781


def kts_to_mph(kts):
    return kts * 1.15078


def feet_to_miles(feet):
    return feet / 5280.0


def extrapolate_velocity(pos, speed, heading, delta_t):
    # Courtesy of https://stackoverflow.com/q/4909380
    rad_heading = math.radians(heading)
    dx = math.sin(rad_heading) * delta_t * kts_to_fps(speed)
    dy = math.cos(rad_heading) * delta_t * kts_to_fps(speed)

    lat = pos[0] + math.degrees(dy / EARTH_RADIUS)
    lon = pos[1] + math.degrees(dx / EARTH_RADIUS / math.sin(math.radians(pos[0])))
    return lat, lon


def azimuth(start, end):
    s_lat, s_lon = coord_to_rads(start)
    e_lat, e_lon = coord_to_rads(end)
    del_lon = e_lon - s_lon

    theta = math.atan2(
        math.sin(del_lon) * math.cos(e_lat),
        (math.cos(s_lat) * math.sin(e_lat)) - (math.sin(s_lat) * math.cos(e_lat) * math.cos(del_lon))
    )

    return math.degrees(theta)


def law_of_cosines(origin_side, target_side, angle):
    csq = origin_side * origin_side + target_side * target_side - (2 * origin_side * target_side * math.cos(angle))
    return math.sqrt(csq)


def law_of_sines(ref_side, ref_angle, target_side):
    return math.asin((target_side / ref_side) * math.sin(ref_angle))


def eyeball_calculation(origin, target, altitude):
    target_core_distance = EARTH_RADIUS + altitude
    origin_core_distance = EARTH_RADIUS
    arc_distance = haversine(origin, target, unit=Unit.FEET)
    arc_angle = arc_distance / EARTH_RADIUS

    dist_to_target = law_of_cosines(origin_core_distance, target_core_distance, arc_angle)
    origin_side_angle = law_of_sines(dist_to_target, arc_angle, target_core_distance)

    if origin_side_angle < math.pi / 2:
        origin_side_angle = math.pi - origin_side_angle

    horizon_angle = abs(origin_side_angle - math.pi / 2)

    return math.degrees(horizon_angle), dist_to_target


def angle_to_compass(angle):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    if angle < 0:
        angle += 360

    return directions[round(angle / 45)]
