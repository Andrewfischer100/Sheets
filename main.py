import librosa
import matplotlib.pyplot as plt
import numpy as np
import time
from pathlib import Path

from musictree.score import Score
from musictree.part import Part
from musictree.measure import Measure
from musictree.staff import Staff
from musictree.voice import Voice
from musictree.beat import Beat
from musictree.chord import Chord

# Create score
score = Score()
part = score.add_child(Part('P1', name='Part 1'))
measure = part.add_child(Measure(number=1))
staff = measure.add_child(Staff(number=1))
voice = staff.add_child(Voice(number=1))

# filename = librosa.example('nutcracker')
<<<<<<< HEAD
filename = "/Reference Scales_On C.mp3"
filePath = Path(str(Path(__file__).parent) + filename)
=======
filename = "Reference Scales_On C.mp3"
filePath = Path(str(Path(__file__).parent) + "/" + filename)
>>>>>>> c7fe82ea1054f3ad5295817cfd9247b4947a7407

print("Loading file: %s" % filename)
loadStartTime = time.time()
audio, samplerate = librosa.load(filePath)
loadEndTime = time.time()
loadTime = loadEndTime - loadStartTime
print("File loaded in %.2f seconds" % loadTime)

tempo = librosa.feature.tempo(y=audio, sr=samplerate)
print("Tempo = %d" % tempo[0])

print("pyin")
pyinStartTime = time.time()
freqs, voiced_flag, voiced_probs = librosa.pyin(
    y=audio, 
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7'),
    sr=samplerate)
pyinEndTime = time.time()
pyinTime = pyinEndTime - pyinStartTime
print("pyin done in %.2f seconds" % pyinTime)

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

print("onset_detect")
onsetDetectStartTime = time.time()
onsetDetectionTimes = librosa.onset.onset_detect(y=audio, sr=samplerate, units='frames')
onsetDetectEndTime = time.time()
onsetDetectTime = onsetDetectEndTime - onsetDetectStartTime
print("onset_detect done in %.2f seconds" % onsetDetectTime)
# print(onsetDetectionTimes)

quarterNoteInSeconds = 60.0 / float(tempo[0])
quarterNoteIndexSpacing = np.round(quarterNoteInSeconds / times[1])

# print(quarterNoteIndexSpacing)
for i in onsetDetectionTimes:
    # Sometimes the note at the onset is not the actual note we are looking for, i+1 is to just check the next frequency,
    # which tends to be more accurate, maybe question mark?
    #
    # Alternatively we could check for the median frequency between two onsets, which may be more accurate 
    freq = freqs[i+1]
    if not np.isnan(freq):
        midiValue = np.round(librosa.hz_to_midi(freq))
        
        beat = voice.add_child(Beat(quarter_duration=1))
        beat.add_child(Chord(midiValue, 1))
           
xml_path = filePath.with_suffix('.xml')
score.export_xml(xml_path)

