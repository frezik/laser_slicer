# Copyright (c) 2017  Timm Murray
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
import argparse
import tempfile


def parse_args():
    parser = argparse.ArgumentParser(
            description='Slice a 3D model into a vector file for laser cutting' );
    parser.add_argument( '--input',
            metavar = 'input_file',
            type = str,
            required = True,
            help = 'Input file path' )
    parser.add_argument( '--end-height',
            metavar = 'mm',
            type = float,
            required = True,
            dest = 'end_height',
            help = 'Stop slicing at a given height, in mm' )
    parser.add_argument( '--layer-height',
            metavar = 'mm',
            type = float,
            required = True,
            dest = 'layer_height',
            help = 'Height of each layer' )
    parser.add_argument( '--output-type',
            metavar = 'output_type',
            type = str,
            default = 'dxf',
            dest = 'output_type',
            choices = [ 'svg', 'dxf' ],
            help = 'Output file type' )
    parser.add_argument( '--start-height',
            metavar = 'mm',
            default = 0.1,
            type = float,
            dest = 'start_height',
            help = 'Start slicing at a given height, in mm' )
    args = parser.parse_args()
    return args

def get_scad_tmp_file():
    scad_file = tempfile.NamedTemporaryFile( delete = False )
    scad_file_name = scad_file.name
    scad_file.close()
    return scad_file_name

def slice_model( tmp_file, start_height, layer_height, end_height ):
    layer_height = args.start_height
    layer_count = 1
    while( layer_height < args.end_height ):
        print "Creating layer " + str( layer_count ) + " at height " + str( layer_height )
        layer_count += 1
        layer_height += args.layer_height


args = parse_args()
print "Input file: " + args.input
print "Start slicing height: " + str( args.start_height )
print "End slicing height: " + str( args.end_height )
print "Layer height: " + str( args.layer_height )

scad_file_name = get_scad_tmp_file()
slice_model(
        tmp_file = scad_file_name,
        start_height = args.start_height,
        layer_height = args.layer_height,
        end_height = args.end_height )
