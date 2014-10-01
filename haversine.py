#!/usr/bin/env python

# Adapted from code by Wayne Dyck

import math

km = 6371.009
mi = 3958.761
nm = 3440.07

seattle = [47.621800, -122.350326]
olympia = [47.041917, -122.893766]

def unpack(origin, destination):
    if len(origin) == 2:
        lat_d1, lon_d1 = origin
    elif len(origin) == 3:
        pass
    else:
        assert 1==0
    if len(destination) == 2:
        lat_d2, lon_d2 = destination
    elif len(destination) == 3:
        pass
    else:
        assert 1==0
    return [math.radians(lat_d1), math.radians(lon_d1), math.radians(lat_d2), math.radians(lon_d2)]

def distance(origin, destination):
    [lat1, lon1, lat2, lon2] = unpack(origin, destination)
    radius = km
    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) \
        * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def ini_bearing(origin, destination):
    [lat1, lon1, lat2, lon2] = unpack(origin, destination)
    y = math.sin(lon2-lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)
    brng = math.atan2(y, x) # radians
    return brng

