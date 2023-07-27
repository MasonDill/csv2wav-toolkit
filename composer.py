import notes as notes
import dfg as dfg
import numpy as np
import csv2wav as csv2wav
import common as common

import argparse as ap
#Take an array of tuples {note, octave, start, duration}
#Generate a csv file with the tuples
#Generate a wav file from the csv file

def compose(script, output_file, sample_rate=44100, bit_depth=16, channels=1, save_csv=False, save_wav=True):
    #check paramter sanity
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")
    if channels <= 0:
        raise ValueError("channels must be greater than 0")
    if output_file is None:
        raise ValueError("output_file must be provided")
    
    #infer dtype
    if(bit_depth == 16):
        dtype = np.float16
    elif(bit_depth == 32):
        dtype = np.float32
    elif(bit_depth == 64):
        dtype = np.float64
    
    #create csv data
    data = []
    for line in script:
        note = line[0]
        octave = int(line[1])
        start = float(line[2])
        duration = float(line[3])
        freq = notes.get_freq_octave(notes.get_note_freq(note), octave)
        data.append((freq, start, duration))

    #sort data by start time + duration (end time)
    data.sort(key=lambda x: x[1] + x[2])
    total_duration = data[-1][1] + data[-1][2]

    #generate csv file
    dfg_data = np.zeros(int(total_duration* sample_rate), dtype=dtype)
    for line in data:
        freq = line[0]
        start = line[1]
        duration = line[2]
        dfg.dfg(freq, duration=duration, sample_rate=sample_rate, bit_depth=bit_depth, channels=channels, start_time=start, data=dfg_data, function='sin')

    #generate wav file
    if save_wav:
        csv2wav.csv2wav(dfg_data, output_file, bit_depth=bit_depth, channels=channels, sample_rate=sample_rate)
    if save_csv:
        common.save_csv(dfg_data, output_file + '.csv', channels=channels, delimiter=',')

def compile_composer_script(input_file):
    data = np.genfromtxt(input_file, delimiter=',', dtype=str)
    return data

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='composer', description='Generate a wav file from a composer script')
    parser.add_argument('script', type=str, help='Script file')
    parser.add_argument('output_file', type=str, help='Output file name')
    parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate')
    parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth')
    parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels')
    parser.add_argument('--save_csv', action='store_true', help='Save csv file')
    args = parser.parse_args()

    script = compile_composer_script(args.script)
    compose(script, args.output_file, args.sample_rate, args.bit_depth, args.channels, args.save_csv)