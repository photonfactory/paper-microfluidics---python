import ezdxf

dwg = ezdxf.readfile("hello.dxf")
modelspace = dwg.modelspace()
illegal_entity_count = 0


for e in modelspace:
    print("DXF Entity: %s\n" % e.dxftype())
    if not (e.dxftype() == "LINE" or e.dxftype() == "ARC" or e.dxftype() == "VIEWPORT"):
        if e.dxftype() == "POLYLINE":
            # print ("Polyline type: %s" % e.get_mode())
            point_array = []
            for p in e.points():
                point_array.append(p)
            # print point_array
            modelspace.delete_entity(e)
            for i in range(0, len(point_array)-1):
                modelspace.add_line(point_array[i], point_array[i+1])
        print ("illegal entity: %s" % e.dxftype())
        illegal_entity_count += 1

if not illegal_entity_count:
    print "SUCCESS - no illegal entities found"
else:
    print "%s illegal entities detected" % illegal_entity_count

dwg.saveas("hello_modified_2.dxf")