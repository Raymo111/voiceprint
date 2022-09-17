import os
from pydub import AudioSegment


for file in os.listdir('/home/kevincheng/Documents/voiceprint-htn/audio'):
    path = os.path.join('/home/kevincheng/Documents/voiceprint-htn/audio', file)
    sound = AudioSegment.from_wav(path)
    sound = sound.set_channels(1)
    sound.export(path, format="wav")

