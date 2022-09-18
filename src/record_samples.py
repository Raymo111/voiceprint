import os
from voice_auth import voice_record, voice_auth

BASEPATH = os.path.dirname(__file__)
NUM_SAMPLE = 5
phrase = 'The quick fox jumps nightly above the wizard'



if __name__ == '__main__':
    username = input('Please input your username: ')
    dest = os.path.join(BASEPATH, f'../audio')

    paths = []
    for i in range(1, NUM_SAMPLE + 1):
        print("Please say the phrase:", phrase)
        promp = input('Press enter to record... ')
        path = os.path.join(dest, username + str(i) + '.wav')
        voice_record.record(path, 5)
        paths.append(path)

    voice_auth.build_model(username, paths)
