Use OpenSCAD to slice a 3D model for a laser cutter. This allows you to 
build up layers of flat material and stack them for a 3D shape.

This requires OpenSCAD to be installed on your local machine.

Usage:

laser_slicer.py [-h] --input input_file --end-height mm --layer-height
                       mm [--output-type output_type] [--start-height mm]

optional arguments:
  --input input_file    Input file path
  --end-height mm       Stop slicing at a given height, in mm
  --layer-height mm     Height of each layer
  --output-type output_type
                        Output file type
  --start-height mm     Start slicing at a given height, in mm
