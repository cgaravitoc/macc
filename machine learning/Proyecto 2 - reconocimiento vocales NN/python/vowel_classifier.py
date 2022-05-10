CURRENT_PATH = os.getcwd()
SAMPLES_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'database')
CSV_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'csv')
MODELS_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'models')
NEWSAMPLES_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'new_samples')
PYTHON_PATH = os.path.join(CURRENT_PATH, os.path.pardir, 'python')

import librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import pathlib
import csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import keras
from keras import layers
from keras import layers
import keras
from keras.models import Sequential
import h5py
from keras.models import model_from_json
import os 
import glob
import librosa
import soundfile 
import csv

import sys
sys.path.insert(1, PYTHON_PATH)

import transform2wav as t2wav
import vowel_classifier as vc

import warnings
warnings.filterwarnings('ignore')


class my_vowelClassifier:

    def __init__(self, CSV_PATH, NEWSAMPLES_PATH, MODELS_PATH):
        '''
        Crea la instancia para la red neuronal

        Parámetros
        ----------
        CSV_PATH: ruta de trabajo para guardar archivos csv
        NEWSAMPLES_PATH: ruta de trabajo para leer las muestras de audio
        '''
        self.CSV_PATH = CSV_PATH
        self.NEWSAMPLES_PATH = NEWSAMPLES_PATH
        self.MODELS_PATH = MODELS_PATH

        # load json and create model
        json_file = open(os.path.join(MODELS_PATH, 'model.json'), 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        # load weights into new model
        loaded_model.load_weights(os.path.join(MODELS_PATH, "model.h5"))
        print("Loaded model from disk")

    def csv_creator(self, dataset_NEW):
        '''
        Crea el archivo csv con los datos de entrada para la red nueronal

        Parámetros
        ----------
        dataset_NEW: nombre del archivo
        '''

        header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'

        for i in range(1, 20): # origianlly is (1,21)
            header += f' mfcc{i}'

        header += ' label'
        header = header.split()

        file = open(os.path.join(self.CSV_PATH, f'{dataset_NEW}.csv'), 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(header)

        for filename in os.listdir(os.path.join(self.NEWSAMPLES_PATH)):
            sample = os.path.join(self.NEWSAMPLES_PATH, filename) 
            if filename == 'desktop.ini': # omite desktop.ini
                break
            y, sr = librosa.load(sample, mono=True, duration=30)

            rms = librosa.feature.rms(y=y) # The latest librosa replaced rmse with rms, 
            spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
            rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y)
            mfcc = librosa.feature.mfcc(y=y, sr=sr)
            
            to_append = f'{filename} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'    
            
            for e in mfcc:
                to_append += f' {np.mean(e)}'
            
            to_append += f' {filename}'
            file = open(os.path.join(self.CSV_PATH, f'{dataset_NEW}.csv'), 'a', newline='')
            
            with file:
                writer = csv.writer(file)
                writer.writerow(to_append.split())
        return self
    
    def read_myData(self):
        '''
        Lee el archivo csv. 

        Parámetros
        ----------

        Returns
        -------
        X_new: datafrane de datos acondicionados del csv para la entrada de la red neuronal
        new_data: datafrane de datos del csv
        '''
        scaler = StandardScaler()
        new_data = pd.read_csv(os.path.join(self.CSV_PATH, 'dataset_NEW.csv'))
        new_data = new_data.drop(['filename'],axis=1)
        X_new = scaler.fit_transform(np.array(new_data.iloc[:, :-1], dtype = float))

        return X_new, new_data

    def my_prediction(self, loaded_model, X_new, new_data): 
        '''
        Hace la clasificación del sonido. 

        Parámetros
        ----------
        loaded_model: 
        X_new: 
        encoder: 
        new_data: 

        Returns
        -------
        prediction: Dataframe que compara el nombre de la muestra con la clasificación realizada por la red.

        '''
        y_encoder = np.load(os.path.join(MODELS_PATH, 'y_encoder.npy'))

        new_sample = new_data.iloc[:, -1]

        predict_xnew = loaded_model.predict(X_new) 
        classes_xnew = np.argmax(predict_xnew,axis=1)

        pred_str = y_encoder.inverse_transform(classes_xnew)
        prediction = pd.DataFrame(zip(new_sample, pred_str), columns=["new_sample", "prediction"])

        return prediction