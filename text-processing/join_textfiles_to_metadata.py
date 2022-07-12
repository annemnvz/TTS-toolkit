import os

def read_text_file(file_path):
    os.chdir(file_path)
    metadata_list = []
    for file in os.listdir():
        if file.endswith(".txt"):
            fn = os.path.basename(file)
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    metadata_list.append(line)
                    newline = fn.replace(".txt", "") + "|" + line
                    nline = newline.replace("| ","|")
                    with open("metadata.txt", "a+") as fo:
                        fo.writelines(nline)




file_path=""
read_text_file(file_path=file_path)