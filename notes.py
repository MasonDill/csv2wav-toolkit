import argparse as ap

frequencies = {
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

def get_center_note_freq(note):
    if note not in frequencies:
        raise ValueError("Invalid note")
    return frequencies[note]

def get_freq_octave(freq, octave):
    return freq * (2 ** (octave-4))

def get_note_freq(note, octave):
    base_freq = get_center_note_freq(note)
    print(get_freq_octave(base_freq, octave))

def next_tone(note, octave):
    notes = list(frequencies.keys())
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
        for note in frequencies:
            print(note, frequencies[note])
        exit()
    get_note_freq(args.note, args.octave)