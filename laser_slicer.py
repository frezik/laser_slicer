import argparse

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
            help = 'Stop slicing at a given height, in mm (inclusive)' )
    parser.add_argument( '--layer-height',
            metavar = 'mm',
            type = float,
            required = True,
            help = 'Height of each layer' )
    parser.add_argument( '--output-type',
            metavar = 'output_type',
            type = str,
            default = 'dxf',
            choices = [ 'svg', 'dxf' ],
            help = 'Output file type' )
    parser.add_argument( '--start-height',
            metavar = 'mm',
            default = 0.1,
            type = float,
            help = 'Start slicing at a given height, in mm (inclusive)' )
    args = parser.parse_args()
    return args


args = parse_args();
