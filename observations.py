# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 15:30:07 2022

@author: PaulaSaavedra
"""

import tkinter as tk

def observations(run):
    window = tk.Tk()
    window.geometry("340x200")
    window.title('Anotaciones')
    
    info = []
    def GuardarTexto():
        anotaciones = chart.get("1.0","end")
        info.append('ronda_'+str(run))
        info.append(anotaciones)
    
    def Borrar():
        chart.delete("1.0","end")
        
    
    chart=tk.Text(window, height=10, width=45)
    chart.pack(side='top')
    
    borrar = tk.Button(window, height = 1, width = 15, text = "Borrar", command = Borrar)
    guardar = tk.Button(window, height = 1, width = 15, text = "Guardar", command = GuardarTexto)
    salir = tk.Button(window, height = 1, width = 15, text = "Salir", command = window.destroy)
    
    salir.pack(side='right')
    guardar.pack(side='right')
    borrar.pack(side='right')
    
    window.mainloop()
    return info
