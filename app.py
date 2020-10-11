from tkinter import *
import datetime
from project_frame import *
from calendar_frame import *
from menu import *


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title('Gantt Chart')
        self.root.resizable(0, 0)
        self.menuBar = MenuBar(self.root, self)
        self.frame = LabelFrame(self.root)
        # self.frame1 = LabelFrame(self.frame)
        # self.frame2 = LabelFrame(self.frame)
        self.projectFrame = ProjectFrame(self.frame, self, width=620, height=540)
        self.calendarFrame = CalendarFrame(self.frame, self, width=570, height=540)

        self.frame.grid(row=0, column=0)
        self.projectFrame.grid(row=0, column=0)
        self.calendarFrame.grid(row=0, column=1)
        # ==================
        self.projects = []

        s1 = Step()
        s1.name = 's1'
        s1.start = datetime.datetime.strptime('1.10.2020', '%d.%m.%Y')
        s1.end = datetime.datetime.strptime('10.10.2020', '%d.%m.%Y')
        s1.members = ['Joe, Vito']
        s1.about = ''

        s2 = Step()
        s2.name = 's2'
        s2.start = datetime.datetime.strptime('5.10.2020', '%d.%m.%Y')
        s2.end = datetime.datetime.strptime('9.10.2020', '%d.%m.%Y')
        s2.members = ['Jane, Vito']
        s2.about = ''

        prj1 = Project('prj1', [s1, s2, s2])
        prj2 = Project('prj2', [s1, s2])

        self.projects.append(prj1)
        self.projects.append(prj2)

        self.projectFrame.projects = self.projects
        # ================

    @staticmethod
    def new_app(self):
        return App()

    def update(self):
        self.projectFrame.update()
        self.calendarFrame.update(4, self.projectFrame.projects[self.projectFrame.start_index:])

    def run(self):
        self.update()

        self.menuBar.run()
        self.root.mainloop()
