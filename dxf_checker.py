import ezdxf
import math

# parameter settings
file_name = "error.dxf"
laser_spot_diameter = 0.1  # mm - used as distance between concentric circles for filling in wells.
max_permitted_boundary_square = 50.0  # mm
boundary_square_expected_color = 240  # 240 = red
well_expected_color = 240
well_expected_max_radius = 5

# function for finding the bounds of an ARC entity (there is almost certainly a smarter way of doing this...)
def findArcMaxMin(center_point, radius_size, start_angle, end_angle):
    max_and_min_points = []  # [max_x max_y min_x min_y]
    if 0 <= start_angle <= 90:
        if end_angle > start_angle and 0 <= end_angle <= 90:
            max_and_min_points.append(math.cos(start_angle)*radius_size + center_point[0])
            max_and_min_points.append(math.sin(end_angle)*radius_size + center_point[1])
            max_and_min_points.append(math.cos(end_angle)*radius_size + center_point[0])
            max_and_min_points.append(math.sin(start_angle)*radius_size + center_point[1])
        elif end_angle > start_angle and 90 < end_angle <= 180:
            max_and_min_points.append(math.cos(start_angle)*radius_size + center_point[0])
            max_and_min_points.append(radius_size + center_point[1])
            # two possibilities for min y
        elif end_angle > start_angle and 180 < end_angle <= 270:
            max_and_min_points.append(math.cos(start_angle)*radius_size + center_point[0])
            max_and_min_points.append(radius_size + center_point[1])
        elif end_angle > start_angle and 270 < end_angle <= 360:
            max_and_min_points.append(math.cos(start_angle)*radius_size + center_point[0])
            max_and_min_points.append(radius_size + center_point[1])
        elif end_angle < start_angle and 0 <= end_angle <= 90:
            max_and_min_points.append(math.cos(end_angle)*radius_size + center_point[0])
            max_and_min_points.append(math.sin(start_angle)*radius_size + center_point[1])
    elif 90 < start_angle <= 180:
        pass
    elif 180 < start_angle <= 270:
        pass
    elif 270 < start_angle <= 360:
        pass
    return max_and_min_points

dwg = ezdxf.readfile(file_name)
modelspace = dwg.modelspace()

# locate boundary square and check it's size
boundary_square_points = []
for e in modelspace:
    if e.dxftype() == "POLYLINE":
        if e.get_dxf_attrib("color") == boundary_square_expected_color:
            for p in e.points():
                boundary_square_points.append(p)
if len(boundary_square_points) == 4:
    boundary_square_min = min(boundary_square_points)
    boundary_square_max = max(boundary_square_points)
    if boundary_square_max[0]-boundary_square_min[0] > max_permitted_boundary_square + 1 \
        and boundary_square_max[1]-boundary_square_min[1] > max_permitted_boundary_square + 1:
        print "detected boundary size: " + str(boundary_square_max[0]-boundary_square_min[0]) \
        + " mm x " + str(boundary_square_max[1]-boundary_square_min[1]) + " mm"
        print "ERROR: boundary square too large - should be less than %s mm x %s mm" \
              % (max_permitted_boundary_square, max_permitted_boundary_square)
else:
    print "ERROR: no boundary square detected"

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
for e in modelspace:
    # print("DXF Entity: %s\n" % e.dxftype())
    if not (e.dxftype() == "LINE" or e.dxftype() == "ARC" or e.dxftype() == "VIEWPORT" or e.dxftype() == "CIRCLE"):
        print "ERROR: illegal %s entity detected " % e.dxftype()

# check design is within size limit
for e in modelspace:
    # check all LINE entities
    if e.dxftype() == "LINE":
        start_point = e.get_dxf_attrib("start")
        end_point = e.get_dxf_attrib("end")
        if start_point[0] < boundary_square_min[0] \
            or start_point[1] < boundary_square_min[1] \
            or start_point[0] > boundary_square_max[0] \
            or start_point[1] > boundary_square_max[1]:
            print "ERROR: LINE entity outside of boundary square"
    # check all CIRCLE entities
    elif e.dxftype() == "CIRCLE":
        center_point = e.get_dxf_attrib("center")
        radius_size = e.get_dxf_attrib("radius")
        if (center_point[0] - radius_size) < boundary_square_min[0] \
            or (center_point[1] - radius_size) < boundary_square_min[1] \
            or (center_point[0] + radius_size) > boundary_square_max[0] \
            or (center_point[1] + radius_size) > boundary_square_max[1]:
            print "ERROR: CIRCLE entity outside of boundary square"
    # check all ARC entities
    elif e.dxftype() == "ARC":
        center_point = e.get_dxf_attrib("center")
        radius_size = e.get_dxf_attrib("radius")
        start_angle = e.get_dxf_attrib("start_angle")
        end_angle = e.get_dxf_attrib("end_angle")
        # print "%s, %s, %s, %s" % (center_point, radius_size, start_angle, end_angle)
        max_point = findArcMaxMin(center_point, radius_size, start_angle, end_angle)
        print max_point




# attempt to detect discontinuities
pass

# count entities
pass

# locate and draw wells
for e in modelspace:
    if e.dxftype() == "CIRCLE":
        radius = e.get_dxf_attrib("radius")
        color = e.get_dxf_attrib("color")
        center = e.get_dxf_attrib("center")
        if color == well_expected_color and radius < well_expected_max_radius:
            for i in range(0, int(math.floor(radius/laser_spot_diameter)-1)):
                modelspace.add_circle(center, radius-laser_spot_diameter*(i+1))

# Move all entities so that the bottom left of the boundary square is located at the origin.
pass

dwg.saveas(file_name.replace('.dxf', '') + "_converted.dxf")