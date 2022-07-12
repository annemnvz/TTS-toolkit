import os

  
def read_text_file(file_path):
    os.chdir(text_path)
    metadata_list = []
    for file in os.listdir():
        if file.endswith(".txt"):
            with open(file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    metadata_list.append(line)
    return metadata_list

def split_sentences(metadata):
    sentence_dict = {}
    for line in metadata:
        parts = line.split("	", 1)
        ids = parts[0].replace("XX", "72")
        #sorry some spaghetti code here
        if "." in parts[1]:
            sentences = parts[1].replace(".", "^ .").split(" .")
            sentence_dict[ids] = sentences
        if "?" in parts[1]:
            sentences = parts[1].replace("?", "* ?").split(" ?")
            sentence_dict[ids] = sentences
        if "!" in parts[1]:
            sentences = parts[1].replace("!", "~ !").split(" !")
            sentence_dict[ids] = sentences
    

    for text_id, text in sentence_dict.items():
        count = 0
        if "\n" in text:
            text.remove("\n")
        if "" in text:
            text.remove("")
        for s in text:
            # sorry for the spaghetti
            # s = s.replace(" ^", ".")
            # s = s.replace(" *", "?") 
            # s = s.replace(" ~", "!")
            # s = s.replace("^", ".")
            # s = s.replace("*", "?") 
            # s = s.replace("~", "!")
            count += 1
            save_first_file = f"{text_id}.txt"
            save_file = f"{text_id}_{count}.txt"
            #save the first with the original name
            if count == 1:
                line = f"{text_id}" + "|" + s + "\n"
                with open(f"text_splitting_test/{save_first_file}", "a+") as fo:
                    fo.writelines(line)
            #save adding underscore number for following ones(starts at 2)
            else:
                line = f"{text_id}" + "|" + s + "\n"
                with open(f"text_splitting_test/{save_file}", "a+") as fo:
                    fo.writelines(line)