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
import matplotlib.pyplot as plt
from playsound import playsound

#from tk import Label,Button,Scroller


class GUI:
    def __init__(self):
        self.startFlag = True
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
        
        button3 = tk.Button(
            text="Play Original Sound",
            width=25,
            height=2)
        button3.pack()
        button3.bind("<Button-1>", self.play)
        
        frame_a = tk.Frame()
        frame_b = tk.Frame()
        
        frame_a.pack()
        frame_b.pack()
        
        T = tk.Label(self.window, text = "Start Time")
        T.pack() 
        
        w = tk.Scale(self.window, from_ = 0, to = 100, orient= tk.HORIZONTAL, command=self.startTimefunc) 
        w.pack()
        
        T  = tk.Label(self.window, text = "End time")
        T.pack() 
        
        w = tk.Scale(self.window, from_ = 0, to = 100, orient= tk.HORIZONTAL, command=self.endTimefunc) 
        w.pack()
        
        button2 = tk.Button(
            text="Modify Frequency",
            width=25,
            height=2)
        button2.pack()
        button2.bind("<Button-1>", self.modifyFreq)
        
        button3 = tk.Button(
            text="Play New Sound",
            width=25,
            height=2)
        button3.pack()
        button3.bind("<Button-1>", self.playNewSound)

            
        self.window.mainloop()
    
    def startTimefunc(self, startTime):
        self.startTime = startTime
        
    def endTimefunc(self, endTime):
        self.endTime = endTime
        
    def play(self, x):
        playsound(self.wavfile)  
        
    def playNewSound(self, x):
        playsound(os.path.join(os.getcwd(),self.wavfile.split("/")[-1]))  
    
    def displaySig(self):
        #add in a frame
        self.fig = Figure(figsize = (10, 5), dpi = 100)
        self.plot1 = self.fig.add_subplot(111)
        source = scipy.io.wavfile.read(self.wavfile)
        signal = source[1]
        
        fs = source[0]
        Time = np.linspace(0, len(signal)/fs, num=len(signal))
                
  
        # plotting the graph
        self.plot1.plot(Time, signal)
      
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        self.canvas = FigureCanvasTkAgg(self.fig,
                                   master = self.window)  
        self.canvas.draw()
      
        # placing the canvas on the Tkinter window
        self.canvas.get_tk_widget().pack()
      
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(self.canvas,
                                       self.window)
        toolbar.update()
      
        # placing the toolbar on the Tkinter window
        self.canvas.get_tk_widget().pack()
  
    def modifyFreq(self, h):
        pitchShifter(self.wavfile, startTime= int(self.startTime), endTime = int(self.endTime), pitch = int(1), out = os.path.join(os.getcwd(),self.wavfile.split("/")[-1]))
        
        
    def handleClick(self, x):
        #clear plot frame
    
            
        filetypes = (('wav files', '*.wav'), ('All files', '*.*'))
        
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        
        self.wavfile = filename
        showinfo(title='Selected File', message=filename)
        print(os.getcwd())
        #self.displaySig()
        
        
        

def main():
    GUI()


if __name__ == "__main__":
    main()


    
        
       