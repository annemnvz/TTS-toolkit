from pydub import AudioSegment
import math, os

# Pydub library is recommended to split in miliseconds
class SplitWavAudioMubin():
    def __init__(self, folder, filename, blr_path):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename
        self.blr_path = blr_path
        self.audio = AudioSegment.from_wav(self.filepath)
    
    def get_duration(self):
    # get audio durations
        return self.audio.duration_seconds

    def get_parts_durations(self, blr_path):
    # extract and return start and end timestamps from SAM file
        os.chdir(blr_path)
        lbo_parts_durations = {}
        for file in os.listdir():
            if file.endswith(".esS"):
                file_path = f"{self.blr_path}/{file}"
                with open(file_path, 'r') as f:
                    f.name
                    fn = os.path.basename(f.name)
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("LBO"):
                            lbo_parts = line.split(",",3)
                            part_start = lbo_parts[0].replace("LBO: ", "")
                            part_end = lbo_parts[2]
                            lbo_parts_durations[fn] = [part_start, part_end]
        return lbo_parts_durations

    def single_split(self, split_filename):
    # split only once 
        parts_durs = self.get_parts_durations(self.blr_path)
        for name, part in parts_durs.items():
            split_filename = name.replace(".esS", ".wav")
            t1 = int(float(part[0]) * 1000)
            t2 = int(float(part[1]) * 1000)
            split_audio = self.audio[t1:t2]
            split_audio.export(self.folder + '/' + split_filename, format="wav")
        
    def multiple_split(self):
    # split multiple times (apply the split once function in loop)
        parts_durs = self.get_parts_durations(self.blr_path)
        total_mins = math.ceil(self.get_duration() / 60)
        count = 0
        for i in range(0, len(parts_durs.values())):
            split_fn = str(i) + '_' + self.filename
            self.single_split(self.filename)
            print(str(i) + ' Done')
            count += 1
            if count == len(parts_durs.values()):
                print('All splited successfully')

folder = ' ' # folder with audios 
file = ' .wav' #single wav for testing
blr_path = " " #path with SAM files

split_wav = SplitWavAudioMubin(folder=folder, filename=file, blr_path=blr_path)
split_wav.multiple_split()    