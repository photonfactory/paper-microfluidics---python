R12 DXF JPSA converter
======================

## Program Description

This python script reads R12 DXF files and checks that they are in the correct format to be imported by the JPSA machining software for the fabrication of paper microfluidics.

Currently the script performs the following operations:

1. Deletes all POLYLINE entities and replaces them with LINE entities.
2. Checks that only ARC, CIRCLE, VIEWPORT and LINE entities are present in the file
3. Locates well locations and fills them in with concentric circles

Things that are still to come:

1. Check that the design fits within a 100 by 100 mm square area
2. Checks to ensure the design is not overly complex (too many entities)
3. ability to run the script with the filename to be converted as an argument
4. establish a list of error codes

## Installation

This script has been testing with Python 2.7

https://www.python.org/download/releases/2.7.7/

It requires the ezdxf library to be installed.

https://pypi.python.org/pypi/ezdxf/0.3.0

An easy way to install ezdxf is to install pip first

http://pip.readthedocs.org/en/latest/installing.html

