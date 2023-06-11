import numpy as np
import wave as wv
import argparse as ap

def csv2wav(input_file, output_file, delimiter=',', sample_rate=44100, bit_depth=16, channels=1):
    #check paramter sanity
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")
    if output_file is None:
        raise ValueError("output_file must be provided")
    if channels <= 0:
        raise ValueError("channels must be greater than 0")
    
    #infer dtype
    if(bit_depth == 16):
        dtype = np.float16
    elif(bit_depth == 32):
        dtype = np.float32
    elif(bit_depth == 64):
        dtype = np.float64
    else:
        raise ValueError("bit_depth must be 16, 32 or 64")
    
    #parse csv
    try: data = np.genfromtxt(input_file, delimiter=delimiter, dtype=dtype)
    except Exception as e:
        raise ValueError("Could not parse csv data:", e)
    
    #write wav
    wave_file = wv.open(output_file, 'w')
    wave_file.setparams((channels, bit_depth//8, sample_rate, len(data), 'NONE', 'not compressed'))
    wave_file.writeframes(data)
    wave_file.close()

parser = ap.ArgumentParser(prog='csv2wav', description='Converts a csv file to a wav file')
parser.add_argument('input_file', type=str, help='Input file name')
parser.add_argument('output_file', type=str, help='Output file name')
parser.add_argument('-d', '--delimiter', type=str, default=',', help='Delimiter of the csv file')
parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate of the wave')
parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth of the wave')
parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels of the wave')
args = parser.parse_args()  

csv2wav(args.input_file, args.output_file, args.delimiter, args.sample_rate, args.bit_depth, args.channels)