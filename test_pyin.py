import librosa
import numpy as np
y = np.zeros(2048)
f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('E3'), fmax=librosa.note_to_hz('C7'))
print(f0)
