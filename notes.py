import argparse as ap
from copy import copy
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
WESTERN_HEPTATONIC_MAJOR_SCALE = (Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.WHOLE)
WESTERN_HEPTATONIC_MINOR_SCALE = (Step.WHOLE, Step.HALF, Step.WHOLE, Step.WHOLE, Step.HALF, Step.WHOLE)

# Helper function: Get the pitch Class from a Note (e.g. C0) or Scale (e.g. CM)
def parse_pitch_class(haystack: str) -> str:
        pitch_class = ''

        note_end_index = 0
        for char in haystack:
            char = char.upper()
            if not(char in ['#', 'A', 'B', 'C', 'D', 'E', 'F', 'G']):
                break
            pitch_class += char
            note_end_index += 1
        
        if (len(pitch_class) == 2) and (pitch_class[1] == 'B') and (pitch_class[0] not in ['C', 'F']):
            previous_index = CHROMATIC_SCALE.index(pitch_class[0]) - 1
            pitch_class = CHROMATIC_SCALE[previous_index]

        if pitch_class not in CHROMATIC_SCALE:
            raise ValueError(f"Invalid note '{pitch_class}'. Provide a note from the western chromatic scale.")
        
        return pitch_class, note_end_index

class Note:
    def __init__(self, pair: str):
        self.pitch_class, note_end_index = parse_pitch_class(pair)
        octave = pair[note_end_index:]
        
        if not octave:
            raise ValueError("Missing octave. Provide an integer.")
        
        try:
            octave = int(octave)
        except ValueError:
            raise ValueError(f"Invalid octave '{octave}'. Provide an integer octave.")

        self.octave = octave

    def get_freq(self):
        base_freq = CHROMATIC_FREQ_MAP[self.pitch_class]
        return base_freq * (2 ** (self.octave-4))
    
    def __str__(self):
        return f"{self.pitch_class}{self.octave}"

class Scale:
    def __init__(self, pair: str):
        pitch_class, note_end_index = parse_pitch_class(pair)

        scale_type = pair[note_end_index:]
        if(scale_type not in ["M","m"]):
            raise ValueError("Invalid scale type " +scale_type)

        self.start_pitch_class = pitch_class
        self.type = scale_type
    
    def get_note_intervals(self) -> tuple[Step]:
        if(self.type == "M"):
            scale_type = WESTERN_HEPTATONIC_MAJOR_SCALE
        elif(self.type == "m"):
            scale_type = WESTERN_HEPTATONIC_MINOR_SCALE
        else:
            raise ValueError("Invalid scale type " +self.type)
        
        return scale_type
        
    def get_note_pattern(self) -> list:
        root_index = CHROMATIC_SCALE.index(self.start_pitch_class)
        scale_notes = [self.start_pitch_class]
        
        current_index = root_index
        for step in self.get_note_intervals():
            current_index = (current_index + step.value) % len(CHROMATIC_SCALE)
            scale_notes.append(CHROMATIC_SCALE[current_index])
        
        return scale_notes

    def __str__(self) -> str:
        return str(self.get_note_pattern())

class Chord:
    def __init__(self, scale: Scale, root_note: Note, end_note: Note):
        notes = [root_note]

        curr_note = root_note
        while((curr_note.octave < end_note.octave) or (scale.get_note_pattern().index(curr_note.pitch_class) < scale.get_note_pattern().index(end_note.pitch_class))):
            curr_note = self._next_note(curr_note, scale)
            notes.append(curr_note)
        
        self.notes = notes

    def _next_note(self, note: Note, scale: Scale) -> Note:
        if note.pitch_class not in scale.get_note_pattern():
            raise ValueError(f"Note {note.pitch_class} does not exist in scale {scale.start_pitch_class}{scale.type}")

        next_pitch_class_index = scale.get_note_pattern().index(note.pitch_class)+2

        if(next_pitch_class_index >= len(scale.get_note_pattern())):
            next_octave = note.octave+1
        else:
            next_octave = note.octave

        next_pitch_class_index %= len(scale.get_note_pattern())
        next_pitch_class = scale.get_note_pattern()[next_pitch_class_index]

        next_note = copy(note)
        next_note.pitch_class = next_pitch_class
        next_note.octave = next_octave

        return next_note

    def __str__(self) -> str:
        return ' '.join([str(note) for note in self.notes])

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='notes', description='Get information about notes, frequencies, scales, or extended chords')
    parser.add_argument('-n', '--notes', nargs='+', type=str, help='Print frequency of a set of notes: <note><octave> <note><octave> <note><octave>...')
    parser.add_argument('-a', '--all', action='store_true', help='Print all notes')
    parser.add_argument('-s', '--scale', type=str, help='Scale: <root>[M|m]')
    parser.add_argument('-c', '--chord', nargs='+', type=str, help='Print notes of a chord: <root>[M|m] <start note><octave> <end note><octave>')
    args = parser.parse_args()

    if args.all:
        for note in CHROMATIC_FREQ_MAP:
            print(note, CHROMATIC_FREQ_MAP[note])    

    elif args.notes:
        for pair in args.notes:
            try:
                note = Note(pair)
            except ValueError as e:
                print(f"Error: {e}")
                exit()

            print(pair, "-", note.get_freq())

    elif args.scale:
        try:
            scale = Scale(args.scale)
        except ValueError as e:
                print(f"Error: {e}")
                exit()
        print(scale.get_note_pattern())
    
    elif args.chord:
        scale = Scale(args.chord[0])
        root_note = Note(args.chord[1])
        end_note = Note(args.chord[2])
        chord = Chord(scale, root_note, end_note)
        print(chord)