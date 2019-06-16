import os
import numpy as np
import librosa
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import utils_score as utils
import hparam_score as hp


def judge(user_audio_path, standard_audio_path):
    user_wav = utils.load_wav(user_audio_path)
    user_wav = user_wav[0:utils.find_endpoint(user_wav)]
    standard_wav, sr = librosa.load(standard_audio_path, sr=hp.sample_rate)

    user_mfccs = librosa.feature.mfcc(y=user_wav, sr=hp.sample_rate, n_mfcc=24)
    standard_mfccs = librosa.feature.mfcc(y=standard_wav, sr=sr, n_mfcc=24)

    assert np.shape(user_mfccs)[0] == np.shape(standard_mfccs)[0]

    scores = np.array(list())
    for i in range(np.shape(user_mfccs)[0]):
        out = fastdtw(user_mfccs[i], standard_mfccs[i], dist=euclidean)
        scores = np.append(scores, out[0])

    zeros = np.zeros([24, np.shape(user_mfccs)[1]])
    scores_stan = np.array(list())
    for i in range(np.shape(user_mfccs)[0]):
        out = fastdtw(zeros[i], standard_mfccs[i], dist=euclidean)
        scores_stan = np.append(scores_stan, out[0])

    score = 1 - (scores.mean()-200) / scores_stan.mean()
    score = score * 100
    print(score)

    return score
