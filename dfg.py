#digital function generator
import numpy as np
import argparse as ap
import scipy as sp

def dfg(frequency, output_file, duration, sample_rate=44100, bit_depth=16, channels=1, function='sin'):
    #check paramter sanity
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")
    if channels <= 0:
        raise ValueError("channels must be greater than 0")
    if frequency is None:
        raise ValueError("frequency must be provided")
    if output_file is None:
        raise ValueError("output_file must be provided")
    if duration is None:
        raise ValueError("duration must be provided")
    if duration <= 0:
        raise ValueError("duration must be greater than 0")    
    
    #infer dtype
    if(bit_depth == 16):
        dtype = np.float16
    elif(bit_depth == 32):
        dtype = np.float32
    elif(bit_depth == 64):
        dtype = np.float64
    else:
        raise ValueError("bit_depth must be 16, 32 or 64")
        
    #create csv data
    data = np.zeros((duration, sample_rate), dtype=dtype)

    #create a pointer to the function
    if function == 'sin':
        fun_ptr = np.sin
    elif function == 'cos':
        fun_ptr = np.cos
    elif function == 'tan':
        fun_ptr = np.tan
    elif function == 'sawtooth':
        fun_ptr = sp.signal.sawtooth
    elif function == 'square':
        fun_ptr = sp.signal.square
    elif function == 'sinc':
        fun_ptr = np.sinc
    elif function == 'sinc2':
        fun_ptr = lambda x: np.sinc(x)**2
    elif function == 'exp':
        fun_ptr = np.exp
    else:
        raise ValueError("function not supported")
    
    #generate wave
    for i in range(duration):
        for j in range(sample_rate):
            data[i][j] = fun_ptr.__call__(2*np.pi*j* frequency/sample_rate)

    print("Samples:", data.size)
    
    #write csv data
    try: np.savetxt(output_file, data, delimiter=',', fmt='%f')
    except Exception as e:
        print("Could not write csv data:", e)
        return None

parser = ap.ArgumentParser(prog='dfg', description='Digital Function Generator')
parser.add_argument('frequency', type=float, help='Frequency of the wave')
parser.add_argument('output_file', type=str, help='Output file name')
parser.add_argument('duration', type=int, help='Duration of the wave in seconds')
parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate of the wave')
parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth of the wave')
parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels of the wave')
parser.add_argument('-f', '--function', type=str, default='sin', help='Function to generate the wave')
args = parser.parse_args()

dfg(args.frequency, args.output_file, args.duration, args.sample_rate, args.bit_depth, args.channels, args.function)