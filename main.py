import librosa
import matplotlib.pyplot as plt
import numpy as np
import time

audio_file_path = "bach-prelude-c-major-156935.mp3"
# audio_file_path = "Reference Scales_On C.mp3"

print("Loading file: %s" % audio_file_path)
loadStartTime = time.time()
audio, samplerate = librosa.load(audio_file_path)
loadEndTime = time.time()
loadTime = loadEndTime - loadStartTime
print("File loaded in %.2f seconds" % loadTime)

print("Detecting tempo")
tempo = librosa.feature.tempo(y=audio, sr=samplerate)
print("Tempo = %d" % tempo[0])

print("Detecting frequencies")
freqStartTime = time.time()
freqs, voiced_flag, voiced_probs = librosa.pyin(
    y=audio, 
    fmin=librosa.note_to_hz('C2'),
    fmax=librosa.note_to_hz('C7'),
    sr=samplerate)
freqEndTime = time.time()
freqTime = freqEndTime - freqStartTime
print("Frequency detection done in %.2f seconds" % freqTime)

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
quarterNoteInSeconds = 60 / tempo
timesSampleRate = int(np.round(quarterNoteInSeconds / times[1]))
print("timesSampleRate: %d" % timesSampleRate)
for i in freqs[0::timesSampleRate]:
    if not np.isnan(i):
        notes.append(librosa.hz_to_note(i))
    
print(notes)