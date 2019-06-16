import librosa
import scipy
import numpy as np

import hparam_score as hp


def load_wav(path):
    return librosa.core.load(path, sr=hp.sample_rate)[0]


def melspectrogram(y):
    D = _stft(preemphasis(y))
    S = _amp_to_db(_linear_to_mel(np.abs(D))) - hp.ref_level_db

    return _normalize(S)


def _stft(y):
    n_fft, hop_length, win_length = _stft_parameters()
    return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)


def _stft_parameters():
    n_fft = (hp.num_freq - 1) * 2
    hop_length = int(hp.frame_shift_ms / 1000 * hp.sample_rate)
    win_length = int(hp.frame_length_ms / 1000 * hp.sample_rate)
    return n_fft, hop_length, win_length


def preemphasis(x):
    return scipy.signal.lfilter([1, -hp.preemphasis], [1], x)


def _amp_to_db(x):
    return 20 * np.log10(np.maximum(1e-5, x))


def _linear_to_mel(spectrogram):
    _mel_basis = _build_mel_basis()
    return np.dot(_mel_basis, spectrogram)


def _build_mel_basis():
    n_fft = (hp.num_freq - 1) * 2
    return librosa.filters.mel(hp.sample_rate, n_fft, n_mels=hp.num_mels)


def _normalize(S):
    return np.clip((S - hp.min_level_db) / -hp.min_level_db, 0, 1)


def _db_to_amp(x):
    return np.power(10.0, x * 0.05)


def find_endpoint(wav, threshold_db=-40, min_silence_sec=0.8):
    window_length = int(hp.sample_rate * min_silence_sec)
    hop_length = int(window_length / 4)
    threshold = _db_to_amp(threshold_db)
    for x in range(hop_length, len(wav) - window_length, hop_length):
        if np.max(wav[x:x+window_length]) < threshold:
            return x + hop_length
    return len(wav)
