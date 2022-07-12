#!/bin/bash

# select begin and end stages
# depending on what's needed
stage=0
stop_stage=7

# -- Paths --
# copy files into this folder 
# or save modified ones into another
path=""
outpath=""
outfile="${outpath}/texts_all.txt"

# -- Transcription and dictionary related --
# This part should be substituted by eSpeak for transcriptions and MFA for dictionary creation (as my suggestions, could be any other)
MODULE=""
TEXT_MODE=""
DICT=""
LANG="es"

# --

if [ $stage -le 0 ] && [ ${stop_stage} -ge 0 ]; then
    # loop to convert multiple files 
    echo "Stage 0: Converting files from ${FROM_ENCODING} to ${TO_ENCODING} encoding..."

    #!/bin/bash
    #enter input encoding here
    FROM_ENCODING="iso-8859-1"
    #output encoding(UTF-8)
    TO_ENCODING="UTF-8"
    CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"

    for  file  in  *.txt; do
        $CONVERT   "$file"   -o  "${file%.txt}"
    done
    exit 1
fi

if [ $stage -le 1 ] && [ ${stop_stage} -ge 1 ]; then
    # join text files in one
    echo "Stage 1: Joining all text files in ${path} into ${outfile}..."

    for  file  in  $path/*.txt; do
        cat "$file" >> $outfile || exit 1;
    done
fi

if [ $stage -le 2 ] && [ ${stop_stage} -ge 2 ]; then
    # clean clean clean
    echo "Stage 2: Cleaning the text in ${outfile}..."

    # pasar a ISO antes de modulos

    CLEAN_CHARS="${MODULE}  -TxtMode=${TEXT_MODE} -HDicDB=${DICT} -Lang=${LANG}"

    # echo "cat "$outfile" | iconv -f UTF-8 -t ISO—8859-15 -c |$CLEAN_CHARS > "${outpath}/temp_clean.txt""
    cat "$outfile" | iconv -f UTF-8 -t ISO—8859-15 -c |$CLEAN_CHARS > "${outpath}/temp_clean.txt"

    # input encoding
    FROM_ENCODING="ISO-8859-15"
    # output encoding
    TO_ENCODING="UTF-8"
    CONVERT=" iconv  -f   $FROM_ENCODING  -t   $TO_ENCODING"
    TEMP_UTF_FILE="${outpath}/temp_clean-utf8.txt"
    echo "$CONVERT ${outpath}/temp_clean.txt > $TEMP_UTF_FILE"
    $CONVERT "${outpath}/temp_clean.txt" > $TEMP_UTF_FILE

    sed 's/\./ /g' -i $TEMP_UTF_FILE
    sed 's/,/ /g' –i $TEMP_UTF_FILE
    sed 's/¡/ /g' –i $TEMP_UTF_FILE
    sed 's/!/ /g' –i $TEMP_UTF_FILE
    sed 's/¿/ /g' –i $TEMP_UTF_FILE
    sed 's/?/ /g' –i $TEMP_UTF_FILE
    sed 's/;/ /g' –i $TEMP_UTF_FILE
    sed 's/:/ /g' –i $TEMP_UTF_FILE
    sed 's/(/ /g' –i $TEMP_UTF_FILE
    sed 's/)/ /g' –i $TEMP_UTF_FILE
    sed 's/”/ /g' -i $TEMP_UTF_FILE
    sed "s/'/ /g" -i $TEMP_UTF_FILE 
    # exit 1
    # mv "temp_clean_utf8.txt" "${path}/clean/temp_clean_utf8.txt"
fi

if [ $stage -le 3 ] && [ ${stop_stage} -ge 3 ]; then
    # getting unique line wordlist
    echo "Stage 3: Getting unique wordlist..."

    WORDLIST="${outpath}/word_list.txt"
    tr ' ' '\n' < "${outpath}/temp_clean-utf8.txt" | sort | uniq > "${outpath}/temp_list.txt"
    sed -i '/^$/d' "${outpath}/temp_list.txt"
    sed 's/$/\./' "${outpath}/temp_list.txt" > $WORDLIST || exit 1;
fi

if [ $stage -le 4 ] && [ ${stop_stage} -ge 4 ]; then
    # transcribe words
    # replace with Phonemizer, for instance
    echo "Stage 4: Transcribing wordlist..."

    TRANSCRIBED="${outpath}/transcribed_list.txt"
    cat "${outpath}/word_list.txt" | iconv -f UTF-8 -t ISO—8859-15 | $MODULE -Lang=$LANG -HDicDB=$DICT | iconv -f ISO8859-15 -t UTF-8 > $TRANSCRIBED
    sed 's/-//g' -i $TRANSCRIBED
    # FOLLOWING COMMAND MIGHT BE NEEDED FOR MFA
    # sed "s/'//g" $TRANSCRIBED  || exit 1;
fi

if [ $stage -le 5 ] && [ ${stop_stage} -ge 5 ]; then
    # Create dictionary
    # This step can be performed with MFA train: 
    # https://montreal-forced-aligner.readthedocs.io/en/latest/user_guide/workflows/train_acoustic_model.html
    echo "Stage 5: Creating dictionary file..."

    DICT_FILE="${outpath}/mydict.dict"
    paste "${outpath}/word_list.txt" "${outpath}/transcribed_list.txt" > ${DICT_FILE}
    # iconv -f ISO8859-15 -t UTF-8 ${DICT_FILE} > "${outpath}/myfile_utf8.dict" || exit 1;
fi

if [ $stage -le 6 ] && [ ${stop_stage} -ge 6 ]; then
    # clean (again)
    echo "Stage 6: Cleaning txt files in ${outpath} directory..."

    #one file
    DICT_FILE="${outpath}/mydict.dict"
    sed 's/\./ /g' -i $DICT_FILE
    sed 's/,/ /g' –i $DICT_FILE
    sed 's/¡/ /g' –i $DICT_FILE
    sed 's/!/ /g' –i $DICT_FILE
    sed 's/¿/ /g' –i $DICT_FILE
    sed 's/?/ /g' –i $DICT_FILE
    sed 's/;/ /g' –i $DICT_FILE
    sed 's/:/ /g' –i $DICT_FILE
    sed 's/(/ /g' –i $DICT_FILE
    sed 's/)/ /g' –i $DICT_FILE
    sed 's/”/ /g' -i $DICT_FILE
    sed 's/"/ /g' -i $DICT_FILE
    # sed "s/'/ /g" -i $DICT_FILE 
    sed 's/\s\s*/ /g' -i $DICT_FILE;
    sed 's/\n\n*/ /g' -i $DICT_FILE;

    # multiple files
    # for i in $outpath/*.txt ; do 
    #     sed 's/\./ /g' -i $i;
    #     sed 's/,/ /g' -i $i;
    #     sed 's/¡/ /g' -i $i;
    #     sed 's/!/ /g' -i $i;
    #     sed 's/¿/ /g' -i $i;
    #     sed 's/?/ /g' -i $i;
    #     sed 's/;/ /g' -i $i;
    #     sed 's/:/ /g' -i $i;
    #     sed 's/(/ /g' -i $i;
    #     sed 's/)/ /g' -i $i;
    #     sed 's/"/ /g' -i $i;
    #     sed "s/'/ /g" -i $i;
    #     sed 's/\s\s*/ /g' -i $i;
    #     sed 's/\n\n*/ /g' -i $i;
    #     done
    #     exit 1
 fi
