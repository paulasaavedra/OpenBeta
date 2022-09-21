# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 10:03:28 2021

@author: PaulaSaavedra
"""
import datetime
import os.path as op
import mne
from mne_bids import (write_raw_bids, BIDSPath)
import json
import os
import numpy as np

def raw_bids(board_id,board,data,infor, markers_list, run, folder_path):
    """
    Write BIDS format files.
    
    Parameters
    ----------
    board_id : int
        Integer that determines which board is used:
            Synthetic: -1
            Cyton: 0
            Ganglion: 1
            Cyton Daisy: 2
    board : board_shim.BoardShim
        brainflow.board_shim object
        allows to read the board.
    data : Array de float64
        Values from the board.
        Dimensions depending on the type and time of acquisition.

    Returns
    -------
    None.

    """
    eeg_channels = board.get_eeg_channels(board_id)
    eeg_data = data[eeg_channels, :]
    eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE

    # Creating MNE objects from brainflow data arrays
    ch_types = ['eeg'] * len(eeg_channels)
    ch_names = board.get_eeg_names(board_id)
 
               
    sfreq = board.get_sampling_rate(board_id)
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    raw = mne.io.RawArray(eeg_data, info)
    
    # measurement date
    meas_date = datetime.datetime.now(datetime.timezone.utc)
    raw.set_meas_date(meas_date)
    
    raw.info['line_freq']=50
    
    # Date of Birth
    dob = infor[0]['Fecha_de_Nacimiento']
    year = int(dob[6:])
    month = int(dob[3:5])
    day = int(dob[0:2])
    dob = [year,month,day]
    
    # gender
    gender = infor[0]['Genero']
    if (gender == 'Masculino'):
        gen = 1
    elif (gender == 'Femenino'):
        gen = 2
    else:
        gen = 0
    
    # dominance
    dominance = infor[0]['Dominancia']
    if (dominance == 'Derecha'):
        domi = 1
    elif (dominance == 'Izquierda'):
        domi = 2
    else:
        domi = 3
    
    raw.info['subject_info']={'sex':gen,'birthday':dob,'hand':domi}
    
    data_path = folder_path + '/' + infor[0]['Tarea'] + '/BIDS/'
    
    bids_path = BIDSPath(subject=infor[0]['Sujeto'], session=infor[0]['Sesion'],
                         task=infor[0]['Tarea'], run='0'+str(run), root=data_path)
    
    eventos = []
    tam = len(ch_names)+15 
    for i in range(len(data[tam])):
        if (data[tam][i]!=0):
            eventos.append([i,0, data[tam][i]])
            
    eventos_array=np.array(eventos[:][:][:])

    write_raw_bids(raw, bids_path, format='BrainVision',allow_preload=True, events_data=eventos_array, event_id=markers_list, overwrite=True);        
    
    # events.json           
    fileName = 'task-'+ infor[0]['Tarea'] + '_events.json'
    data = {}
    data['onset'] = []
    data['onset'].append({
        'Description': 'Event onset',
        'Units': 'second'})
    
    data['duration'] = []
    data['duration'].append({
        'Description': 'Event duration',
        'Units': 'second'})
    
    data['value'] = []
    data['value'].append({
        'Description': 'Value of event (numerical)',
        'Levels': {
            "1": "deviant",
            "2": "std"}})
    with open(os.path.join(data_path, fileName), 'w') as file:
        json.dump(data, file, indent=4)
        
        