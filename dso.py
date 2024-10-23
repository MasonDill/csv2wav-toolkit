#digital signal oscilloscope
import numpy as np
import argparse as ap
import matplotlib.pyplot as plt
import scipy as sp

import common

def dso(data, output_file, sample_rate=44100, bit_depth=16, channels=1, duration=None):
    #check paramter sanity
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")
    if channels <= 0:
        raise ValueError("channels must be greater than 0")
    if data is None:
        raise ValueError("data must be provided")
    
    if duration is None:
        duration = data.size / sample_rate

    print("Duration:", duration)
    
    #for simplicity, we will assume the signal sample rate is the same as the oscilloscope sample rate
    #create a linspace for the x axis where each segment is 1/sample_rate
    time_axis = np.linspace(0, duration, int(duration * sample_rate))

    if(time_axis.shape[0] < data.shape[0]):
        data = data[:time_axis.shape[0]]
    elif(time_axis.shape[0] > data.shape[0]):
        data = np.pad(data, (0, time_axis.shape[0] - data.shape[0]), 'constant', constant_values=(0, 0))

    #plot the data
    plt.plot(time_axis, data)

    #upscale the plot
    plt.gcf().set_size_inches(18.5, 10.5)

    #save the plot
    time_plot_file = output_file + "_time.svg"
    plt.savefig(time_plot_file)

    #plot the fourier transform
    fourier_transform(data, sample_rate, duration, output_file)


def fourier_transform(data, sample_rate, duration, output_file):
    # Perform Fourier transform
    fft_result = np.fft.fft(data)
    frequencies = np.fft.fftfreq(len(data)) * sample_rate

    plt.clf()
    # Plot the Fourier transform
    plt.plot(frequencies, np.abs(fft_result))

    #upscale the plot
    plt.gcf().set_size_inches(18.5, 10.5)

    #label the plot
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')

    #save the plot
    freq_plot_file = output_file + "_freq.svg"
    plt.savefig(freq_plot_file)

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='dso', description='Digital Signal Oscilloscope')
    parser.add_argument('input_file', type=str, help='Input file')
    parser.add_argument('-s', '--sample_rate', type=int, default=44100, help='Sample rate')
    parser.add_argument('-b', '--bit_depth', type=int, default=16, help='Bit depth')
    parser.add_argument('-c', '--channels', type=int, default=1, help='Number of channels')
    parser.add_argument('-t', '--duration', type=float, default=None, help='Duration of time to plot')
    parser.add_argument('-d', '--delimiter', type=str, default=',', help='Delimiter for csv file')
    args = parser.parse_args()

    data = common.read_csv(args.input_file, args.delimiter, args.bit_depth, args.channels)
    dso(data, args.sample_rate, args.bit_depth, args.channels, args.duration)