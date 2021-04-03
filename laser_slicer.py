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
import os
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
            description='Slice a 3D model into a vector file for laser cutting')
    parser.add_argument('--input',
                        metavar='input_file',
                        type=str,
                        required=True,
                        help='Input file path')

    parser.add_argument('--end-height',
                        metavar='mm',
                        type=float,
                        required=True,
                        dest='end_height',
                        help='Stop slicing at a given height, in mm')

    parser.add_argument('--layer-height',
                        metavar='mm',
                        type=float,
                        required=True,
                        dest='layer_height',
                        help='Height of each layer')

    parser.add_argument('--output-type',
                        metavar='output_type',
                        type=str,
                        default='dxf',
                        dest='output_type',
                        choices=['svg', 'dxf'],
                        help='Output file type')

    parser.add_argument('--start-height',
                        metavar='mm',
                        default=0.1,
                        type=float,
                        dest='start_height',
                        help='Start slicing at a given height, in mm')

    arguments = parser.parse_args()

    return arguments


def get_scad_temp_file(input_file):
    scad_file_path = os.path.dirname(os.path.abspath(__file__))
    temp_scad_file_name = os.path.join(scad_file_path, input_file+'temp')
    return temp_scad_file_name


def slice_model(
    output_type,
    model_name,
    start_height,
    layer_height,
    end_height
):
    scad_temp_file = get_scad_temp_file(model_name)
    current_layer_height = start_height
    layer_count = 1
    while current_layer_height < end_height:
        print("Creating layer " + str(layer_count) + " at height " + str(current_layer_height))
        create_slice(
                output_type=output_type,
                model_name=model_name,
                tmp_file=scad_temp_file,
                slice_height=current_layer_height,
                layer_count=layer_count)
        layer_count += 1
        current_layer_height += layer_height
    os.remove(scad_temp_file)

def create_slice(
    output_type,
    model_name,
    tmp_file,
    slice_height,
    layer_count
):
    out_model_file_name = make_output_file_name(
        output_type, model_name, layer_count)

    print("    Outputting to " + out_model_file_name)
    with open(tmp_file, 'w') as out_scad:
        out_scad.write('projection( cut = true )'
                       ' translate( v = [ 0, 0, -' + str(slice_height) + ' ] )'
                       ' import( "' + os.path.abspath(model_name) + '" ); ')

    run_openscad(out_model_file_name, tmp_file)


def make_output_file_name(output_type, model_name, layer_count):
    stripped_model_name, _ = os.path.splitext(model_name)
    file_name = stripped_model_name + '_' + str(layer_count).zfill(4) + '.' + output_type
    return file_name


def run_openscad(out_model_file_name, scad_file):
    subprocess.call([
        'openscad',
        '-o',
        out_model_file_name,
        scad_file
    ])


if __name__ == '__main__':
    args = parse_args()
    print("Input file: " + args.input)
    print("Output type: " + args.output_type)
    print("Start slicing height: " + str(args.start_height))
    print("End slicing height: " + str(args.end_height))
    print("Layer height: " + str(args.layer_height))
    print("")
    print("=" * 10)
    print("")

    slice_model(
            output_type=args.output_type,
            model_name=args.input,
            start_height=args.start_height,
            layer_height=args.layer_height,
            end_height=args.end_height)
