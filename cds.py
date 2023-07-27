#define the composer digital signal class with frequency, duration, sample_rate=44100, bit_depth=16, channels=1, function='sin'
import dfg as dfg

class wave:
    def __init__(self, frequency, duration, sample_rate=44100, bit_depth=16, channels=1, function='sin', start_time=0):
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
    
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.channels = channels
        self.function = function
        self.start_time = start_time

    # def __add__(self, other):
    #     #call the dfg function and return the result

    # def __mul__(self, other):
    #     if constsant, scale the data
    #     if wave, convolve, mix, or mux the data

#A composer digital signal is csv data with a sample rate, bit depth, and number of channels
class cds:
    def __init__(self, sample_rate=44100, bit_depth=16, channels=1, data=None):
        if sample_rate <= 0:
            raise ValueError("sample_rate must be greater than 0")
        if channels <= 0:
            raise ValueError("channels must be greater than 0")
        if bit_depth <= 0:
            raise ValueError("bit_depth must be greater than 0")
        
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.channels = channels
        self.data = data
    
    def __add__(self, other):
        if isinstance(other, wave):
            self = dfg.dfg(other, self.data)