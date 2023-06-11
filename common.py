import numpy as np

def save_csv(data, output_file, channels=1, delimiter=','):
    try: np.savetxt(output_file, data, delimiter=delimiter, fmt='%f')
    except Exception as e:
        print("Could not write csv data:", e)

    return None

def infer_dtype(bit_depth):
    #infer dtype
    if(bit_depth == 16):
        dtype = np.float16
    elif(bit_depth == 32):
        dtype = np.float32
    elif(bit_depth == 64):
        dtype = np.float64
    else:
        raise ValueError("bit_depth must be 16, 32 or 64")
    
    return dtype

def read_csv(input_file, delimiter=',', bit_depth=16, channels=1):
    dtype = infer_dtype(bit_depth)
    #parse csv
    try: data = np.genfromtxt(input_file, delimiter=delimiter, dtype=dtype)
    except Exception as e:
        raise ValueError("Could not parse csv data:", e)
    
    return data