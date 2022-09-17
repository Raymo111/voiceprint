import os
from pydub import AudioSegment

HOME = os.environ.get("HOME")

for file in os.listdir(f'{HOME}/Documents/voiceprint-htn/audio'):
    path = os.path.join(f'{HOME}/Documents/voiceprint-htn/audio', file)
    sound = AudioSegment.from_wav(path)
    sound = sound.set_channels(1)
    sound.export(path, format="wav")

