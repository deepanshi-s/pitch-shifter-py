# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 03:03:23 2022

@author: Admin
"""

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import os 
from pitchShifterfunc import pitchShifter
from matplotlib.figure import Figure
import scipy.io.wavfile
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np


#from tk import Label,Button,Scroller


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        greeting = tk.Label(text="Hello, this is a GUI for pitch shift")
        greeting.pack()
        
        button = tk.Button(
            text="Select Files",
            width=25,
            height=2)
        button.pack()
        button.bind("<Button-1>", self.handleClick)
        
        #for feedback
        '''
        text_box = tk.Text()
        text_box.pack()
        '''
        
        frame_a = tk.Frame()
        frame_b = tk.Frame()
        
        frame_a.pack()
        frame_b.pack()
        
        

        
        self.window.mainloop()
    
    def displaySig(self):
        #add in a frame
        source = scipy.io.wavfile.read(self.wavfile)
        signal = source[1]
        fig = Figure(figsize = (10, 5), dpi = 100)
        fs = source[0]
        Time = np.linspace(0, len(signal)/fs, num=len(signal))
        
        print(Time, fs)
        plot1 = fig.add_subplot(111)
  
        # plotting the graph
        plot1.plot(Time, signal)
      
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig,
                                   master = self.window)  
        canvas.draw()
      
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
      
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                       self.window)
        toolbar.update()
      
        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
  
        
    def handleClick(self, x):
        #clear plot frame
        filetypes = (('wav files', '*.wav'), ('All files', '*.*'))
        
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        
        self.wavfile = filename
        
        showinfo(title='Selected File', message=filename)
        print(os.getcwd())
        self.displaySig()
        #pitchShifter(self.wavfile, pitch =1, out = os.path.join(os.getcwd(),'out.wav'))
        
        
        

def main():
    GUI()


if __name__ == "__main__":
    main()


    
        
       