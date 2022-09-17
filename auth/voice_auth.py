from distutils.log import debug
import os
import logging
import wave
import time
import pickle
import numpy as np
import librosa
import librosa.display
import sklearn
import python_speech_features as features
import scipy.io.wavfile as wav
import sklearn.mixture

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def voice_features(rate, data):
    """ Extracts MFCC features from the given WAV data
    Parameters:
    rate: int               - sampling rate of WAV file
    data: numpy array       - data from WAV file
    """

    # mfccs = librosa.feature.mfcc(y=data, sr=rate)
    # print(mfccs.shape)
    # print(mfccs)
    # librosa.display.specshow(mfccs, sr=rate, x_axis='time')

    # mfccs = features.mfcc(data, rate, 0.025, 0.01, 20, nfft=1200, appendEnergy=True)
    mfccs = features.mfcc(data, rate, nfft=1200)  # using default parameters except fft size
    mfccs = sklearn.preprocessing.scale(mfccs)
    delta_mfccs = features.delta(mfccs, 2)
    return np.hstack((mfccs, delta_mfccs))

def build_model(name, paths):
    """ Builds Gaussian Mixture Model from features of each WAV file in paths collection
    Parameters:
    name: str               - name of collection
    paths: list[str]        - list of paths of WAV files
    """
    dest = '/home/kevincheng/Documents/voiceprint-htn/audio_models/'
    combined_features = np.asarray([])

    for path in paths:
        sampling_rate, data = wav.read(path)
        features = voice_features(sampling_rate, data)
        if combined_features.size == 0:
            combined_features = features
        else:
            combined_features = np.vstack([combined_features, features])
        logging.debug(f"Combined feature size: {combined_features.size}")

    if combined_features.size != 0:
        logging.debug(f"n components: {len(paths)}")
        gmm = sklearn.mixture.GaussianMixture(
            n_components=len(paths), max_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)
        pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
        return True
    else:
        logging.warning(" NO FEATURES")
        return False


def compare(path):
    """ Compares audio features against all GMMs to find closest match
    Parameters:
    paths: str              - path of WAV file to compare
    """
    models_src = '/home/kevincheng/Documents/voiceprint-htn/audio_models/'
    model_paths = [os.path.join(models_src, fname) for fname in
        os.listdir(models_src) if fname.endswith('.gmm')]

    sampling_rate, data = wav.read(path)

    best_model = None
    best_probabilty = None
    debug_every_model = []
    for path in model_paths:
        model_name = path.split('/')[-1].split('.')[0]
        model = pickle.load(open(path, 'rb'))
        features = voice_features(sampling_rate, data)
        ll = np.array(model.score(features)).sum()

        if best_model is None:
            best_model = model_name
        if best_probabilty is None:
            best_probabilty = ll
        elif ll > best_probabilty:
            best_model = model_name
            best_probabilty = ll
        debug_every_model.append((model_name, ll))

    logging.debug(debug_every_model)
    return best_model, best_probabilty



