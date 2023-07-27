#digital function generator
import numpy as np
import argparse as ap
import scipy as sp

import common

def dfg(frequency, duration, sample_rate=44100, bit_depth=16, channels=1, function='sin', data=None, start_time=0):
    #check paramter sanity
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")
    if channels <= 0:
        raise ValueError("channels must be greater than 0")
    if frequency is None:
        raise ValueError("frequency must be provided")
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
        
    if data is None:
        data = np.zeros(duration*sample_rate, dtype=dtype)

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
    start_index = time_to_index(start_time, sample_rate)
    end_index = time_to_index(start_time + duration, sample_rate)
    for i in range(start_index, end_index):
            coeff = 2*np.pi*(i - start_index)* frequency/sample_rate
            data[i] += fun_ptr.__call__(coeff)
    
    return data

def time_to_index(time, sample_rate):
    return int(time * sample_rate)

    
if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='dfg', description='Digital Function Generator')
    parser.add_argument('frequency', type=float, help='Frequency of the wave')
    parser.add_argument('output_file', type=str, help='Output file name')
    parser.add_argument('duration', type=int, help='Duration of the wave in seconds')
    parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate of the wave')
    parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth of the wave')
    parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels of the wave')
    parser.add_argument('-f', '--function', type=str, default='sin', help='Function to generate the wave')
    parser.add_argument('-d', '--delimiter', type=str, default=',', help='Delimiter for csv file')
    args = parser.parse_args()

    data = dfg(args.frequency, args.duration, args.sample_rate, args.bit_depth, args.channels, args.function)
    common.save_csv(data, args.output_file, args.channels, args.delimiter)


#define the composer digital signal class with frequency, duration, sample_rate=44100, bit_depth=16, channels=1, function='sin'
class cds: