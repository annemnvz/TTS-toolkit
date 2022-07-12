## TTS-toolkit
A minimalistic toolkit with recipes for the preprocessing and handling of audio and text data oriented to Text-to-Speech modeling. 

Note: I tried to make recipes generic but some parts are specific to my project - I will improve this by adapting them to open source tools.

## Comes with recipes for...
### Audio processing:
- Resample audio (SoX)
- PCM modification (by changing bit-depth in this case) (SoX)
- Audio split in miliseconds (Pydub)
- Audio split in seconds (Wave)

### Text processing:
- Change text encoding
- Text cleanup 
- Join text files in single metadata.txt
- Text split in punctuation marks 

### Phoneme processing
- Transcribe metadata phonetically (save as numpy or regular phonemes)

### Dictionary creation and implementation:
To be added.

## Getting started

Just clone this repo

```
git clone https://github.com/annemnvz/TTS-toolkit.git
cd TTS-toolkit
```

And run the recipe you need to use. 

Remember to modify paths and files or tools if needed.
