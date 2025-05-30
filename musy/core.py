"""Basic musy building blocks"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['BASE_NOTES', 'CHROMATIC_NOTES', 'ENHARMONIC_NOTES', 'INTERVALS', 'Note']

# %% ../nbs/00_core.ipynb 3
from fastcore.all import *
from mingus.core import chords, notes, intervals

# %% ../nbs/00_core.ipynb 6
BASE_NOTES = ["C", "D", "E", "F", "G", "A", "B"]
CHROMATIC_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ENHARMONIC_NOTES = ["C", "C#", "Db", "D", "D#", "Eb", "E", "Fb", "E#", "F", "F#", "Gb",
                    "G", "G#", "Ab", "A", "A#", "Bb", "B", "Cb", "B#"]
INTERVALS = ["1", "b2", "2", "b3", "3", "4", "#4", "5", "b6", "6", "b7", "7"]

# %% ../nbs/00_core.ipynb 9
class Note(BasicRepr):
    def __init__(self, note: str):
        # Transform note to uppercase
        note = note[0].upper() + note[1:]
        assert notes.is_valid_note(note), f"Note '{note}' is not valid"
        self.note = self.postprocess_note(notes.remove_redundant_accidentals(note))

    @staticmethod
    def postprocess_note(note: str):
        """ Get rid of unnecessary accidentals."""
        if note == "B#": note = "C"
        elif note == "E#": note = "F"
        elif note == "Cb": note = "B"
        elif note == "Fb": note = "E"
        elif note.endswith("##"):
            note = BASE_NOTES[BASE_NOTES.index(note[0])+1]
        elif note.endswith("bb"):
            note = BASE_NOTES[BASE_NOTES.index(note[0])-1]
        return str(note)
    
    def __str__(self): return self.note
    def __eq__(self, other): return str(self) == str(other)
    def __ne__(self, other): return not str(self) == str(other) 

# %% ../nbs/00_core.ipynb 15
@patch
def __add__(self:Note, semitones: int):
    """Add n semitones to a note."""
    return Note(intervals.from_shorthand(str(self), INTERVALS[(semitones)%12]))

# %% ../nbs/00_core.ipynb 19
@patch
def __sub__(self:Note, semitones: int):
    return Note(intervals.from_shorthand(str(self), INTERVALS[(semitones)%12], False))

# %% ../nbs/00_core.ipynb 24
@patch
def augment(self:Note):
    return Note(str(self) + "#" if str(self)[-1] != "b" else str(self)[:-1])

# %% ../nbs/00_core.ipynb 29
@patch
def diminish(self:Note):
    return Note(str(self) + "b" if str(self)[-1] != "#" else str(self)[:-1])

# %% ../nbs/00_core.ipynb 36
@patch
def interval(self:Note, other:Note, short=False):
    return intervals.determine(str(self), str(other), short)

# %% ../nbs/00_core.ipynb 43
@patch
def minor(self:Note): return self - 3

# %% ../nbs/00_core.ipynb 46
@patch
def major(self:Note): return self + 3
