import argparse as ap
from enum import Enum
from abc import ABC, abstractmethod

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
    def __init__(self, root_note: str, pattern: list[Step]):
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

class Step(Enum):
    HALF = 1
    WHOLE = 2

class Scale:
    WESTERN_HEPTATONIC_MAJOR_SCALE = [Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE, Step.HALF]
    WESTERN_HEPTATONIC_MINOR_SCALE = [Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE]

    def __init__(self, root_note: str, pattern: list[Step]):
        self.root_note = root_note
        self.pattern = pattern

    def get_notes(self):
        # Find the index of the root note in the chromatic scale
        root_index = CHROMATIC_SCALE.index(self.root_note)
        scale_notes = [self.root_note]
        
        # Calculate the notes of the scale using the step pattern
        current_index = root_index
        for step in self.pattern:
            # Move by the appropriate number of semitones (1 for HALF, 2 for WHOLE)
            current_index = (current_index + step.value) % len(CHROMATIC_SCALE)
            scale_notes.append(CHROMATIC_SCALE[current_index])
        
        return scale_notes

# Western heptatonic scale patterns
WESTERN_HEPTATONIC_MAJOR_SCALE = [Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE, Step.HALF]
WESTERN_HEPTATONIC_MINOR_SCALE = [Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE]

# Example usage
c_major_scale = Scale("C", WESTERN_HEPTATONIC_MAJOR_SCALE)
print(c_major_scale.get_notes())  # Output: ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C']

a_minor_scale = Scale("A", WESTERN_HEPTATONIC_MINOR_SCALE)
print(a_minor_scale.get_notes())  # Output: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A']


def get_center_note_freq(note):
    if note not in CHROMATIC_FREQ_MAP:
        raise ValueError("Invalid note")
    return CHROMATIC_FREQ_MAP[note]

def get_freq_octave(freq, octave):
    return freq * (2 ** (octave-4))

def get_note_freq(note, octave):
    base_freq = get_center_note_freq(note)
    print(get_freq_octave(base_freq, octave))

def next_tone(note, octave):
    notes = list(CHROMATIC_FREQ_MAP.keys())
    tone = notes.index(note)+2 # move up two half steps

    if(tone >= len(tone)):
        next_octave = octave+1
    else:
        next_octave = octave

    tone %= len(notes)
    next_note = notes[tone]

    return (next_note, next_octave)

def create_extended_chord(note, low_octave, high_octave):
    #typical chord is a root, third, fifth, etc
    chord = [[note, low_octave]]

    curr_octave = low_octave
    curr_note = note
    while(curr_octave <= high_octave):
        (curr_note, curr_octave) = next_tone(curr_note, curr_octave)
        chord.append([curr_note, curr_octave])

    return chord

def create_extended_chord_freqencies(note, low_octave, high_octave):
    chord = create_extended_chord(note, low_octave, high_octave)
    chord_freqs =[]
    for note_pair in chord:
        freq = get_note_freq(note_pair[0], note_pair[1])
        chord_freqs.append(freq)

    return (chord, chord_freqs)
        

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='notes', description='Get the frequency of a note')
    parser.add_argument('note', type=str, help='Note name')
    parser.add_argument('octave', type=int, help='Octave number')
    parser.add_argument('-a', '--all', action='store_true', help='Print all notes')
    args = parser.parse_args()
    args.note = args.note.upper()

    if args.all:
        for note in CHROMATIC_FREQ_MAP:
            print(note, CHROMATIC_FREQ_MAP[note])
        exit()
    get_note_freq(args.note, args.octave)