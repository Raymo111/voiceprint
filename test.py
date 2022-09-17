import librosa

from auth import voice_auth


if __name__ == '__main__':
    kevin = ['/home/kevincheng/Documents/voiceprint-htn/audio/record1.wav',
        '/home/kevincheng/Documents/voiceprint-htn/audio/record2.wav',
        '/home/kevincheng/Documents/voiceprint-htn/audio/record3.wav',
        '/home/kevincheng/Documents/voiceprint-htn/audio/record4.wav',
        '/home/kevincheng/Documents/voiceprint-htn/audio/record5.wav']
    thomas = ['/home/kevincheng/Documents/voiceprint-htn/audio/thomas1.wav',
        '/home/kevincheng/Documents/voiceprint-htn/audio/thomas2.wav',]

    success = voice_auth.build_model("kevin", kevin)
    success = voice_auth.build_model("thomas", thomas)

    model, prob = voice_auth.compare('/home/kevincheng/Documents/voiceprint-htn/audio/record4.wav')
    print(model, prob)