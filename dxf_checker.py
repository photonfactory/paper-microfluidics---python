import ezdxf
import math

file_name = "square.dxf"

dwg = ezdxf.readfile(file_name)
modelspace = dwg.modelspace()

# draw LINES instead of POLYLINES
for e in modelspace:
    if e.dxftype() == "POLYLINE":
        point_array = []
        for p in e.points():
            point_array.append(p)
        for i in range(0, len(point_array)-1):
            modelspace.add_line(point_array[i], point_array[i+1])
        if e.dxf.flags == 1:  # check if the polyline is closed or not
            modelspace.add_line(point_array[len(point_array)-1], point_array[0])

# delete POLYLINES
polylines_remaining = 0
for e in modelspace:
    if e.dxftype() == "POLYLINE":
        polylines_remaining = 1
while polylines_remaining:
    for e in modelspace:
        if e.dxftype() == "POLYLINE":
            modelspace.delete_entity(e)
    polylines_remaining = 0
    for e in modelspace:
        if e.dxftype() == "POLYLINE":
            polylines_remaining = 1

# check file for illegal entities
illegal_entity_count = 0
for e in modelspace:
    # print("DXF Entity: %s\n" % e.dxftype())
    if not (e.dxftype() == "LINE" or e.dxftype() == "ARC" or e.dxftype() == "VIEWPORT" or e.dxftype() == "CIRCLE"):
        print "illegal entity: " + e.dxftype()
        illegal_entity_count += 1

if not illegal_entity_count:
    print "SUCCESS - no illegal entities found"
else:
    print "%s illegal entities detected" % illegal_entity_count

# check design is within size limit
pass

# locate and draw wells
for e in modelspace:
    if e.dxftype() == "CIRCLE":
        radius = e.get_dxf_attrib("radius")
        color = e.get_dxf_attrib("color")
        center = e.get_dxf_attrib("center")
        if color == 240 and radius < 6:
            for i in range(0, int(math.floor(radius/0.1))-1):
                modelspace.add_circle(center, radius-0.1*(i+1))

dwg.saveas(file_name.replace('.dxf', '') + "_converted.dxf")