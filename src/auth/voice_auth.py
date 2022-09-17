import os
import logging
import pickle
import numpy as np
import sklearn
import python_speech_features as features
import scipy.io.wavfile as wav
import sklearn.mixture
import noisereduce
from pydub import AudioSegment

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


def test_noise_reduction(path, path2):
    print(path)
    rate, data = wav.read(path)
    # convert stereo to mono if applicable

    if len(data.shape) > 1:
        sound = AudioSegment.from_wav(path)
        sound = sound.set_channels(1)
        sound.export(path, format="wav")

    rate, mono_data = wav.read(path)

    reduced_noise_data = noisereduce.reduce_noise(y=mono_data, sr=rate, n_fft=2048)
    wav.write(path2, rate, reduced_noise_data)


def voice_features(rate, data):
    """ Extracts MFCC features from the given WAV data, also reduces noise
    Parameters:
    rate: int               - sampling rate of WAV file
    data: numpy array       - data from WAV file

    audiodata[[left right]
              [left right]
               ...
              [left right]]

    """
    # convert stereo to mono if applicable
    if len(data.shape) > 1:
        raise ValueError("WAV file is not mono!")

    reduced_noise = noisereduce.reduce_noise(y=data, sr=rate, n_fft=2048)
    mfccs = features.mfcc(reduced_noise, rate, nfft=2048)  # using default parameters except fft size
    mfccs = sklearn.preprocessing.scale(mfccs)
    delta_mfccs = features.delta(mfccs, 2)
    return np.hstack((mfccs, delta_mfccs))


# TODO: improve the scaling and accuracy of the model -> wordlists? better word distribition? bg noise filtering?
def build_model(name, paths):
    """ Builds Gaussian Mixture Model from features of each WAV file in paths collection
    Parameters:
    name: str               - name of model (id)
    paths: list[str]        - list of paths of WAV files. WAV files MUST BE MONO NOT STERO
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

    if combined_features.size != 0:
        logging.debug(f"# samples: {len(paths)}")
        gmm = sklearn.mixture.GaussianMixture(
            n_components=len(paths), max_iter=200, covariance_type='diag', n_init=3)
        gmm.fit(features)
        pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
        return True
    else:
        logging.warning(" NO FEATURES")
        return False


def compare(path, threshold, models_src):
    """ Compares audio features against all models to find closest match above given threshold
    Parameters:
    paths: str              - path of WAV file to compare
    threshold: num          - threshold for match, negative log likelihood
    """

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
    if best_probabilty > threshold:
        return best_model, best_probabilty
    else:
        return None, None



