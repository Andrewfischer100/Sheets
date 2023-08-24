import librosa
import matplotlib.pyplot as plt
import numpy as np
import time

from timer import Timer

filename = librosa.example('nutcracker')
# audio_file_path = "Reference Scales_On C.mp3"

with Timer("File loaded in {:0.4f} seconds"):
    print("Loading file: %s" % filename)
    audio, samplerate = librosa.load(filename)

print("Detecting tempo")
tempo = librosa.feature.tempo(y=audio, sr=samplerate)
print("Tempo = %d" % tempo[0])

with Timer("Frequency detection done in {:0.4f} seconds"):
    print("Detecting frequencies")
    freqs, voiced_flag, voiced_probs = librosa.pyin(
        y=audio,
        fmin=librosa.note_to_hz('C2'),
        fmax=librosa.note_to_hz('C7'),
        sr=samplerate)

times = librosa.times_like(freqs)
# print("Constructing fundamental frequency spectrogram")
# D = librosa.amplitude_to_db(
#     np.abs(librosa.stft(audio)), 
#     ref=np.max)
# fig, ax = plt.subplots()
# img = librosa.display.specshow(
#     D, 
#     x_axis='time', 
#     y_axis='log', 
#     ax=ax)
# ax.set(title='pYIN fundamental frequency estimation')
# fig.colorbar(img, ax=ax, format="%+2.f dB")
# ax.plot(times, freqs, label='freqs', color='cyan', linewidth=3)
# ax.legend(loc='upper right')
# fig.show()
# input("Press Enter to continue...")


notes = []
onsetDetectionTimes = librosa.onset.onset_detect(y=audio, sr=samplerate, units='time')
for i in onsetDetectionTimes:
        notes.append(librosa.hz_to_note(i))
notes_string = ",".join(notes)
print("Notes based on Onset Detection: " + notes_string)
