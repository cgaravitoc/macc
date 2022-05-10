#
# Reemplaza formatos de audio .ogg (whatsapp) y .m4a (grabadora win10) a formato .wav
# 

import os 
import glob
import librosa
import soundfile 

import warnings
warnings.filterwarnings("ignore")



def transform2wav():
  CURRENT_PATH = os.getcwd()
  NEWSAMPLES_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'new_samples')
  
  for format in ['ogg', 'm4a']:
    path = os.path.join(NEWSAMPLES_PATH, f'*.{format}')
    files = glob.glob(path)
    i = 1
    print(files)
    for file in files:
        print(file)
        print("in for cycle for change format")
        audio, sr = librosa.load(str(file), sr = 16000)
        soundfile.write(os.path.join(NEWSAMPLES_PATH, f'sample_{i}.wav'), audio ,16000)
        i+=1            

        if os.path.exists(file):
            print(f"file {file} deleted!")
            os.remove(file)                     