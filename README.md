R12 DXF JPSA converter
======================

## Program Description

V1.0

This python script reads R12 DXF files and checks that they are in the correct format to be imported by the JPSA machining software for the fabrication of paper microfluidics.

Currently the script performs the following operations:

1. Deletes all POLYLINE entities and replaces them with LINE entities.
2. Checks that only ARC, CIRCLE, VIEWPORT and LINE entities are present in the file
3. Locates well locations (wells are red circles with radius less than 5 mm) and fills them in with concentric circles
4. Locates boundary square - reports error if does not exist
5. Checks to see if all entities are within the boundary square

Things that are still required:

1. Check for discontinuities
2. Move all entities so that the boundary square left corner is at the origin
3. Check that design is not overly complex (too many entities)


## Installation

This script has been testing with Python 2.7

https://www.python.org/download/releases/2.7.7/

It requires the ezdxf library to be installed.

https://pypi.python.org/pypi/ezdxf/0.3.0

An easy way to install ezdxf is to install pip first

http://pip.readthedocs.org/en/latest/installing.html

