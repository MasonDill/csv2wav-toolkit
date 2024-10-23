import argparse as ap
from enum import Enum

# Frequencies given for the 4th octave of the chromatic scale
CHROMATIC_FREQ_MAP = {
    'C': 261.63,
    'C#': 277.18,
    'D': 293.66,
    'D#': 311.13,
    'E': 329.63,
    'F': 349.23,
    'F#': 369.99,
    'G': 392.00,
    'G#': 415.30,
    'A': 440.00,
    'A#': 466.16,
    'B': 493.88
}

class Step(Enum):
    HALF = 1
    WHOLE = 2 

CHROMATIC_SCALE = list(CHROMATIC_FREQ_MAP.keys())   
WESTERN_HEPTATONIC_MAJOR_SCALE = [Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE, Step.HALF]
WESTERN_HEPTATONIC_MINOR_SCALE = [Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE]

class Scale:
    def __init__(self, root_note, pattern):
        self.root_note = root_note
        self.pattern = pattern

    def get_notes(self):
        root_index = CHROMATIC_SCALE.index(self.root_note)
        scale_notes = [self.root_note]
        
        current_index = root_index
        for step in self.pattern:
            current_index = (current_index + step.value) % len(CHROMATIC_SCALE)
            scale_notes.append(CHROMATIC_SCALE[current_index])
        
        return scale_notes

def get_middle_note_freq(note):
    if note not in CHROMATIC_FREQ_MAP:
        raise ValueError("Invalid note")
    return CHROMATIC_FREQ_MAP[note]

def get_freq_octave(freq, octave):
    return freq * (2 ** (octave-4))

def get_note_freq(note, octave):
    base_freq = get_middle_note_freq(note)
    return get_freq_octave(base_freq, octave)

def next_tone(note, octave, scale):
    tone = scale.index(note)+2

    if(tone >= len(scale)):
        next_octave = octave+1
    else:
        next_octave = octave

    tone %= len(scale)
    next_note = scale[tone]

    return (next_note, next_octave)

def create_extended_chord(scale, root_note, low_octave, end_note, high_octave):
    chord = [[root_note, low_octave]]

    curr_octave = low_octave
    curr_note = root_note
    while(curr_octave <= high_octave and scale.index(curr_note) < scale.index(end_note)):
        (curr_note, curr_octave) = next_tone(curr_note, curr_octave, scale)
        chord.append([curr_note, curr_octave])

    return chord

def parse_note(haystack: str) -> str:
    note = ''

    note_end_index = 0
    for char in haystack:
        char = char.upper()
        if not(char in ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G']):
            break
        note += char
        note_end_index += 1
    
    if (len(note) == 2) and (note[1] == 'B') and (note[0] not in ['C', 'F']):
        previous_index = CHROMATIC_SCALE.index(note[0]) - 1
        note = CHROMATIC_SCALE[previous_index]

    if note not in CHROMATIC_SCALE:
        raise ValueError(f"Invalid note '{note}'. Provide a note from the western chromatic scale.")
    
    return note, note_end_index

def parse_note_octave_pair(pair: str) -> tuple[str, int]:
    note, note_end_index = parse_note(pair)
    octave = pair[note_end_index:]
    
    if not octave:
        raise ValueError("Missing octave. Provide an integer.")
    
    try:
        octave = int(octave)
    except ValueError:
        raise ValueError(f"Invalid octave '{octave}'. Provide an integer octave.")

    return (note, octave)

def parse_scale(pair):
    root, note_end_index = parse_note(pair)

    scale_type = pair[note_end_index:]
    if(scale_type == "M"):
        scale_type = WESTERN_HEPTATONIC_MAJOR_SCALE
    elif(scale_type == "m"):
        scale_type = WESTERN_HEPTATONIC_MINOR_SCALE
    else:
        raise ValueError("Invalid scale type " +scale_type)

    return Scale(root, scale_type)

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='notes', description='Get information about notes, frequencies, scales, or extended chords')
    parser.add_argument('-n', '--notes', nargs='+', type=str, help='Print frequency of a set of notes: <note><octave> <note><octave> <note><octave>...')
    parser.add_argument('-a', '--all', action='store_true', help='Print all notes')
    parser.add_argument('-s', '--scale', type=str, help='Scale: <root>[M|m]')
    parser.add_argument('--extended-chord', nargs='+', type=str, help='Print notes of an extended chord: <root>[M|m] <start note><octave> <end note><octave>')
    args = parser.parse_args()

    if args.all:
        for note in CHROMATIC_FREQ_MAP:
            print(note, CHROMATIC_FREQ_MAP[note])    

    elif args.notes:
        for pair in args.notes:
            try:
                (note, octave) = parse_note_octave_pair(pair)
            except ValueError as e:
                print(f"Error: {e}")
                exit()

            print(pair, "-", get_note_freq(note, octave))

    elif args.scale:
        try:
            scale = parse_scale(args.scale)
        except ValueError as e:
                print(f"Error: {e}")
                exit()
        print(scale.get_notes())
    
    elif args.extended_chord:
        scale = parse_scale(args.extended_chord[0])
        (start_note, start_octave) = parse_note_octave_pair(args.extended_chord[1])
        (end_note, end_octave) = parse_note_octave_pair(args.extended_chord[2])
        print(create_extended_chord(scale, start_note, start_octave, end_note, end_octave))