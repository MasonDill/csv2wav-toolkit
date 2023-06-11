import argparse as ap

notes = {
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

def get_note_freq(note):
    if note not in notes:
        raise ValueError("Invalid note")
    return notes[note]

def get_freq_octave(freq, octave):
    return freq * (2 ** octave)

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='notes', description='Get the frequency of a note')
    parser.add_argument('note', type=str, help='Note name')
    parser.add_argument('octave', type=int, help='Octave number')
    parser.add_argument('-a', '--all', action='store_true', help='Print all notes')
    args = parser.parse_args()
    args.note = args.note.upper()

    if args.all:
        for note in notes:
            print(note, notes[note])
        exit()
    freq = get_note_freq(args.note)
    print(get_freq_octave(freq, args.octave))