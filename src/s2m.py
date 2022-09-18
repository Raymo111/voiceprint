from email.mime import audio
import os
from pydub import AudioSegment

""" This script converts any stereo audio to mono in the audio folder """
HOME = os.environ.get("HOME")
BASEPATH = os.path.dirname(__file__)

audio_path = os.path.join(BASEPATH, '../audio')
for file in os.listdir(audio_path):
    path = os.path.join(audio_path, file)
    sound = AudioSegment.from_wav(path)
    sound = sound.set_channels(1)
    sound.export(path, format="wav")

