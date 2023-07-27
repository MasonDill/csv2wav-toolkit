#digital function generator
import numpy as np
import argparse as ap
import scipy as sp

import common
import cds

#take any number of waves and return a composer digital signal of their composition
def dfg(*waves, data=None):
    if (not data is None) and (not isinstance(data, cds.cds)):
        raise ValueError("data must be a composer digital signal or None")
    if waves is None:
        raise ValueError("waves must be provided")
    
    #check that all waves have the same sample rate and bit depth
    signal_duration = 0 #this value will never be 0 since wave duration is always > 0
    for wave in waves:
        if not isinstance(wave, cds.wave):
            raise ValueError("signal must be a composer wave")
    
        if wave.sample_rate != waves[0].sample_rate:
            raise ValueError("Variable sample rates are not yet supported")
            #TODO: upsample or downsample
        if wave.bit_depth != waves[0].bit_depth:
            raise ValueError("Variable bit depths are not yet supported")
            #TODO: truncate or pad
        if wave.channels != waves[0].channels:
            raise ValueError("Variable number of channels are not yet supported")
        
        wave_duration = wave.start_time + wave.duration
        if wave_duration > signal_duration:
            signal_duration = wave_duration
    
    if data is None:
        data = np.zeros(int(signal_duration*wave.sample_rate), dtype=common.infer_dtype(wave.bit_depth))

    for wave in waves:
        #create a pointer to the function
        if wave.function == 'sin':
            fun_ptr = np.sin
        elif wave.function == 'cos':
            fun_ptr = np.cos
        elif wave.function == 'tan':
            fun_ptr = np.tan
        elif wave.function == 'sawtooth':
            fun_ptr = sp.signal.sawtooth
        elif wave.function == 'square':
            fun_ptr = sp.signal.square
        elif wave.function == 'sinc':
            fun_ptr = np.sinc
        elif wave.function == 'sinc2':
            fun_ptr = lambda x: np.sinc(x)**2
        elif wave.function == 'exp':
            fun_ptr = np.exp
        else:
            raise ValueError("function not supported")
        
        #calculate start and end index from start time and duration
        start_index = time_to_index(wave.start_time, wave.sample_rate)
        end_index = time_to_index(wave.start_time + wave.duration, wave.sample_rate)

        #generate signal
        for i in range(start_index, end_index):
                coeff = 2*np.pi*(i - start_index)* wave.frequency/wave.sample_rate
                data[i] += fun_ptr.__call__(coeff)
    
    signal = cds.cds(wave.sample_rate, wave.bit_depth, wave.channels, data)
    return signal

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

    wave = cds.wave(args.frequency, args.duration, args.sample_rate, args.bit_depth, args.channels, args.function)
    signal = dfg(wave)
    common.save_csv(signal.data, args.output_file, signal.channels, args.delimiter)