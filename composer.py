from notes import Note
import dfg as dfg
import dso as dso
import csv2wav as csv2wav
import common as common
import cds as cds

import numpy as np
import argparse as ap
#Take an array of tuples {note, octave, start, duration}
#Generate a csv file with the tuples
#Generate a wav file from the csv file

def compose(script, output_file, sample_rate=44100, bit_depth=16, channels=1, save_csv=False, save_scope=False):
    #check paramter sanity
    if output_file is None:
        raise ValueError("output_file must be specified")
    
    waves = []
    for line in script:
        note = Note(line[0])
        start = float(line[1])
        duration = float(line[2])

        freq = note.get_freq()
        wave = cds.wave(frequency=freq, duration=duration, sample_rate=sample_rate, bit_depth=bit_depth, channels=channels, function='sin', start_time=start)
        waves.append(wave)

    signal = dfg.dfg(*waves)
    csv2wav.csv2wav(signal.data, output_file + '.wav', bit_depth=bit_depth, channels=channels, sample_rate=sample_rate)
    
    if save_csv:
        common.save_csv(signal.data, output_file + '.csv', channels=channels, delimiter=',')
    if save_scope:
        dso.dso(signal.data, output_file, sample_rate=sample_rate, bit_depth=bit_depth, channels=channels)

def compile_composer_script(input_file):
    data = np.genfromtxt(input_file, delimiter=',', dtype=str, comments="//")
    return data

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='composer', description='Generate a wav file from a composer script')
    parser.add_argument('script', type=str, help='Script file')
    parser.add_argument('output_file', type=str, help='Output file name')
    parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate')
    parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth')
    parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels')
    parser.add_argument('--save_csv', action='store_true', help='Save csv file')
    parser.add_argument('--save_scope', action='store_true', help='Save scope image')
    args = parser.parse_args()

    script = compile_composer_script(args.script)
    compose(script, args.output_file, args.sample_rate, args.bit_depth, args.channels, args.save_csv, args.save_scope)