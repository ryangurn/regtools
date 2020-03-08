"""

ClassInfo.py is is the graphics modules dedicated to the setup and display of
the class information window. It also handles user interaction with the window.

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
from tkinter import font
from tkinter.ttk import Notebook, Entry
import StudentModel
import StudentClassModel
import ClassModel
import json


class classInfo(tk.Tk):
    def __init__(self, master, db_file, className, class_id):
        """
        Initializer for the MainMenu window. This function requires the name
        of the database to connect and interact with. It also requires the
        master window from tkinter to interface with. It also needs the class
        name so that it can get info on that class from the database.

        :param
        master :tkinter.Tk
        db_file :str
        className :str
        class_id :str

        Example Usage:

        """
        self.db = db_file
        self.master = master

        self._lightGrey = "#b8b8b8"
        self._backgroundColor = "#323232"
        self._grey = "#323232"
        self._darkGrey = "#282929"
        self._green = "#369148"
        self._yellow = "#ffcc00"
        self._button = "<Button-1>"

        self.window = Frame(master, bg=self._darkGrey, height=800, width=800)
        self.window.place(x=0, y=0)

        self.windowTop = Frame(self.window, bg="#323232", height=125, width=800)
        self.windowTop.place(x=0, y=0)
        # Display class name on top
        labelWidth = 200
        if len(className) > 12:
            labelWidth = 500

        cm = ClassModel.ClassModel(self.db)
        self.classRecord = cm.find_by('id', class_id)[0]
        # print(self.classRecord)
        self.sections = json.loads(self.classRecord[11])
        # print(self.sections)

        roadMapLabel = Label(self.windowTop, text=className, background="#323232",
                             fg="#ffcc00")
        roadMapLabel.place(x=0, y=5, height=115, width=labelWidth)
        roadMapLabel.config(font=("Helvetica", 44))

        # UO Logo
        logoUO = PhotoImage(file="./img/UOicon.gif")
        labelUO = Label(self.windowTop, image=logoUO, borderwidth=0)
        labelUO.image = logoUO
        labelUO.place(x=670, y=4)

        # Grey Lines that hide the white lines on the logo
        greyLine = Label(self.windowTop, text="", background=self._grey)
        greyLine.place(x=0, y=110, height=8, width=800)
        greyLineTop = Label(self.windowTop, text="", background=self._grey)
        greyLineTop.place(x=0, y=3, height=8, width=800)
        greyLineLeft = Label(self.windowTop, text="", background=self._grey)
        greyLineLeft.place(x=665, y=0, height=120, width=8)
        greyLineRight = Label(self.windowTop, text="", background=self._grey)
        greyLineRight.place(x=785, y=0, height=120, width=8)

        greenLine = Label(self.windowTop, text="", background=self._green)
        greenLine.place(x=0, y=120, height=8, width=800)

        # details box is where all of the statistics information will go
        detailsBox = Text(self.window, wrap=WORD, background=self._grey, selectbackground=self._green, fg="#e6e6e6")
        detailsBox.place(x=20, y=195, height=285, width=760)
        detailsBox.config(font=("Arial", 14))

        # setup the scrolling mechanic for the details box
        # scrollbar = Scrollbar(detailsBox)
        # scrollbar.pack(side=BOTTOM, fill=X)

        # use the scrollbar
        # detailsBox.config(xscrollcommand=scrollbar.set)
        # scrollbar.config(command=detailsBox.xview)

        # detailsBox.insert(END, "hi")
        # detailsBox.insert(END, "\t\thi")

        # get the description
        description = []
        prereqs = []
        locations = []
        for item in self.sections:
            if item['description'] != "" and (item['type'] == "" or item['type'] == "Lecture"):
                description.append(item['description'])
            if item['prereqs'] != "":
                prereqs.append(item['prereqs'])
            if item['location'] != "":
                locations.append(item['location'])

        # insert the description, prereqs, and locations
        # detailsBox.insert("1.0", "Description: " + "\n".join(description))
        detailsBox.insert("1.0", "Description: " + "\n".join(description))
        print(description, prereqs, locations)


        returnButton = Label(self.window, text='Return')
        returnButton.config(font=("Arial Bold", 18), bg=self._green, fg=self._yellow)
        returnButton.place(x=600, y=540, height=30, width=140)
        returnButton.bind(self._button, self.returnClick)

    def returnClick(self, event):
        """
        DESC

        :param

        Example Usage:

        """
        self.windowTop.destroy()
        self.window.destroy()
