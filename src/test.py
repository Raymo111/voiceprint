import os
import itertools
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from scipy import linalg
from tqdm import tqdm
from voice_auth import voice_auth
from pydub import AudioSegment

from voice_auth.voice_record import voice_record

HOME = os.environ.get("HOME")
color_iter = itertools.cycle(["navy", "c", "cornflowerblue", "gold", "darkorange"])

def train():
    kevin = [
        f'{HOME}/Documents/voiceprint-htn/audio/kevin1.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/kevin2.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/kevin3.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/kevin4.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/kevin5.wav'
    ]

    thomas = [
        f'{HOME}/Documents/voiceprint-htn/audio/thomas1.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/thomas2.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/thomas3.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/thomas4.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/thomas5.wav'
    ]
    raymond = [
        # f'{HOME}/Documents/voiceprint-htn/audio/raymond1.wav',
        # f'{HOME}/Documents/voiceprint-htn/audio/raymond2.wav',
        # f'{HOME}/Documents/voiceprint-htn/audio/raymond3.wav',
        # f'{HOME}/Documents/voiceprint-htn/audio/raymond4.wav',
        # f'{HOME}/Documents/voiceprint-htn/audio/raymond5.wav'
        f'{HOME}/Documents/voiceprint-htn/audio/raymond6.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond7.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond8.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond9.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond10.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond11.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/raymond12.wav'
    ]

    success = voice_auth.build_model("kevin", kevin)
    # success = voice_auth.build_model("thomas", thomas)
    # success = voice_auth.build_model("raymond", raymond)

    # lst = []
    # for path in kevin:
    #     model, prob = voice_auth.compare(path)
    #     lst.append((model, prob))

    # print(lst)


# # 102 correct out of 104 (52 male, 52 female), -18.98 avg
# def test2():
#     voices_male_src = f'{HOME}/Documents/sample_voice_data/males'
#     voices_female_src = f'{HOME}/Documents/sample_voice_data/females'

#     for voice in os.listdir(voices_male_src):
#         path = os.path.join(voices_male_src, voice)
#         success = voice_auth.build_model(voice, [path])

#     for voice in os.listdir(voices_female_src):
#         path = os.path.join(voices_female_src, voice)
#         success = voice_auth.build_model(voice, [path])

#     lst = []
#     voices_male_src = f'{HOME}/Documents/sample_voice_data/males'
#     voices_female_src = f'{HOME}/Documents/sample_voice_data/females'

#     for voice in tqdm(os.listdir(voices_male_src)):
#         path = os.path.join(voices_male_src, voice)
#         model, prob = voice_auth.compare(path, THRESHOLD, f'{HOME}/Documents/voiceprint-htn/audio_models_celeb/')
#         lst.append((model == voice.split('.wav')[0], prob))


#     for voice in tqdm(os.listdir(voices_female_src)):
#         path = os.path.join(voices_female_src, voice)
#         model, prob = voice_auth.compare(path, THRESHOLD, f'{HOME}/Documents/voiceprint-htn/audio_models_celeb/')
#         lst.append((model == voice.split('.wav')[0], prob))

#     print(len([1 for t, n in lst if t == True]))



def plot_results(X, Y_, means, covariances, index, title):
    print("*********")
    splot = plt.subplot(2, 1, 1 + index)
    for i, (mean, covar, color) in enumerate(zip(means, covariances, color_iter)):
        v, w = linalg.eigh(covar)
        v = 2.0 * np.sqrt(2.0) * np.sqrt(v)
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        if not np.any(Y_ == i):
            continue
        print(Y_)
        print(Y_==i)
        plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], 0.8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180.0 * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180.0 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)

    plt.xlim(-9.0, 5.0)
    plt.ylim(-3.0, 6.0)
    plt.xticks(())
    plt.yticks(())
    plt.title(title)
    plt.show()


def test3():
    import scipy.io.wavfile as wav
    import sklearn.mixture
    # path = f'{HOME}/Documents/voiceprint-htn/audio/record2.wav'
    # sampling_rate, data = wav.read(path)

    # features = voice_auth.voice_features(sampling_rate, data)
    # print(features)

    # Number of samples per component
    n_samples = 500

    # Generate random sample, two components
    np.random.seed(0)
    C = np.array([[0.0, -0.1], [1.7, 0.4]])
    X = np.r_[
        np.dot(np.random.randn(n_samples, 2), C),
        0.7 * np.random.randn(n_samples, 2) + np.array([-6, 3]),
        1.2 * np.random.randn(n_samples, 2) + np.array([-1, 2]),
        0.3 * np.random.randn(n_samples, 2) + np.array([-3, 4]),
        -0.1 * np.random.randn(n_samples, 2) + np.array([2, 2]),
    ]
    print(X)
    return
    # Fit a Gaussian mixture with EM using five components
    gmm = sklearn.mixture.GaussianMixture(n_components=10, covariance_type="full").fit(X)


    plot_results(X, gmm.predict(X), gmm.means_, gmm.covariances_, 0, "Gaussian Mixture")
    x_ = gmm.sample(n_samples=10)[0]
    y_ = gmm.predict(x_)
    print(x_)
    print(y_)

def test_noise_reduction():
    voice_auth.test_noise_reduction(f'{HOME}/Documents/voiceprint-htn/audio/rtest2.wav',
        f'{HOME}/Documents/voiceprint-htn/audio/result2.wav')

def test4():
    ret = voice_auth.authenticate()
    print(ret)


if __name__ == '__main__':
    # train()
    test4()
    # print(os.path.dirname(__file__))
