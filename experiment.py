# -*- coding: utf-8 -*-
"""
Created on Thu May 19 13:37:51 2022

@author: PaulaSaavedra
"""

from psychopy import visual, core, sound, monitors, prefs
import random
import psychtoolbox as ptb
import keyboard
import time

def experiment (info, board):
  
    prefs.hardware['audioLib'] = ['sounddevice','PTB', 'pyo','pygame']
    
        
    trial = ['std']*50
    positions = []
    aux=[]
    while (len(aux)<10):
        positions.append(random.randrange(2,50,3))
        aux = set(positions)
    
    aux = list(aux)    
    for i in range(10):
        trial[aux[i]]='deviant'
        
    markers_list = {'deviant':1, 'std':2}
    markers = []
    times = []
    mon = monitors.Monitor('SMB2030N')
    mon.setDistance(114)
    window = visual.Window(fullscr=False, screen=1)
    

    for tri in range(len(trial)):
        if (keyboard.is_pressed('q')==False):
            if (trial[tri] =='std'):
                std = sound.Sound(500,0.075)
                now_std = ptb.GetSecs()
                board.insert_marker(markers_list['std'])
                markers.append('std')
                std.play(when= now_std)
                t0 = time.time()
                times.append(t0)
                core.wait(0.075)
                core.wait(0.5)
            else:
                deviant = sound.Sound(1000,0.03)
                now_deviant = ptb.GetSecs()
                board.insert_marker(markers_list['deviant'])
                markers.append('deviant')
                deviant.play(when= now_deviant)
                t0 = time.time()
                times.append(t0)
                core.wait(0.03)
                core.wait(0.5)

        else:
            break
    window.close()
    return markers, times, markers_list