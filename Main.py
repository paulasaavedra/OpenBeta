# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 12:15:42 2021

@author: paula
"""

import os
folder_path = 'C:\\Users\\PaulaSaavedra\\PaulaGD\\IMAL\\PA_Interfaz\\OpenBCI_Python'

os.chdir(folder_path)

from pynput import keyboard as kb
from subject_data import subject_data
from experiment import experiment
from prepare import prepare
from raw_bids import raw_bids
from observations import observations
import json

import realtime
import threading
import time
import numpy as np
import csv


#%%
def main():
    
    information = subject_data()
   
    def siguiente_ronda(tecla):
        if tecla == kb.KeyCode.from_char('x'):
            return False
    escuchador = kb.Listener(siguiente_ronda)
    
    rondas = int(information[0]['Rondas']) 
    observations = []
    
    for ronda in range(1,rondas+1):
        
        print('Presione x para comenzar con la ronda ' + str(ronda))
         
        board_id = information[0]['Placa']
        port = information[0]['Puerto']
        board = prepare(board_id, port)
        
        board.prepare_session ()
        t0 = time.time()
        board.start_stream ()
        
        # if (ronda==1):
            
        #     hilo = threading.Thread(target=data_sent.append(board.get_current_board_data(32)), args=(board,))
        #     hilo.start()
        
            
        with kb.Listener(siguiente_ronda) as escuchador:
            escuchador.join()
            
        print('Ronda '+str(ronda))
        markers, tiempos, markers_list = experiment(information,board)    
       
        
        board.stop_stream ()
        tf = time.time()
        data = board.get_board_data ()
        board.release_session ()
               
        samples = []
        channel = board.get_timestamp_channel(board_id)
        j=0
        
        for i in range(len(tiempos)):
            aux = tiempos [i] - t0
               
            while ((data [channel][j]-t0)<aux):
                j=j+1
            sample_anterior = (data [channel][j-1]-t0)-aux
            sample_sig = (data [channel][j]-t0)-aux
            if (sample_anterior<sample_sig):
                samples.append(j-1)
            else:
                samples.append(j)


        freq = board.get_sampling_rate(board_id)
        tiempo_registro = np.arange(0, tf-t0, 1/freq)
        
        tiempos_rel = np.array(tiempos)-t0
        duracion = np.diff(tiempos_rel)
        duracion= np.append(duracion,0)
               
        values =[]
        for i in range(len(markers)):
            if markers[i]=='std':
                values.append(2)
            else:
                values.append(1)
        
        my_event_file =  np.vstack((tiempos_rel, duracion, markers,values, samples ))
        
        
        raw_bids(board_id,board,data,information, markers, markers_list, ronda)
        nombre_archivo = 'sub-' + str(information[0]['Sujeto']) + '_ses-' + str(information[0]['Sesion'])  + '_task-' + str(information[0]['Tarea'])+'_run-0'+str(ronda)
        bids_path =data_path = 'C:/Users/PaulaSaavedra/PaulaGD/IMAL/PA_Interfaz/Interfaz/'+ information[0]['Tarea'] + '/BIDS/' + 'sub-' + str(information[0]['Sujeto']) + '/' +  'ses-' + str(information[0]['Sesion']) + '/eeg/'
        os.chdir(bids_path)
        
        
        with open(nombre_archivo + '_eventos.tsv', 'w', newline='') as f_output:
            header = ['onset', 'duration','trial_type', 'value', 'sample' ]
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(header)
            for col in range(len(my_event_file.T)):
                tsv_output.writerow(my_event_file[:,col])

        observations.append(observations(ronda))
        
    data_path = 'C:/Users/PaulaSaavedra/PaulaGD/IMAL/PA_Interfaz/Interfaz/'+ information[0]['Tarea'] + '/BIDS/Code/Anotaciones/'    
    if (int(information[0]['Sesion'])==1):
        os.makedirs(data_path)
    os.chdir(data_path)    
    archivo = 'sub-' + str(information[0]['Sujeto']) + '_ses-' + str(information[0]['Sesion'])  + '_task-' + str(information[0]['Tarea'] + 'run0' + str(ronda))
    with open(archivo + '.json', 'w') as file:
            json.dump(observations, file, indent=1)
        

if __name__ == '__main__':
    main()

