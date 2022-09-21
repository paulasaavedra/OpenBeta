# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 08:58:28 2021

@author: PaulaSaavedra
"""

import json
import os
from tkinter import Tk, ttk,font,Label, Entry, IntVar, StringVar, Radiobutton, Checkbutton, PhotoImage

def subject_data(folder_path):
    
    '''
    
    Load subject data,
    choose which board will be used, or simulation,
    load data that the board requires,
    select the number of channels
    name channels or load channel names from a ch_names.txt
    
    Returns
    -------
    subject_data: it is a dictionary with all the information loaded.

    '''
    
    root = Tk()
    root.resizable(width=0, height=0)
    root.title('Nueva adquisición')
    root.grid()
    
    header = PhotoImage(file='header.png')
    Label(root, image=header, bd=0).grid(row=0,columnspan=8)
    
    bold = font.Font(weight='bold')
    
    subject_data_title = Label(root, text='Datos sujeto:', font = font.Font(weight='bold'))
    subject_data_title.grid(row=1,column=0, sticky='W', padx=5, pady=5)
    
    # Load subject information
    subject = StringVar()
    label_subject = Label(root, text='Sujeto:')
    label_subject.grid(row=2,column=0, sticky='E', padx=5, pady=5)
    entry_subject = Entry(root, textvariable=subject)
    entry_subject.grid(row=2,column=1, padx=5, pady=5)
    
    # Load date of birth. Format: dd/mm/yyyy
    birth_data = StringVar()
    label_birth_data = Label(root, text='F. de Nac.:')
    label_birth_data.grid(row=2,column=2, sticky='E', padx=5, pady=5)
    entry_birth_data = Entry(root, textvariable=birth_data)
    entry_birth_data.grid(row=2,column=3, padx=5, pady=5)
        
    # Load experiment name
    experiment_name = StringVar()
    label_experiment_name = Label(root, text='Tarea:')
    label_experiment_name.grid(row=3,column=0, sticky='E', padx=5, pady=5)
    entry_experiment_name = Entry(root, textvariable=experiment_name)
    entry_experiment_name.grid(row=3,column=1, padx=5, pady=5)
    
    # Load session
    session = StringVar()
    label_session = Label(root, text='Sesión:')
    label_session.grid(row=3,column=2, sticky='E', padx=5, pady=5)
    entry_session = Entry(root, textvariable=session)
    entry_session.grid(row=3,column=3, padx=5, pady=5)
    
    # Load gender
    gender = StringVar()
    gender.set(None)  
    label_select_gender = Label(root, text='Seleccionar género:')
    label_select_gender.grid(row=4,column=0, sticky='E',pady=5)
        
    Radiobutton(root, text='Femenino', variable=gender, 
                value='Femenino').grid(row=4,column=1, sticky='W')
    Radiobutton(root, text='Masculino', variable=gender, 
                value='Masculino').grid(row=5,column=1,sticky='W')
    Radiobutton(root, text='Otro', variable=gender, 
                value='Otro').grid(row=6,column=1, sticky='W')
    
    # Load dominance
    dominance = StringVar()
    dominance.set(None) 
    label_select_dominance = Label(root, text='Seleccionar dominancia:')
    label_select_dominance.grid(row=4,column=3, sticky='E',pady=5)
    
    Radiobutton(root, text='Derecha', variable=dominance, 
                value='Derecha').grid(row=4,column=4, sticky='W')
    Radiobutton(root, text='Izquierda', variable=dominance, 
                value='Izquierda').grid(row=5,column=4, sticky='W')
    Radiobutton(root, text='Ambidiestro', variable=dominance, 
                value='Ambidiestro').grid(row=6,column=4, sticky='W')
    
    # Load pathology
    pathology = StringVar()
    pathology.set(None) 
    label_select_pathology = Label(root, text='Patologías?')
    label_select_pathology.grid(row=4,column=5, sticky='E',pady=5)
    
    Radiobutton(root, text='No', variable=pathology, 
                value='No').grid(row=4,column=6, sticky='W')
    Radiobutton(root, text='Si', variable=pathology, 
                value='Si').grid(row=5,column=6, sticky='W')
    
    separator1 = ttk.Separator(root)
    separator1.grid(row=12, padx=5, pady=5)
    
    
    technical_data = Label(root, text='Datos técnicos:', font = bold)
    technical_data.grid(row=13,column=0, sticky='W', padx=5, pady=5)
    
    
    # Load total round
    total_rounds = IntVar()
    total_rounds.set(1)
    label_total_rounds = Label(root, text='Rondas totales:')
    label_total_rounds.grid(row=14,column=0, sticky='E', padx=5, pady=5)
    entry_total_rounds = Entry(root, textvariable=total_rounds)
    entry_total_rounds.grid(row=14,column=1, padx=5, pady=5)
    
    # Load start round. 
    # For example, if you want to start recording the second round, put 2. 
    # The total number of rounds indicated in the previous variable is respected.
    round_start = IntVar()
    round_start.set(1)
    label_round_start = Label(root, text='Comienza en:')
    label_round_start.grid(row=14,column=3, sticky='E', padx=5, pady=5)
    entry_round_start = Entry(root, textvariable=round_start)
    entry_round_start.grid(row=14,column=4, padx=5, pady=5)
    
    
    # Load board. Option 3 is when no board is selected
    board = IntVar()
    board.set(3)  
    label_select_board = Label(root, text='Seleccionar placa:')
    label_select_board.grid(row=15,column=0, sticky='E',pady=5)
        
    Radiobutton(root, text='Simulación', variable=board, 
                value=-1).grid(row=15,column=1, sticky='W')
    Radiobutton(root, text='Cyton', variable=board, 
                value=0).grid(row=16,column=1,sticky='W')
    Radiobutton(root, text='Cyton Daisy', variable=board, 
                value=2).grid(row=17,column=1, sticky='W')
    Radiobutton(root, text='Ganglion', variable=board, 
                value=1).grid(row=18,column=1,sticky='W')
    
    # Load port
    port = StringVar()
    label_port = Label(root, text='Puerto:')
    label_port.grid(row=16,column=2, sticky='E', padx=5, pady=5)
    entry_port = Entry(root, textvariable=port)
    entry_port.grid(row=16,column=3, padx=5, pady=5) 
      
    # Channels
    # 1 if selected. 0 if not selected
    label_channels = Label(root, text='Seleccionar canales:')
    label_channels.grid(row=19,column=0, sticky='E', padx=5, pady=5)
    
    C8 = IntVar()
    C8.set(0)
    Radiobutton(root, text='8 canales', variable=C8, 
                value=1).grid(row=19,column=2, sticky='W')
    
    C16 = IntVar()
    C16.set(0)
    Radiobutton(root, text='16 canales', variable=C16, 
                value=1).grid(row=19,column=4, sticky='W')
    
    # Selecting this option also indicates the number of channels to be registered
    ch_names_option = IntVar()
    ch_names_option.set(0)
    Radiobutton(root, text='Cargar nombres desde un .txt', variable=ch_names_option,
                value=1).grid(row=19, column=5, sticky='W')

       
    CH1 = IntVar()
    CH1.set(0)
    Checkbutton(root, text="CH1", variable=CH1).grid(row=20, column=0)
    label_CH1 = StringVar()
    entry_CH1 = Entry(root, textvariable=label_CH1)
    entry_CH1.grid(row=20, column=1, sticky='E')
    
    CH2 = IntVar()
    CH2.set(0)
    Checkbutton(root, text="CH2", variable=CH2).grid(row=20, column=2)
    label_CH2 = StringVar()
    entry_CH2 = Entry(root, textvariable=label_CH2)
    entry_CH2.grid(row=20, column=3)
    
    CH3 = IntVar()
    CH3.set(0)
    Checkbutton(root, text="CH3", variable=CH3).grid(row=20, column=4)
    label_CH3 = StringVar()
    entry_CH3 = Entry(root, textvariable=label_CH3)
    entry_CH3.grid(row=20, column=5)
    
    CH4 = IntVar()
    CH4.set(0)
    Checkbutton(root, text="CH4", variable=CH4).grid(row=20, column=6)
    label_CH4 = StringVar()
    entry_CH4 = Entry(root, textvariable=label_CH4)
    entry_CH4.grid(row=20, column=7,padx=5, pady=5)
    
    CH5 = IntVar()
    CH5.set(0)
    Checkbutton(root, text="CH5", variable=CH5).grid(row=21, column=0)
    label_CH5 = StringVar()
    entry_CH5 = Entry(root, textvariable=label_CH5)
    entry_CH5.grid(row=21, column=1, sticky='E')
    
    CH6 = IntVar()
    CH6.set(0)
    Checkbutton(root, text="CH6", variable=CH6).grid(row=21, column=2)
    label_CH6 = StringVar()
    entry_CH6 = Entry(root, textvariable=label_CH6)
    entry_CH6.grid(row=21, column=3)
    
    CH7 = IntVar()
    CH7.set(0)
    Checkbutton(root, text="CH7", variable=CH7).grid(row=21, column=4)
    label_CH7 = StringVar()
    entry_CH7 = Entry(root, textvariable=label_CH7)
    entry_CH7.grid(row=21, column=5)
    
    CH8 = IntVar()
    CH8.set(0)
    Checkbutton(root, text="CH8", variable=CH8).grid(row=21, column=6)
    label_CH8 = StringVar()
    entry_CH8 = Entry(root, textvariable=label_CH8)
    entry_CH8.grid(row=21, column=7,padx=5, pady=5)
    
    CH9 = IntVar()
    CH9.set(0)
    Checkbutton(root, text="CH9", variable=CH9).grid(row=22, column=0)
    label_CH9 = StringVar()
    entry_CH9 = Entry(root, textvariable=label_CH9)
    entry_CH9.grid(row=22, column=1, sticky='E')
    
    CH10 = IntVar()
    CH10.set(0)
    Checkbutton(root, text="CH10", variable=CH10).grid(row=22, column=2)
    label_CH10 = StringVar()
    entry_CH10 = Entry(root, textvariable=label_CH10)
    entry_CH10.grid(row=22, column=3)
    
    CH11 = IntVar()
    CH11.set(0)
    Checkbutton(root, text="CH11", variable=CH11).grid(row=22, column=4)
    label_CH11 = StringVar()
    entry_CH11 = Entry(root, textvariable=label_CH11)
    entry_CH11.grid(row=22, column=5)
    
    CH12 = IntVar()
    CH12.set(0)
    Checkbutton(root, text="CH12", variable=CH12).grid(row=22, column=6)
    label_CH12 = StringVar()
    entry_CH12 = Entry(root, textvariable=label_CH12)
    entry_CH12.grid(row=22, column=7,padx=5, pady=5)
    
    CH13 = IntVar()
    CH13.set(0)
    Checkbutton(root, text="CH13", variable=CH13).grid(row=23, column=0)
    label_CH13 = StringVar()
    entry_CH13 = Entry(root, textvariable=label_CH13)
    entry_CH13.grid(row=23, column=1, sticky='E')
    
    CH14 = IntVar()
    CH14.set(0)
    Checkbutton(root, text="CH14", variable=CH14).grid(row=23, column=2)
    label_CH14 = StringVar()
    entry_CH14 = Entry(root, textvariable=label_CH14)
    entry_CH14.grid(row=23, column=3)
    
    CH15 = IntVar()
    CH15.set(0)
    Checkbutton(root, text="CH15", variable=CH15).grid(row=23, column=4)
    label_CH15 = StringVar()
    entry_CH15 = Entry(root, textvariable=label_CH15)
    entry_CH15.grid(row=23, column=5)
    
    CH16 = IntVar()
    CH16.set(0)
    Checkbutton(root, text="CH16", variable=CH16).grid(row=23, column=6)
    label_CH16 = StringVar()
    entry_CH16 = Entry(root, textvariable=label_CH16)
    entry_CH16.grid(row=23, column=7,padx=5, pady=5)

    channelList = [CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8, CH9, CH10, CH11, CH12, CH13, CH14, CH15, CH16]
    labelChannelList = [label_CH1, label_CH2, label_CH3, label_CH4, label_CH5, label_CH6, label_CH6, label_CH7, label_CH8, label_CH9, label_CH10, label_CH11, label_CH12, label_CH13, label_CH14, label_CH15, CH16]
    info = []
    
    def clear_data():
        subject.set('')
        birth_data.set('')
        experiment_name.set('')
        session.set('')
        total_rounds.set('')
        round_start.set('')
        port.set('')
                
        gender.set(None)
        label_select_gender.config(text='Seleccionar género:')
        dominance.set(None)
        label_select_dominance.config(text='Seleccionar dominancia:')
        pathology.set(None)
        label_select_pathology.config(text='Patologías?')
        board.set(3)
        total_rounds.set(1)
        round_start.set(1)
        label_select_board.config(text='Seleccionar placa:')
        C8.set(0), C16.set(0), ch_names_option.set(0),
        for i in range(16):
            channelList[i].set(0)
        for i in range(16):
            labelChannelList[i].set('')
        
    
    def save_data():
        if (C8.get()==1):
            for i in range(8):
                channelList[i].set(1)
           
        elif (C16.get()==1):
            for i in range(16):
                channelList[i].set(1)
        else:
            for i in range(8):
                channelList[i].set(1)
           
                    
        information = {
            'Sujeto': entry_subject.get(),
            'Fecha_de_Nacimiento': entry_birth_data.get(),
            'Tarea':entry_experiment_name.get(),
            'Sesion': entry_session.get(),
            'Genero':gender.get(),
            'Dominancia':dominance.get(),
            'Patologia': pathology.get(),
            'Rondas': entry_total_rounds.get(),
            'Ronda_inicio': entry_round_start.get(),
            'Placa': board.get(),
            'Puerto': port.get(),
            'Canales':[CH1.get(), CH2.get(), CH3.get(), CH4.get(),
                       CH5.get(), CH6.get(), CH7.get(), CH8.get(),
                       CH9.get(), CH10.get(), CH11.get(), CH12.get(),
                       CH13.get(), CH14.get(), CH15.get(), CH16.get()],   
            'Nombre_canales':[label_CH1.get(), label_CH2.get(), label_CH3.get(), label_CH4.get(),
                       label_CH5.get(), label_CH6.get(), label_CH7.get(), label_CH8.get(),
                       label_CH9.get(), label_CH10.get(), label_CH11.get(), label_CH12.get(),
                       label_CH13.get(), label_CH14.get(), label_CH15.get(), label_CH16.get()]
            }
       
        if (ch_names_option.get()==1):
            # Channel names file path
            os.chdir(folder_path)
            ch_names = open("ch_names.txt", "r")
            names = ch_names.readlines()
            for i in range(len(names)):
                information ['Nombre_canales'][i]= names[i].rstrip()
                channelList[i].set(1)
            ch_names.close()
        
        info.append(information)
        with open('datos.json', 'w') as file:
            json.dump(information, file, indent=4)
    
        
    
    separador2 = ttk.Separator(root)
    separador2.grid(row=24, padx=5, pady=5)
    
    ttk.Button(root, text='Borrar', command=clear_data).grid(row=25, column=3)
    ttk.Button(root, text='Guardar', command=save_data).grid(row=25, column=2)
    ttk.Button(root, text='Salir', command=root.destroy).grid(row=25, column=4)
    root.mainloop()
   
    return info
