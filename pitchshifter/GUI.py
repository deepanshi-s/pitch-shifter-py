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
import shutil
from PIL import Image, ImageTk
import cv2



class GUI:
    def __init__(self):
        self.startFlag = True
        self.window = tk.Tk()
        
        self.parentDir = 'C:/Users/Admin/Documents/grad_school/sem2/dsp-speech/project/pitch-shifter-py'
        
        self.panelA = None
        self.panelB = None
        self.panelC = None
        self.pandelD = None
        
        #greeting = tk.Label(text="Hello, this is a GUI for pitch shift")
        #greeting.pack()
        
        
        
        #for feedback
        '''
        text_box = tk.Text()
        text_box.pack()
        '''

        self.buttonframe = tk.Frame(self.window)
        self.buttonframe.grid(row = 2, column=0, columnspan=2)
        
        button = tk.Button(self.buttonframe,
            text="Select Files",
            width=25,
            height=2)
        button.grid(row = 0, column = 0)
        button.bind("<Button-1>", self.handleClick)
        
        button3 = tk.Button(self.buttonframe,
           text="Play Original Sound",
           width=25,
           height=2)
        button3.grid(row = 0, column = 1)
        button3.bind("<Button-1>", self.play)
        
        button2 = tk.Button(self.buttonframe,
            text="Modify Frequency",
            width=25,
            height=2)
        button2.grid(row = 0, column = 2)
        button2.bind("<Button-1>", self.modifyFreq)
        
        button3 = tk.Button(self.buttonframe,
            text="Play New Sound",
            width=25,
            height=2)
        button3.grid(row = 0, column = 3)
        button3.bind("<Button-1>", self.playNewSound)
        
        
        #self.buttonframe = tk.Frame(self.window)
        #self.buttonframe.grid(row = 10, column=0, columnspan=2)
        
        button4 = tk.Button(self.buttonframe,
            text="Quit",
            width=25,
            height=2, command = self.window.destroy)
        button4.grid(row = 0, column = 4)
        #tk.Button(self.window, text="Quit", command=self.window.destroy).pack()
        
        
        T1 = tk.Label(self.window, text = "Start Time")
        T1.grid(row = 10, column = 0) 
        
        w1 = tk.Scale(self.window, from_ = 0, to = 100, orient= tk.HORIZONTAL, command=self.startTimefunc) 
        w1.grid(row = 10, column = 1)


        T2  = tk.Label(self.window, text = "End time")
        T2.grid(row = 11, column = 0)  
        
        w2 = tk.Scale(self.window, from_ = 0, to = 100, orient= tk.HORIZONTAL, command=self.endTimefunc) 
        w2.grid(row = 11, column = 1)

        
        T3  = tk.Label(self.window, text = "Frequency")
        T3.grid(row = 12, column = 0)
        
        w4 = tk.Scale(self.window, from_ = 10, to = 100, orient= tk.HORIZONTAL, command=self.pitchFunc) 
        w4.grid(row = 12, column = 1)
        
        
        
        self.window.mainloop()
    
    
    def addImage(self):
        print('inadd Image')
        print(self.parentDir, 'plots', (self.wavfile.split("/")[-1].split(".")[0] + '.png'))
        
        ogPlot = cv2.imread(os.path.join(self.parentDir, 'plots', (self.wavfile.split("/")[-1].split(".")[0] + '.png')))
        ogPlot = cv2.cvtColor(ogPlot, cv2.COLOR_BGR2RGB)
        ogPlot = cv2.resize(ogPlot, (350, 350))
        ogPlot = Image.fromarray(ogPlot)
        ogPlot = ImageTk.PhotoImage(ogPlot)
        
        print(os.path.join(self.parentDir, 'plots', ('modified_' + self.nameFile.split(".")[0] + '.png')))
        newPlot = cv2.imread(os.path.join(self.parentDir, 'plots', ('modified_' + str(self.nameFile.split(".")[0]) + '.png')))
        newPlot = cv2.cvtColor(newPlot, cv2.COLOR_BGR2RGB)
        newPlot = cv2.resize(newPlot, (350, 350))
        newPlot = Image.fromarray(newPlot)
        newPlot = ImageTk.PhotoImage(newPlot)        
        
        if self.panelA is None or self.panelB:
            print('if cond')
            self.panelA = tk.Label(self.window,text="Metrics hereplot 1",font = 40)
            self.panelA.image = ogPlot
            self.panelA.configure(image=ogPlot)
            self.panelA.grid(row = 14, column =0)
            
            self.panelB = tk.Label(self.window)
            self.panelB.image = newPlot
            self.panelB.configure(image =  newPlot)
            self.panelB.grid(row = 14, column = 1)
            #self.panelA.pack(side="left")
        
        else:
            #self.panelA.image = None
            #self.panelA.configure(image = None)

            self.panelA.configure(image = ogPlot)
            self.panelA.image = ogPlot
            
            self.panelB.configure(image = newPlot)
            self.panelB.image = newPlot
        
        
        
    def pitchFunc(self, x):
        self.pitch = float(x)/200.
        
    def startTimefunc(self, startTime):
        self.startTime = startTime
        
    def endTimefunc(self, endTime):
        self.endTime = endTime
        
    def play(self, x):
        playsound(self.wavfile)  
        
    def playNewSound(self, x):
        playsound(os.path.join(self.parentDir, 'output', ('modified_', self.wavfile.split("/")[-1]))) 
    
    def saveFig(self, name, plotName):
        #add in a frame
        self.fig = Figure(figsize = (10, 5), dpi = 100)
        self.plot1 = self.fig.add_subplot(111)
        source = scipy.io.wavfile.read(name)
        signal = source[1]
        
        fs = source[0]
        Time = np.linspace(0, len(signal)/fs, num=len(signal))
                
  
        # plotting the graph
        plt.plot(Time, signal)
        print(os.path.join(self.parentDir, 'plots', plotName))
        
        plt.savefig(os.path.join(self.parentDir, 'plots', plotName))
        plt.clf()
        
  
    def modifyFreq(self, h):
        pitchShifter(self.wavfile, name = self.nameFile, startTime= int(self.startTime), endTime = int(self.endTime), pitch = float(self.pitch), out = os.path.join(self.parentDir,'output', ('modified_' +self.wavfile.split("/")[-1])))
        self.saveFig(os.path.join(self.parentDir,'output', ('modified_' + self.wavfile.split("/")[-1])), 'modified_' + self.nameFile.split(".")[0] + '.png')
        self.addImage()
        
    def handleClick(self, x):
        #clear plot frame
    
            
        filetypes = (('wav files', '*.wav'), ('All files', '*.*'))
        
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        
        self.nameFile = filename.split("/")[-1]
        self.wavfile = filename
        showinfo(title='Selected File', message=filename)
        print(os.getcwd())
        
        self.saveFig(self.wavfile, self.nameFile.split(".")[0] + '.png')
        #self.addImage()
        
        
        

def main():
    GUI()


if __name__ == "__main__":
    main()


    
        
       