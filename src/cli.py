import argparse
import os
import sys
from typing import Optional
from voice_auth import voice_auth
from voice_auth import voice_record

THRESHOLD = -17.0
SECONDS = 5
BASEPATH = os.path.dirname(__file__)
NUM_SAMPLE = 5
phrase = 'The quick fox jumps nightly above the wizard'


def authenticate():
    path = os.path.join(BASEPATH, '../audio/compare.wav')
    model, prob = voice_auth.compare(voice_record.record(path, SECONDS))
    print(model, prob)

    # if model != os.environ.get('USER'):
    #     return False
    if prob and prob > THRESHOLD:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--auth', action='store_true', required=False)
    args = parser.parse_args()
    if not args.auth:
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
    else:
        sys.exit(1 if authenticate() else 0)
