"""Stack of notes"""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_chord.ipynb.

# %% auto 0
__all__ = ['Chord', 'PolyChord']

# %% ../nbs/01_chord.ipynb 3
import numpy as np
import pandas as pd
from fastcore.all import *
from IPython.display import Audio
from mingus.core import chords as mingus_chords

from . import Note, Interval, INTERVAL_TO_SEMITONES

# %% ../nbs/01_chord.ipynb 5
class Chord(BasicRepr):
    def __init__(self, notes: List[Note]):
        self.notes = [Note(n) if isinstance(n, str) else n for n in notes]
        self.s_notes = [str(n) for n in self.notes]
        self.oct_s_notes = [f"{n.note}{n.oct}" for n in self.notes]
        self.names = mingus_chords.determine(self.s_notes)
        self.name = self.names[0] if self.names else "No chord found."
        self.root = min(self.notes, key=lambda n: n.midi)
        self.s_root = str(self.root)
        self.oct_s_root = f"{self.root.note}{self.root.oct}"

    @classmethod
    def from_short(cls, c: str): return cls(mingus_chords.from_shorthand(c)) 
    @classmethod
    def from_midi(cls, midi: list[int]): return cls([Note.from_midi(m) for m in midi])

    def __repr__(self): return f"Chord: '{self.name}'. Notes: {self.oct_s_notes}"
    def __add__(self, other): return Chord([n + other for n in self.notes])
    def __sub__(self, other): return Chord([n - other for n in self.notes])
    def __mod__(self, other): return Chord([n % other for n in self.notes])
    def __len__(self): return len(self.notes)
    def __floordiv__(self, other): return Chord([n // other for n in self.notes])
    def __iter__(self) -> list[str]: return iter(self.notes)
    def __index__(self):
        mask = 0
        for n in self.notes: mask |= 1 << n.midi
        return mask
    def __int__(self): return self.__index__()
    @property
    def midi(self): return [n.midi for n in self.notes]
    
    def _compare_notes(self, other, op): return all(op(n1, n2) for n1, n2 in zip(self.notes, other.notes))
    def __eq__(self, other): return self.root == other.root and self._compare_notes(other, lambda x, y: x == y)
    def __ne__(self, other): return not self == other
    def __lt__(self, other): return self.root < other.root or (self.root == other.root and self._compare_notes(other, lambda x, y: x < y))
    def __le__(self, other): return self.root < other.root or (self.root == other.root and self._compare_notes(other, lambda x, y: x <= y))
    def __gt__(self, other): return self.root > other.root or (self.root == other.root and self._compare_notes(other, lambda x, y: x > y))
    def __ge__(self, other): return self.root > other.root or (self.root == other.root and self._compare_notes(other, lambda x, y: x >= y))

# %% ../nbs/01_chord.ipynb 31
@patch
def __mul__(self:Note, other: Note):
    """ Form a chord from two notes. """
    return Chord([self, other])
@patch
def __mul__(self:Chord, other): 
    """ Add a note to a chord. """
    return Chord([*self.notes, other])

# %% ../nbs/01_chord.ipynb 38
@patch
def invert(self:Chord, n: int = 1):
    assert n > 0 and n < len(self.s_notes), f"Invalid inversion '{n}' for chord with '{len(self.s_notes)}' notes."
    return Chord(self.notes[n:] + [Note(str(note), oct=note.oct + 1) for note in self.notes[:n]])

# %% ../nbs/01_chord.ipynb 41
@patch
def rel_intervals(self:Chord):
    return [Interval(self.notes[0], n) for n in self.notes[1:]]

@patch
def abs_intervals(self:Chord):
    return [Interval(n1, n2) for n1, n2 in zip(self.notes, self.notes[1:])]

# %% ../nbs/01_chord.ipynb 45
@patch
def dominant(self:Chord, dim=False): 
    if not dim: # V7
        return Chord([r := self.root.P5(), r.M3(), r.P5(), r.m7()])
    else: # vii°7
        return Chord([r := self.root.dm2(), r.m3(), r.TT(), r.M6()])

# %% ../nbs/01_chord.ipynb 53
@patch
def add_interval(self:Chord, semitones: int):
    """ Add note to existing chord. """
    new_midi = self.root.midi + semitones
    notes = self.notes.copy()
    if new_midi not in self.midi:
        notes.append(Note.from_midi(new_midi))
        notes.sort(key=lambda n: n.midi)
    return Chord(notes)
@patch
def add2(self:Chord): return self.add_interval(2)
@patch
def add4(self:Chord): return self.add_interval(5)
@patch
def add6(self:Chord): return self.add_interval(9)
@patch
def add_ext(self:Chord, name: str):
    semis = INTERVAL_TO_SEMITONES.get(name)
    if semis is None: raise ValueError(f"Unknown interval: {name}")
    return self.add_interval(semis)
@patch
def remove_ext(self: Chord, name: str):
    semis = INTERVAL_TO_SEMITONES.get(name)
    if semis is None: raise ValueError(f"Unknown interval: {name}")
    target_midi = self.root.midi + semis
    notes = [n for n in self.notes if n.midi != target_midi]
    return Chord(notes)

# %% ../nbs/01_chord.ipynb 63
@patch
def get_audio_array(self:Chord, length=1):
    return np.sum([n.get_audio_array(length) for n in self.notes], axis=0)

@patch
def play(self:Chord, length=1): 
    return Audio(self.get_audio_array(length), rate=44100)

# %% ../nbs/01_chord.ipynb 69
@patch
def to_frame(self:Chord):
    rel_intervals = self.rel_intervals()
    rel_short_intvals = [i.short for i in rel_intervals]
    rel_long_intvals = [i.long for i in rel_intervals]
    abs_intervals = self.abs_intervals()
    abs_short_intvals = [i.short for i in abs_intervals]
    abs_long_intvals = [i.long for i in abs_intervals]
    
    d = {
        "Notes": self.notes,
        "Relative Degree": [1] + rel_short_intvals,
        "Relative Interval": ["unison"] + rel_long_intvals,
        "Absolute Interval": ["unison"] + abs_long_intvals,
        "Absolute Degree": [1] + abs_short_intvals,
    }
    return pd.DataFrame(d)

# %% ../nbs/01_chord.ipynb 74
class PolyChord(Chord):
    def __init__(self, chords: list[Chord]):
        self.chords = chords
        super().__init__([note for chord in chords for note in chord.notes])
    def __repr__(self): return f"PolyChord: '{'|'.join([c.name for c in self.chords])}'. Notes: {self.oct_s_notes}"

# %% ../nbs/01_chord.ipynb 78
@patch
def invert(self:PolyChord, n: int = 1):
    return PolyChord([c.invert(n) for c in self.chords])

# %% ../nbs/01_chord.ipynb 83
@patch
def to_frame(self:PolyChord) -> list[pd.DataFrame]:
    return [c.to_frame() for c in self.chords]
