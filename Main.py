# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 12:15:42 2021

@author: paula
"""

import os
folder_path = 'C:/Users/PaulaSaavedra/PaulaGD/IMAL/OpenBeta'

os.chdir(folder_path)

from pynput import keyboard as kb
from subject_data import subject_data
from prepare import prepare
from raw_bids import raw_bids
from observations import observations
import json
#import realtime
#import threading
import time
import numpy as np
import csv


# Acá se importan los experimentos
from experiment import experiment 

#%%
def main():
    
    information = subject_data(folder_path)
   
    def next_run(tecla):
        if tecla == kb.KeyCode.from_char('x'):
            return False
    escuchador = kb.Listener(next_run)
    
    runs = int(information[0]['Rondas']) 
    observations_list = []
    
    for run in range(1,runs+1):
        
       
        board_id = information[0]['Placa']
        port = information[0]['Puerto']
        board = prepare(board_id, port)
        
        board.prepare_session ()
        t0 = time.time()
        board.start_stream ()
        
        print('Presione x para comenzar con la ronda ' + str(run))
        
        # if (run==1):
            
        #     hilo = threading.Thread(target=data_sent.append(board.get_current_board_data(32)), args=(board,))
        #     hilo.start()
        
            
        with kb.Listener(next_run) as escuchador:
            escuchador.join()
            
        print('Ronda '+str(run))
        markers, tiempos, markers_list = experiment(information,board)    
       
        
        board.stop_stream ()
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
        
        
        raw_bids(board_id,board,data,information, markers_list, run, folder_path)
        nombre_archivo = 'sub-' + str(information[0]['Sujeto']) + '_ses-' + str(information[0]['Sesion'])  + '_task-' + str(information[0]['Tarea'])+'_run-0'+str(run)
        bids_path = folder_path + '/' + information[0]['Tarea'] + '/BIDS/' + 'sub-' + str(information[0]['Sujeto']) + '/' +  'ses-' + str(information[0]['Sesion']) + '/eeg/'
        os.chdir(bids_path)
        
        
        with open(nombre_archivo + '_eventos.tsv', 'w', newline='') as f_output:
            header = ['onset', 'duration','trial_type', 'value', 'sample' ]
            tsv_output = csv.writer(f_output, delimiter='\t')
            tsv_output.writerow(header)
            for col in range(len(my_event_file.T)):
                tsv_output.writerow(my_event_file[:,col])

        observations_list.append(observations(run))
        
    data_path = folder_path + information[0]['Tarea'] + '/BIDS/Code/Anotaciones/'    
    if (int(information[0]['Sesion'])==1):
        os.makedirs(data_path)
    os.chdir(data_path)    
    archivo = 'sub-' + str(information[0]['Sujeto']) + '_ses-' + str(information[0]['Sesion'])  + '_task-' + str(information[0]['Tarea'] + 'run0' + str(run))
    with open(archivo + '.json', 'w') as file:
            json.dump(observations_list, file, indent=1)
        

if __name__ == '__main__':
    main()

