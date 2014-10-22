#!/usr/bin/env python

import math

km = 6371.009
mi = 3958.761
nm = 3440.07

radius = nm

def unpack(origin, destination):
    if len(origin) == 2:
        lat_d1, lon_d1 = origin
    elif len(origin) == 6:
        xd, xm, xs, yd, ym, ys = origin
        lat_d1 = dms_dd(xd, xm, xs)
        lon_d1 = dms_dd(yd, ym, ys)
    else:
        assert 1==0
    if len(destination) == 2:
        lat_d2, lon_d2 = destination
    elif len(destination) == 6:
        xd, xm, xs, yd, ym, ys = destination
        lat_d2 = dms_dd(xd, xm, xs)
        lon_d2 = dms_dd(yd, ym, ys)
    else:
        assert 1==0
    return [math.radians(lat_d1), math.radians(lon_d1), math.radians(lat_d2), \
                math.radians(lon_d2)]

def dms_dd(d, m, s):
    if d != 0:
        sign = abs(d) / d
    else: # FIXME this would fail on negative zero
        sign = 1
    m = m * sign
    s = s * sign
    return d + float(m)/60 + float(s)/3600

def distance(origin, destination):
    # Adapted from code by Wayne Dyck, 2009-10-05
    [lat1, lon1, lat2, lon2] = unpack(origin, destination)
    dlat = lat2-lat1
    dlon = lon2-lon1

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1) \
        * math.cos(lat2) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def ini_bearing(origin, destination):
    # Adapted from code by Chris Veness
    # github.com/chrisveness/geodesy file latlon.js
    [lat1, lon1, lat2, lon2] = unpack(origin, destination)
    y = math.sin(lon2-lon1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - \
        math.sin(lat1) * math.cos(lat2) * math.cos(lon2-lon1)
    brng = math.atan2(y, x)
    return (math.degrees(brng) + 360) % 360

def fin_bearing(origin, destination):
    # Adapted from code by Chris Veness
    return (ini_bearing(destination, origin) + 180) % 360

### tests

rold = radius
radius = km

seattle = [47.621800, -122.350326]
olympia = [47.041917, -122.893766]
assert round(distance(seattle, olympia),2) == 76.39
assert dms_dd(1, 30, 0) == 1.5
assert dms_dd(0, 30, 0) == 0.5
assert dms_dd(-45, 30, 0) == -45.5
boat = [36, 8, 12, -13, 5, 7] # 36N8'12" 13W5'7"
gibr = [35, 58, 35, -5, 28, 37] # gibraltar
assert round(distance(boat,gibr), 1) == 684.0
assert round(ini_bearing(boat,gibr),2) == round(dms_dd(89, 14, 57),2)
assert round(fin_bearing(boat,gibr),2) == round(dms_dd(93, 43, 54),2)

radius = rold

### end tests

if radius == km:
    unit = "km"
elif radius == nm:
    unit = "nm"
elif radius == mi:
    unit = "mi"

vi = [17, 46, 52, -20, 13, 23] # near cape verde
vo = [-3, 50, 59, -32, 34, 15] # fernando de noronha
print "Distance:\t\t" , round(distance(vi,vo),2), unit
print "Initial bearing:\t", round(ini_bearing(vi,vo),1)
print "Final bearing:\t\t", round(fin_bearing(vi,vo),1)
