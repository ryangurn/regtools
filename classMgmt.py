import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import font
from jsonPythonParser import * 

class classMgmt(tk.Tk):
    def __init__(self, master, studentName):
        self.master = master
        self.newWindow = Frame(master, bg = "#262929", height = 400, width = 810)
        self.newWindow.place(x = 0, y = 150)
        subfont= font.Font(family="Helvetica", size=26)
        courseFont = font.Font(family = "Helvetica", size = 16)
        self.courseSubjects = Listbox(self.newWindow, selectmode="browse", bg="#ffcc00", width = 6, borderwidth=2, font = subfont)
        
        #TODO: Iterate through SQL subjects, insert into this listbox accordingly
        self.courseSubjects.insert(0, "CIS")
        self.courseSubjects.insert(1, "MATH")
        self.courseSubjects.insert(2, "ENG")

        studentLabel = Label(self.newWindow, text='Student:')
        studentLabel.place(x=10,y=0, height=40, width=80)
        studentLabel.config(font=("Arial Bold", 20))
        studentLabel.config(bg="#262929", fg="#ffcc00")

        # Student Name Label (Updates)
        labl = Label(self.newWindow, text= studentName, anchor='w')
        labl.place(x=95,y=5, height=30, width=200)
        labl.config(font=("Arial Bold", 20))
        labl.config(bg="#262929", fg="#ffcc00")

        self.courseSubjects.bind("<Double-Button-1>", self.subjectClick)
        self.offeredCourses = Listbox(self.newWindow, selectmode = "browse", bg = "#ffcc00", width = 35, borderwidth = 2, font = courseFont)
        self.offeredCourses.bind("<Double-Button-1>", self.courseClick)
        self.takenClasses = Listbox(self.newWindow, selectmode = "browse", bg = "#ffcc00", width = 40, borderwidth = 2)
        self.takenClasses.bind("<Double-Button-1>", self.removeClass)
        #self.courseSubjects.pack(side = "left", fill = NONE, expand = FALSE, padx = 10, pady = 10)
        self.courseSubjects.place(x = 10, y = 50, height = 325)
        #self.offeredCourses.pack(side = "left", fill = NONE, expand = FALSE, padx = 15, pady = 10)
        self.offeredCourses.place(x = 100, y = 50, height = 325)
        #self.courseBio.pack(side = "left", fill = NONE, expand = FALSE, padx = 10, pady = 10)
        self.takenClasses.place(x = 390, y = 50, height = 325)


        goHome = Label(self.newWindow, text='Return Home')
        goHome.config(font=("Arial Bold", 13), bg="#369148", fg="#ffcc00")
        goHome.bind("<Double-Button-1>", self.goHomeClick)
        goHome.place(x = 605, y = 380, height = 15)
  
        saveData = Label(self.newWindow, text='Save Data')
        saveData.config(font=("Arial Bold", 13), bg="#369148", fg="#ffcc00")
        saveData.bind("<Double-Button-1>", self.saveDataClick)
        saveData.place(x = 505, y = 380, height = 15)


    def goHomeClick(self, event):
        #mainMenu(self.master)
        self.newWindow.destroy()
    
    def saveDataClick(self, event):
        print("Send data to SQL")

    def subjectClick(self, event):
        #TODO: will likely have to modify this as we will be importing from a sql database
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        currentSubject = value
        keys = get_keys()
        self.offeredCourses.delete(0, END)
        i = 0
        for key in keys:
            if currentSubject == get_subject(key):
                self.offeredCourses.insert(i, key)
                i += 1
            else:
                continue

    def courseClick(self, event):
        """
        courseData = []
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        currentCourse = value
        self.courseBio.delete(0, END)
        courseData.append("Instructor: " + get_sec_instructor(currentCourse, 0))
        courseData.append("Room: " + get_sec_location(currentCourse, 0))
        courseData.append("Schedule: " + get_sec_days(currentCourse, 0) + " - " + get_sec_times(currentCourse, 0))
        courseData.append("Credits: " + get_credits(currentCourse))
        courseData.append("Grading: " + get_grading(currentCourse))
        courseData.append("Notes: " + get_sec_notes(currentCourse, 0))
        for i in range(len(courseData)):
            self.courseBio.insert(i, courseData[i])
        """
        w = event.widget
        index = int(w.curselection()[0])
        currentCourse = w.get(index)
        self.takenClasses.insert(END, currentCourse)
        
    def removeClass(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        MsgBox = tk.messagebox.askquestion ('Delete Conifrmation','Are you sure you would like to delete this class', icon = 'warning')
        if MsgBox == 'yes':
            self.takenClasses.delete(index)
        