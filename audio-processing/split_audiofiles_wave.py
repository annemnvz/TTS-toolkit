import wave 
import os

# Wave library is recommended to split in seconds (with decimals)
def get_all_wavs(wav_path):
    #returns a list of wavs, e.g.:
    #  [...,'../elra/wavs_original/11/wav/T6B72110121.wav',...]

    folders = os.listdir(wav_path)
    wav_list = []
    for folder in folders:
        path = f"{wav_path}/{folder}/wav"
        folders_all = os.listdir(path)
        for i in folders_all:
            all_wavs = path + "/" + i
            wav_list.append(all_wavs)
    return wav_list

def get_parts_durations(transcriptions_path):
    # returns start and end durations of utterances 
    # specific to my duration filelist (can be sub by MFA duration timestapms)
    folders = os.listdir(transcriptions_path)
    lbo_parts_durations = {}
    for folder in folders:
        path = f"{transcriptions_path}/{folder}"
        folders_all = os.listdir(path)
        for file in folders_all:
            if file.endswith(".esS"):
                transcription_file = f"{path}/{file}"
                with open(transcription_file, 'r') as f:
                    fn = os.path.basename(f.name).replace(".esS", "")
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("LBO"):
                            lbo_parts = line.split(",",3)
                            part_start = lbo_parts[0].replace("LBO: ", "")
                            part_end = lbo_parts[2]
                            if fn in lbo_parts_durations:
                                lbo_parts_durations[fn].append([part_start, part_end])
                            else:
                                lbo_parts_durations[fn] = [[part_start, part_end]]
    return lbo_parts_durations


def get_audio_info(audio_file):
    # returns audio file information
    # number of channels and frames, and sample width and rate
    with wave.open(audio_file, "rb") as infile:
        nchannels = infile.getnchannels()
        sampwidth = infile.getsampwidth()
        samplingrate = infile.getframerate()
        nframes = infile.getnframes()
        print(nframes, "nframes")
        audio = infile.readframes(nframes)
    return nchannels, sampwidth, samplingrate, audio


def split_audio(audio_file, start, end, save_file):
    # file to divide
    with wave.open(audio_file, "rb") as infile:
        nchannels, sampwidth, samplingrate, audio = get_audio_info(audio_file=audio_file)
                
        # set position in wave to start of segment
        infile.setpos(int(start * samplingrate))
        
        # extract data
        data = infile.readframes(int(end * samplingrate - start * samplingrate)+1)

        # write the extracted data to a new file
        with wave.open(save_file, 'w') as outfile:
            outfile.setnchannels(nchannels)
            outfile.setsampwidth(sampwidth)
            outfile.setframerate(samplingrate)
            outfile.setnframes(int(len(data) / sampwidth))
            outfile.writeframes(data)


# ---- paths (audio/SAM files)
transcriptions_path = " " # path with SAM file(s)
wav_path = " " #original wav to split path
wavs = os.listdir(wav_path)
save_path = " " #path to save splitted files

# ---- get SAM time stamps for utterances
durations_dict = get_parts_durations(transcriptions_path=transcriptions_path)

# ---- split single audio file in parts:
count = 0
for key in durations_dict.keys():
    wav = f"{key}.wav"
    if wav in wavs:
        durs = durations_dict[wav.replace(".wav","")]
        for dur in durs:
            count += 1
            start = float(dur[0])
            end = float(dur[1])
            audio_file = f"{wav_path}/{wav}"
            save_file = f"{save_path}/{key}_{count}.wav"
            if count == 1:
                split_audio(audio_file=audio_file, start=start, end=end, save_file=f"{save_path}/{wav}")
            else:
                split_audio(audio_file=audio_file, start=start, end=end, save_file=save_file)

# ---- split all audios in parts:
for key in durations_dict.keys():
    wav = f"{key}.wav"
    if wav in wavs:
        count = 0
        durs = durations_dict[wav.replace(".wav","")]
        for dur in durs:
            count += 1
            start = float(dur[0])
            end = float(dur[1])
            audio_file = f"{wav_path}/{wav}"
            save_first_file = f"{save_path}/{wav}" 
            save_file = f"{save_path}/{key}_{count}.wav"
           
            # if splitting fails, this code saves failed to split filenames in "failed_to_split.txt"
            while not is_done:
                try:
                    if count == 1:
                        print(count, audio_file)
                        split_audio(audio_file=audio_file, start=start, end=end, save_file=save_first_file)
                    else:
                        split_audio(audio_file=audio_file, start=start, end=end, save_file=save_file)
                    is_done = True
                except:
                    line = audio_file+"\n"
                    with open("failed_to_split.txt", "a+") as fo:
                        fo.writelines(line)
                    print (f"splitting fails for {audio_file}.")
                    break