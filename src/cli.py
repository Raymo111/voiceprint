import argparse
import os
import sys
from typing import Optional
from voice_auth import voice_auth
from voice_auth import voice_record

THRESHOLD = -300
SECONDS = 4
BASEPATH = os.path.dirname(__file__)
NUM_SAMPLE = 6
phrase = 'The quick fox jumps nightly above the wizard'


def authenticate():
    f = open(os.path.join(BASEPATH, 'threshold.txt'), 'r')
    THRESHOLD = float(f.read())
    f.close()

    path = os.path.join(BASEPATH, '../audio/compare.wav')
    model, prob = voice_auth.compare(voice_record.record(path, SECONDS))
    print(model, prob)

    if prob and prob > THRESHOLD:
        print('True')
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

        paths_modelling = []
        for i in range(1, NUM_SAMPLE//2 + 1):
            print("Please say the phrase:", phrase)
            promp = input('Press enter to record... ')
            path = os.path.join(dest, username + str(i) + '.wav')
            voice_record.record(path, 5)
            paths_modelling.append(path)

        paths_training = []
        for i in range(3, int(NUM_SAMPLE) + 1):
            print("Please say the phrase:", phrase)
            promp = input('Press enter to record... ')
            path = os.path.join(dest, username + str(i) + '.wav')
            voice_record.record(path, 5)
            paths_training.append(path)

        voice_auth.build_model(username, paths_modelling)

        thresholds = []
        for path in paths_training:
            model, prob = voice_auth.compare(path)
            thresholds.append(prob)

        THRESHOLD = (sum(thresholds) / len(thresholds)) - 0.5
        print(THRESHOLD)

        f = open(os.path.join(BASEPATH, 'threshold.txt'), 'w')
        f.write(str(THRESHOLD))
        f.close()

    else:
        sys.exit(1 if authenticate() else 0)
