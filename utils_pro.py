import os
import utils_pro
import parse_TextGrid
import librosa
import numpy as np
from aip import AipSpeech
import hparams_pro as hp


def tts(seq, path):
    APP_ID = '14566918'
    API_KEY = 'dOPdsdFMewG4HA5WUOGj9YYD'
    SECRET_KEY = 'aiFHxHtG5d3BmIeI4kckTWTWBHYRo3yZ'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result = client.synthesis(seq, 'zh', 1, {'vol': 5, "per": 1, 'aue': 6})

    if not isinstance(result, dict):
        with open(path, 'wb') as f:
            f.write(result)
        return [True, None]
    else:
        return [False, result['err_msg']]


def align_wavs(corpus_foldername, dict_filename, output_foldername):
    if not os.path.exists(output_foldername):
        os.mkdir(output_foldername)

    aligner_path = os.path.abspath(hp.aligner_path)
    corpus_foldername = os.path.abspath(corpus_foldername)
    dict_filename = os.path.abspath(dict_filename)
    pretrain_model = os.path.abspath(hp.pretrain_model)
    output_foldername = os.path.abspath(output_foldername)
    command = aligner_path + " " + corpus_foldername + " " + \
        dict_filename + " " + pretrain_model + " " + output_foldername

    # command = hp.aligner_path + " " + corpus_foldername + " " + \
    #     dict_filename + " " + hp.pretrain_model + " " + output_foldername

    logger = os.popen(command)
    print(logger.read())


def cut_wav(wav_filename, textgrid_filename, output_folder):

    def cut_wav_save(wav, sr, start_time, end_time, save_filename):

        def cut(wav, sr, start_time, end_time):
            start_item = int(start_time * sr)
            end_item = int(end_time * sr)
            wav_cut = wav[start_item:end_item]
            return wav_cut

        wav_cut = cut(wav, sr, start_time, end_time)
        librosa.output.write_wav(save_filename, wav_cut, sr)

    wav, sr = librosa.load(wav_filename)
    cut_info_dict = parse_TextGrid.parse_textgrid(textgrid_filename)

    cnt = 0
    for _, cut_info in enumerate(cut_info_dict):
        if cut_info != "None":
            filename = str(cnt) + "_" + cut_info + ".wav"
            fn = os.path.join(output_folder, filename)
            cut_wav_save(wav, sr,
                         cut_info_dict[cut_info][0],
                         cut_info_dict[cut_info][1], fn)
            cnt = cnt + 1


def getAbsPath(file_list):
    out = list()
    for file_name in os.listdir(file_list):
        out.append(os.path.join(file_list, file_name))
    return out
