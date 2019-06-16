import os
import shutil

import utils_pro as utils
from g2p_en import G2p
import hparams_pro as hp

g2p = G2p()


def pronunciation(str_word_or_sen):
    return_list = list()
    is_word = True

    p_list = g2p(str_word_or_sen)
    if " " in p_list:
        is_word = False

    if not os.path.exists(hp.tts_results_path):
        os.mkdir(hp.tts_results_path)

    wav_file_name = str_word_or_sen + ".wav"
    tts_out = utils.tts(str_word_or_sen, os.path.join(
        hp.tts_results_path, wav_file_name))
    if tts_out[0]:
        return_list.append(os.path.abspath(
            os.path.join(hp.tts_results_path, wav_file_name)))
    else:
        print(tts_out[1])
        return

    if not is_word:
        return_list.append(None)
        return_list.append(None)
        return return_list
    else:
        return_list.append(p_list)

        if not os.path.exists("temp"):
            os.mkdir("temp")
        with open(os.path.join("temp", str_word_or_sen + ".lab"), "w") as f:
            for p in p_list:
                f.write(p)
        shutil.copy(os.path.join(hp.tts_results_path, wav_file_name), "temp")

        with open(hp.words_file_name, "w") as f:
            for p in p_list:
                f.write(p)
            f.write("   ")
            for p in p_list:
                f.write(p + " ")

        if not os.path.exists(hp.align_results_folder):
            os.mkdir(hp.align_results_folder)
        utils.align_wavs("temp", hp.words_file_name, hp.align_results_folder)
        shutil.rmtree("temp")

        if not os.path.exists(hp.cut_results_folder):
            os.mkdir(hp.cut_results_folder)

        if not os.path.exists(os.path.join(hp.cut_results_folder, str_word_or_sen)):
            os.mkdir(os.path.join(hp.cut_results_folder, str_word_or_sen))
            utils.cut_wav(os.path.join(hp.tts_results_path, wav_file_name),
                          os.path.join(hp.align_results_folder,
                                       str_word_or_sen + ".TextGrid"),
                          os.path.join(hp.cut_results_folder, str_word_or_sen))
            return_list.append(os.listdir(os.path.join(
                hp.cut_results_folder, str_word_or_sen)))
        else:
            return_list.append(utils.getAbsPath(os.path.abspath(
                os.path.join(hp.cut_results_folder, str_word_or_sen))))

        return return_list


if __name__ == "__main__":
    # Test
    pronunciation("Education")
