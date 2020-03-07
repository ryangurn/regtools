"""

CollectData.py is the graphics modules dedicated to the setup and display of
the data collection window. It also handles user interaction with the window.

Authors:
(RegTools)
Joseph Goh
Mason Sayyadi
Owen McEvoy
Ryan Gurnick
Samuel Lundquist

Created:

"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import StudentModel
import ClassParser
import ClassModel
import threading
import random


class collectData(tk.Tk):
    def __init__(self, master, db_file):
        """
        Initializer for the CollectData window. This function requires the name
        of the database to connect and interact with, the master window from
        tkinter to interface with, and also the Listbox that contains the names
        of the students in the database.

        :param
        master :tkinter.Tk
        db_file :str

        Example Usage:
        //Called from MainMenu.py
        collectData(self.master, self.db)
        """
        self.db = db_file
        self.master = master

        self._lightGrey = "#b8b8b8"
        self._backgroundColor = "#323232"
        self._darkGrey = "#282929"
        self._green = "#369148"
        self._yellow = "#ffcc00"
        self._button = "<Button-1>"
        self.cm = ClassModel.ClassModel(self.db)
        self.s = ""

        # init variables for loading gif
        self.loadLabel = None
        self.loading = False
        self.frames = []
        self.frameIndex = 0
        index = 0
        filename = "./img/spinner-" + random.randint(0, 2) + ".gif"
        while index >= 0:
            try:
                frame = PhotoImage(file=filename, format='gif -index %i' % (index))
                print("Got image {}".format(str(index)))
                self.frames.append(frame)
                index += 1
            except:
                print("Couldn't get {}".format(str(index)))
                index = -1

        # Creates a frame to add to the master window
        self.master = master
        self.newWindow = Frame(master, bg=self._darkGrey)
        self.newWindow.place(x=0, y=150, height=600, width=800)

        # Year label
        yearLabel = Label(self.newWindow, text='Select the Year')
        yearLabel.place(x=100, y=150, height=30, width=150)
        yearLabel.config(font=("Arial Bold", 18))
        yearLabel.config(bg=self._darkGrey, fg="Grey")

        self.yearVal = StringVar(self.newWindow)
        yearChoices = sorted({'2015', '2016', '2017', '2018', '2019', '2020'})
        self.yearVal.set('2020')  # Default value
        yearMenu = OptionMenu(self.newWindow, self.yearVal, *yearChoices)
        yearMenu.place(x=100, y=185, width=150, height=30)
        yearMenu.config(bg=self._darkGrey)

        # Subject label
        subjectLabel = Label(self.newWindow, text='Select the Subject')
        subjectLabel.place(x=285, y=150, height=30, width=170)
        subjectLabel.config(font=("Arial Bold", 18))
        subjectLabel.config(bg=self._darkGrey, fg="Grey")

        self.subjectVal = StringVar(self.newWindow)
        subjectChoices = ["AAAP", "AAD", "ACTG", "AEIS", "AFR", "AIM", "ANTH", "ANTM", "ARB", "ARCH", "ARH", "ART",
                          "ARTC",
                          "ARTD", "ARTF", "ARTM", "ARTO", "ARTP", "ARTR", "ARTS", "ASIA", "ASL", "ASTR", "BA", "BI",
                          "BIKC",
                          "BIOE", "BLST", "CARC", "CAS", "CDS", "CFT", "CH", "CHKC", "CHN", "CHNF", "CINE", "CIS",
                          "CIT", "CLAS",
                          "COLT", "CPSY", "CRDG", "CRES", "CRWR", "CSCH", "DAN", "DANC", "DANE", "DIST", "DSGN", "EALL",
                          "EC",
                          "ECE", "EDLD", "EDST", "EDUC", "ENG", "ENVS", "ERTH", "ES", "ESC", "EURO", "FHS", "FIN",
                          "FINN", "FLR",
                          "FR", "GEOG", "GEOL", "GER", "GRK", "GRST", "GSAE", "GSCL", "GSGE", "GSST", "HBRW", "HC",
                          "HIST",
                          "HPHY", "HUM", "IARC", "ICH", "INTL", "IST", "ITAL", "J", "JDST", "JGS", "JPN", "KC", "KRN",
                          "LA",
                          "LAS", "LAT", "LAW", "LEAD", "LERC", "LIB", "LING", "LT", "MATH", "MDVL", "MENA", "MGMT",
                          "MIL",
                          "MKTG", "MUE", "MUJ", "MUP", "MUS", "NAS", "NORW", "OBA", "OIMB", "OLIS", "PD", "PDX", "PE",
                          "PEAQ",
                          "PEAS", "PEC", "PEF", "PEI", "PEIA", "PEL", "PEMA", "PEMB", "PEO", "PERS", "PERU", "PETS",
                          "PEW",
                          "PHIL", "PHKC", "PHYS", "PORT", "PPPM", "PREV", "PS", "PSY", "QST", "REES", "REL", "RL",
                          "RUSS",
                          "SBUS", "SCAN", "SCYP", "SERV", "SLP", "SOC", "SPAN", "SPD", "SPED", "SPM", "SPSY", "SWAH",
                          "SWED",
                          "TA", "TLC", "UGST", "WGS", "WR"]

        self.subjectVal.set('CIS')
        subjectMenu = OptionMenu(self.newWindow, self.subjectVal, *subjectChoices)
        subjectMenu.config(bg=self._darkGrey)
        subjectMenu.place(x=290, y=185, width=150, height=30)

        # Term label
        yearLabel = Label(self.newWindow, text='Select the Term')
        yearLabel.place(x=485, y=150, height=30, width=150)
        yearLabel.config(font=("Arial Bold", 18))
        yearLabel.config(bg=self._darkGrey, fg="Grey")

        self.termVal = StringVar(self.newWindow)
        termChoices = sorted({'Spring', 'Summer', 'Fall', 'Winter'})
        self.termVal.set('Spring')
        termMenu = OptionMenu(self.newWindow, self.termVal, *termChoices)
        termMenu.config(bg=self._darkGrey)
        termMenu.place(x=490, y=185, width=150, height=30)

        # Button to trigger the data collection
        self.collectData = Label(self.newWindow, text='Collect Data')
        self.collectData.config(font=("Arial Bold", 18), bg="#369148", fg=self._yellow)
        self.collectData.place(x=225, y=340, height=30, width=140)
        self.collectData.bind(self._button, self.dataCollectClick)

        # Button to close the "Select Data" window and go back to main menu
        self.exitName = Label(self.newWindow, text='Return Home')
        self.exitName.config(font=("Arial Bold", 18), bg="#369148", fg=self._yellow)
        self.exitName.place(x=410, y=340, height=30, width=140)
        self.exitName.bind(self._button, self.exitWindow)

    def initButtons(self):
        print("Initializing buttons")
        # Button to trigger the data collection
        self.collectData = Label(self.newWindow, text='Collect Data')
        self.collectData.config(font=("Arial Bold", 18), bg="#369148", fg=self._yellow)
        self.collectData.place(x=225, y=340, height=30, width=140)
        self.collectData.bind(self._button, self.dataCollectClick)

        # Button to close the "Select Data" window and go back to main menu
        self.exitName = Label(self.newWindow, text='Return Home')
        self.exitName.config(font=("Arial Bold", 18), bg="#369148", fg=self._yellow)
        self.exitName.place(x=410, y=340, height=30, width=140)
        self.exitName.bind(self._button, self.exitWindow)

    def exitWindow(self, event):
        """
        Function used to exit the CollectData window and return to MainMenu
        when an event occurs. This function should be bound to an onclick event
        on the exitName button.

        :param
        event :the event type of an item bound to this function

        Example Usage:
        //Binds left mouse click on 'exitName' button to this function
        exitName.bind("<Button-1>", self.exitWindow)
        """
        self.newWindow.destroy()

    def updateLoadLabel(self):
        print(self.loading)
        if self.loading == True:
            frame = self.frames[self.frameIndex]
            self.frameIndex += 1
            if self.frameIndex >= len(self.frames):
                self.frameIndex = 0
            try:
                self.loadLabel.configure(image=frame)
                self.newWindow.after(50, self.updateLoadLabel)
            except:
                self.frameIndex = 0
        else:
            print("done updating load label")

    def loadingLabel(self):
        # Get coordinates of buttons and remove them
        exit_info = self.exitName.place_info()
        collect_info = self.collectData.place_info()
        xval = (int(exit_info["x"]) + int(collect_info["x"])) / 2
        yval = int(exit_info["y"])
        height = int(exit_info["height"])
        width = int(exit_info["width"])
        self.exitName.destroy()
        self.collectData.destroy()

        # get the gif and animate that shit in
        self.loading = True
        self.loadLabel = Label(self.newWindow, width=100)
        self.loadLabel.place(x=xval, y=yval)
        print("Calling update load label")
        self.newWindow.after(0, self.updateLoadLabel)

    def parseThread(self):
        print("{} Starting...".format(threading.currentThread().getName()))
        p = ClassParser.ClassParser(self.s, self.subjectVal.get())
        p.deleteFormatting()
        p.parseData()
        print("{} Exiting...".format(threading.currentThread().getName()))
        threading.currentThread().exit()

    def dataCollectClick(self, event):
        """
        This function is used to update course data for a specific subject and
        term. It parses data from classes.uoregon.edu and updates the database
        with the latest course information. This function will be called when
        a bound event occurs.

        :param
        event :the event type of an item bound to this function

        Example Usage:
        //Binds left mouse click on collectData button to this function
        collectData.bind("<Button-1>", self.dataCollectClick)
        """
        self.loadingLabel()

        term = self.termVal.get()
        year = self.yearVal.get()
        t = None
        y = int(year)
        if term == "Fall":
            t = 1
        elif term == "Winter":
            y -= 1
            t = 2
        elif term == "Spring":
            y -= 1
            t = 3
        elif term == "Summer":
            y -= 1
            t = 4

        ye = str(y)
        self.s = ye + "0" + str(t)
        currentClasses = self.cm.find_by_term(self.subjectVal.get(), y, t)
        if len(currentClasses):
            self.cm.delete_sub_term(self.subjectVal.get(), self.s)

        parse_thread = threading.Thread(name="ParsingThread", target=self.parseThread)
        parse_thread.start()
        while parse_thread.isAlive():
            self.newWindow.update_idletasks()
            self.newWindow.update()
        parse_thread.join()
        print("Thread joined")

        # Remove loading wheel
        self.loadLabel.destroy()
        self.initButtons()
