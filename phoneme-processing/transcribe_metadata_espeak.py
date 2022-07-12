from phonemizer.backend import EspeakBackend
from phonemizer.punctuation import Punctuation
import numpy as np


def write_lines_into_newfiles(input_metadata_file):
    with open(input_metadata_file, "r") as fi:
        lines = fi.readlines()
        for line in lines:
            parts = line.split('\t')
            name_file = parts[0]
            new_line= name_file+parts[1]
            with (f"{name_file}.txt", "w") as fo:
                fo.writelines(new_line)

def get_ipa_from_phonemizer(lang, text):
    backend = EspeakBackend(lang,preserve_punctuation=True)
    text = Punctuation(';:"()-').remexiove(text)
    ipa = backend.phonemize(text)
    return ipa

def transcribe_metadata(input_metadata_file):
    with open(input_metadata_file, "r") as fi:
        lines = fi.readlines()
        transcribed_sentences = []
        # transcribed_sentences_pipe = []
        for line in lines:
            parts = line.split('\t')
            name_file = parts[0].replace("XX", "72")
            transcriptions = get_ipa_from_phonemizer(lang="es", text=[parts[1]])
            for transcription in transcriptions:
                array = list(transcription)
                print(array)
                np.save(f'main/{name_file}', array)

                # ---- uncomment following for ID|transcription format
                # sentence_format = name_file+"|",transcription
                # sentence = "".join(sentence_format)
                # transcribed_sentences_pipe.append(sentence)

                # ---- Regular write:
                # with open(f"main/metadata_transcribed.txt", "w") as fo:
                #     for sentence in transcribed_sentences:
                #         fo.writelines(str(sentence)+"\n")

def convert_str_to_numpy_array(string):
    n_arrays = numpy.fromstring(string, dtype=float)
    with open(f"main/metadata_array.txt", "w") as fo:
            for array in n_arrays:
                fo.writelines(str(array)+"\n")

input_metadata_file = ""

write_lines_into_newfiles(input_metadata_file=input_metadata_file)
transcribe_metadata(input_metadata_file=input_metadata_file)


