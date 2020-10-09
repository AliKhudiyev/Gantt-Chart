from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import *
import datetime
import os
import json
import numpy as np


class Step:
    def __init__(self, name=''):
        self.name = name
        self.start = None
        self.end = None
        self.duration = 0
        self.members = []

    def is_valid(self):
        if len(self.name) == 0 or self.start is None or self.end is None:
            return False
        return True

    def tell_members(self):
        members = ''
        for i, member in enumerate(self.members):
            members += member
            if i < len(self.members) - 1:
                members += ', '
        return members

    def to_json(self):
        json_str = '{'
        json_str += '"name": "' + self.name + '", '
        json_str += '"start": "' + self.start.strftime('%d/%m/%Y') + '", '
        json_str += '"end": "' + self.end.strftime('%d/%m/%Y') + '", '
        json_str += '"members": ['
        for i, member in enumerate(self.members):
            json_str += '"' + member + '"'
            if i < len(self.members) - 1:
                json_str += ', '
        json_str += ']}'

        return json_str


class Project:
    def __init__(self, title='', steps=[]):
        self.title = title
        self.steps = steps
        self.start = None
        self.end = None
        self.about = ''

        self.update()

    def is_valid(self):
        return True

    def update(self):
        if len(self.steps) > 0:
            self.start = self.steps[0].start
            self.end = self.steps[0].end

        for step in self.steps:
            if self.start > step.start:
                self.start = step.start
            if self.end < step.end:
                self.end = step.end

    def to_json(self):
        json_str = '{'
        json_str += '"title": "' + self.title + '", '
        json_str += '"steps": ['
        for i, step in enumerate(self.steps):
            json_str += step.to_json()
            if i < len(self.steps) - 1:
                json_str += ', '
        json_str += ']}'

        return json_str


def to_json(projects):
    json_str = '{"projects": ['
    for i, project in enumerate(projects):
        json_str += project.to_json()
        if i < len(projects) - 1:
            json_str += ', '
    json_str += ']}'

    return json.loads(json_str)


class ProjectFrame(LabelFrame):
    def __init__(self, master, app, width, height):
        LabelFrame.__init__(self, master, width=width, height=height)
        self.app = app
        self.mainFrame = LabelFrame(self, width=width-45, height=height)
        self.sliderFrame = LabelFrame(self, width=45, height=height)

        self.header = LabelFrame(self.mainFrame)
        self.body = LabelFrame(self.mainFrame)

        self.projects = []
        self.file_path = ''
        self.start_index = 0

        self.button_up = Button(self.sliderFrame, text='U', command=self.click_up)
        self.button_down = Button(self.sliderFrame, text='D', command=self.click_down)
        self.gui_template()

    def load_file(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            json_str = json.load(f)
        f.close()

        for project in json_str['projects']:
            prj = Project(steps=[])
            prj.title = project['title']
            for step in project['steps']:
                stp = Step()
                stp.name = step['name']
                stp.start = datetime.datetime.strptime(step['start'], '%d/%m/%Y')
                stp.end = datetime.datetime.strptime(step['end'], '%d/%m/%Y')
                for member in step['members']:
                    stp.members.append(member)
                prj.steps.append(stp)
            self.projects.append(prj)

    def save_frame(self, file_path=''):
        if len(file_path) == 0:
            file_path = self.file_path

        with open(file_path, 'w') as f:
            json.dump(to_json(self.projects), f)
        f.close()

    def click_up(self):
        if self.start_index > 0:
            self.start_index -= 1
        # self.app.update()
        self.app.projectFrame.update()
        self.app.calendarFrame.update(4, self.projects[self.start_index:])

    def click_down(self):
        if self.start_index + 1 < len(self.projects):
            self.start_index += 1
        # self.app.update()
        self.app.projectFrame.update()
        self.app.calendarFrame.update(4, self.projects[self.start_index:])

    def gui_template(self):
        self.mainFrame.grid(row=0, column=1)
        self.sliderFrame.grid(row=0, column=0)

        self.header.grid(row=0, column=0)
        self.body.grid(row=1, column=0)

        self.button_up.place(x=20, anchor='n')
        self.button_down.place(rely=0.9, y=25)

        self.grid_propagate(0)
        self.mainFrame.grid_propagate(0)
        self.sliderFrame.grid_propagate(0)

        label_projects = Label(self.header, text='Projects', bg='cyan', width=15, height=3)
        label_start = Label(self.header, text='From', bg='cyan', width=10, height=3)
        label_end = Label(self.header, text='To', bg='cyan', width=10, height=3)
        label_duration = Label(self.header, text='Duration', bg='cyan', width=10, height=3)
        label_members = Label(self.header, text='Member(s)', bg='cyan', width=10, height=3)
        label_completion = Label(self.header, text='Completed', bg='cyan', width=10, height=3)

        label_projects.grid(row=0, column=0, padx=1)
        label_start.grid(row=0, column=1, padx=1)
        label_end.grid(row=0, column=2, padx=1)
        label_duration.grid(row=0, column=3, padx=1)
        label_members.grid(row=0, column=4, padx=1)
        label_completion.grid(row=0, column=5, padx=1)

    def add(self, project):
        if project.is_valid:
            self.projects.append(project)
            self.update()

    def update(self):
        clear_frame(self.mainFrame)
        self.gui_template()

        n_row = 0
        for i, project in enumerate(self.projects):
            if i < self.start_index:
                continue
            # print('prj title:', project.title)
            label_title = Label(self.body, text=project.title, bg='yellow', width=15)
            label_title.grid(row=n_row, column=0, padx=1, pady=2)

            for step in project.steps:
                start = step.start.strftime('%d/%m/%Y')
                end = step.end.strftime('%d/%m/%Y')
                step.duration = (step.end - step.start).days
                dt = (datetime.datetime.now() - step.start).days
                completed = 0
                if step.duration > 0 and dt > 0:
                    completed = np.round(100 * dt / step.duration, decimals=0)

                label_name = Label(self.body, text=step.name, width=15)
                label_start = Label(self.body, text=start, width=10)
                label_end = Label(self.body, text=end, width=10)
                label_duration = Label(self.body, text=step.duration, width=10)
                label_members = Label(self.body, text='mems?', width=10)
                label_completion = Label(self.body, text=str(completed), width=10)

                label_name.grid(row=n_row + 1, column=0, padx=1, pady=2)
                label_start.grid(row=n_row + 1, column=1, padx=1, pady=2)
                label_end.grid(row=n_row + 1, column=2, padx=1, pady=2)
                label_duration.grid(row=n_row + 1, column=3, padx=1, pady=2)
                label_members.grid(row=n_row + 1, column=4, padx=1, pady=2)
                label_completion.grid(row=n_row + 1, column=5, padx=1, pady=2)

                n_row += 1
            n_row += 1


class CalendarFrame(LabelFrame):
    def __init__(self, master, app, width, height):
        LabelFrame.__init__(self, master, width=width, height=height)
        self.app = app
        self.mainFrame = LabelFrame(self)
        self.sliderFrame = LabelFrame(self, width=width, height=35)

        self.header = LabelFrame(self.mainFrame)
        self.body = LabelFrame(self.mainFrame)

        self.button_left = Button(self.sliderFrame, text='<', command=self.click_left)
        self.button_right = Button(self.sliderFrame, text='>', command=self.click_right)

        self.week_pad = 1
        self.n_week = 4
        self.calendar_start = datetime.datetime.now()
        self.weekdays = ['M', 'T', 'W', 'Th', 'F', 'St', 'S']

        self.sliderFrame.grid(row=0, column=0)
        self.mainFrame.grid(row=1, column=0)
        self.sliderFrame.grid_propagate(0)

    def click_left(self):
        self.calendar_start -= datetime.timedelta(7)
        self.update(self.n_week, self.app.projectFrame.projects[self.app.projectFrame.start_index:], self.calendar_start)

    def click_right(self):
        self.calendar_start += datetime.timedelta(7)
        self.update(self.n_week, self.app.projectFrame.projects[self.app.projectFrame.start_index:], self.calendar_start)

    def date_index(self, date):
        dt = (date - self.calendar_start).days
        n = 0

        while n < dt:
            n += 1
            if (n + 1) % 8 == 0:
                dt += 1
        return n

    def mark_date(self, row_index, date, color):
        label = Label(self.body, width=1, bg=color)
        label.grid(row=row_index, column=self.date_index(date))

    def display_date(self, projects):
        now = datetime.datetime.now()
        n = self.date_index(now)
        label = Label(self.header, text=self.weekdays[now.weekday()], bg='red')
        label.grid(row=0, column=n)

    def update_calendar_start(self, projects):
        now = datetime.datetime.now()
        self.calendar_start = datetime.datetime(year=now.year, month=now.month, day=now.day)

        for project in projects:
            project.update()
            if self.calendar_start > project.start:
                self.calendar_start = project.start
        self.calendar_start -= datetime.timedelta(self.calendar_start.weekday())
        print('Calendar starts in', self.calendar_start)

    def update(self, n_week=1, projects=[], start_date=None):
        clear_frame(self.header)
        # clear_frame(self.body)
        self.body.destroy()
        self.body = LabelFrame(self.mainFrame)

        self.button_left.place(x=10)
        self.button_right.place(relx=0.9)

        self.n_week = n_week
        self.header.grid(row=0, column=0)
        self.body.grid(row=1, column=0)
        self.grid_propagate(0)

        if start_date is None:
            self.update_calendar_start(projects)

        for i in range(n_week):
            for j in range(7):
                label = Label(self.header, text=self.weekdays[j], width=1)
                label.grid(row=0, column=8 * i + j, padx=2)
            label = Label(self.header, width=self.week_pad)
            label.grid(row=0, column=8 * (i + 1) - 1)

        n_row = 0
        for project in projects:
            for i in range(n_week):
                for j in range(7):
                    label = Label(self.body, width=1, bg='yellow')
                    label.grid(row=n_row, column=8 * i + j, padx=2, pady=2)
                label = Label(self.body, width=self.week_pad)
                label.grid(row=n_row, column=8 * (i + 1) - 1)

            for step in project.steps:
                for i in range(n_week):
                    for j in range(7):
                        label = Label(self.body, width=1, bg='orange')
                        label.grid(row=n_row + 1, column=8 * i + j, padx=2, pady=2)
                    label = Label(self.body, width=self.week_pad)
                    label.grid(row=n_row + 1, column=8 * (i + 1) - 1)
                n_row += 1
            n_row += 1

        n_row = 0
        calendar_end = self.calendar_start + datetime.timedelta(7 * self.n_week)
        for project in projects:
            dt = (project.end - project.start).days

            for i in range(dt):
                if project.start + datetime.timedelta(i) >= calendar_end:
                    break
                self.mark_date(n_row, project.start + datetime.timedelta(i), 'purple')

            for step in project.steps:
                for i in range(step.duration):
                    if step.start + datetime.timedelta(i) >= calendar_end:
                        break
                    self.mark_date(n_row + 1, step.start + datetime.timedelta(i), 'blue')
                n_row += 1
            n_row += 1
        self.display_date(projects)


class ProjectFormWindow(Toplevel):
    def __init__(self, master, app, option=0):
        Toplevel.__init__(self, master)
        self.app = app
        self.option = option
        self.title('New project')

        self.entry_title = Entry(self)
        self.entry_name = Entry(self)
        self.entry_members = Entry(self)
        self.entry_about = Entry(self)
        self.button_start = None
        self.button_end = None
        self.calendar = None
        self.calendarWindow = None

        self.step = Step()
        self.project = Project(steps=[])

    def click_add(self):
        self.step.name = self.entry_name.get()
        self.step.duration = (self.step.end - self.step.start).days
        # print('Duration:', self.step.duration)
        # print('Step interval:', self.step.start, '-', self.step.end)
        self.step.members = self.entry_members.get()

        if self.step.is_valid():
            # print(' --- Appended step')
            self.project.steps.append(self.step)
            self.step = Step()
            # print(' ...# of steps:', len(self.project.steps))

        self.entry_name.delete(0, END)
        self.entry_members.delete(0, END)
        self.entry_about.delete(0, END)
        self.entry_name.delete(0, END)

    def click_save(self):
        title = self.entry_title.get()
        if len(title) > 0:
            self.project.title = title
            self.project.about = self.entry_about.get()
        self.project.update()
        self.app.projectFrame.projects.append(self.project)
        print('Date interval:', self.project.start, self.project.end)
        self.destroy()
        self.app.update()

    def set_step_date(self, date_type):
        picked_date = self.calendar.selection_get()
        date = datetime.datetime(year=picked_date.year, month=picked_date.month, day=picked_date.day)

        if date_type == 'start':
            self.step.start = date
            self.button_start.configure(text=date.strftime('%d/%m/%Y'))
        else:
            self.step.end = date
            self.button_end.configure(text=date.strftime('%d/%m/%Y'))
        self.calendarWindow.destroy()

    def click_datepicker(self, date_type):
        self.calendarWindow = Toplevel(self)
        today = datetime.datetime.now()
        self.calendar = Calendar(self.calendarWindow, font="Arial 14", selectmode='day', locale='en_US',
                                 disabledforeground='red',
                                 cursor="hand1", year=today.year, month=today.month, day=today.day)
        self.calendar.pack(fill="both", expand=True)
        ttk.Button(self.calendarWindow, text="Ok", command=lambda: self.set_step_date(date_type)).pack()

    def run(self):
        label_title = Label(self, text='Project Title')
        label_steps = Label(self, text='Steps')
        label_name = Label(self, text='Name')
        label_start = Label(self, text='From')
        label_end = Label(self, text='To')
        label_members = Label(self, text='Memebers')
        label_about = Label(self, text='About')

        button_add = Button(self, text='Add', command=self.click_add)
        self.button_start = Button(self, text='Choose a date', command=lambda: self.click_datepicker(date_type='start'))
        self.button_end = Button(self, text='Choose a date', command=lambda: self.click_datepicker(date_type='end'))
        button_save = Button(self, text='Save', command=self.click_save)

        label_title.grid(row=0, column=0)
        label_steps.grid(row=1, column=0)
        label_name.grid(row=2, column=0)
        label_start.grid(row=3, column=0)
        label_end.grid(row=3, column=2)
        label_members.grid(row=4, column=0)
        label_about.grid(row=5, column=0)

        self.entry_title.grid(row=0, column=1)
        self.entry_name.grid(row=2, column=1)
        self.entry_members.grid(row=4, column=1)
        self.entry_about.grid(row=5, column=1)

        button_add.grid(row=1, column=1)
        self.button_start.grid(row=3, column=1)
        self.button_end.grid(row=3, column=3)
        button_save.grid(row=6 + self.option, column=0, columnspan=4)

        if self.option == 1:
            label_edit = Label(self, text='ID')
            entry_edit = Entry(self)

            label_edit.grid(row=6, column=0)
            entry_edit.grid(row=6, column=1)
            # TO DO


class ProjectRemoveWindow(Toplevel):
    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.title('Remove project')
        self.app = app

        self.entry_index = Entry(self)

    def click_remove(self):
        index = int(self.entry_index.get())
        if 0 <= index < len(self.app.projectFrame.projects):
            self.app.projectFrame.projects.remove(self.app.projectFrame.projects[index])
        self.app.update()
        self.destroy()

    def run(self):
        label_index = Label(self, text='ID')
        button_remove = Button(self, text='Remove', command=self.click_remove)

        label_index.grid(row=0, column=0)
        self.entry_index.grid(row=0, column=1)
        button_remove.grid(row=1, column=0, columnspan=2)


class MenuBar(Menu):
    def __init__(self, master, app):
        Menu.__init__(self, master)
        self.master = master
        self.app = app

    def click_new(self):
        pass

    def click_open(self):
        pass

    def click_save(self):
        pass

    def click_save_as(self):
        pass

    def click_add(self):
        pass

    def click_edit(self):
        pass

    def click_remove(self):
        pass

    def gui_new(self):
        pass

    def gui_open(self):
        file_type = [('Gantt Chart', '*.json')]
        file_path = filedialog.askopenfilename(parent=self.master,
                                               initialdir=os.getcwd(),
                                               title="Please select a file:",
                                               filetypes=file_type)
        print('Open', file_path)
        self.app.projectFrame.projects = []
        self.app.projectFrame.load_file(file_path)
        self.app.update()

    def gui_save(self):
        print(to_json(self.app.projectFrame.projects))

    def gui_save_as(self):
        file_type = [('Gantt Chart', '*.json')]
        file_path = filedialog.asksaveasfilename(parent=self.master,
                                                 initialdir=os.getcwd(),
                                                 title="Please select a file name for saving:",
                                                 filetypes=file_type)
        print('Save as', file_path)
        self.app.projectFrame.save_frame(file_path)

    def gui_add(self):
        print('Adding...')
        form = ProjectFormWindow(self.master, self.app)
        form.run()

    def gui_edit(self):
        print('Editing...')
        form = ProjectFormWindow(self.master, self.app, 1)
        form.run()

    def gui_remove(self):
        print('Removing...')
        form = ProjectRemoveWindow(self.master, self.app)
        form.run()

    def run(self):
        menu_file = Menu(self)
        menu_file.add_command(label='New', command=self.gui_new)
        menu_file.add_command(label='Open', command=self.gui_open)
        menu_file.add_command(label='Save', command=self.gui_save)
        menu_file.add_command(label='Save as', command=self.gui_save_as)
        menu_file.add_separator()
        menu_file.add_command(label='Exit', command=self.master.destroy)

        self.add_cascade(label='File', menu=menu_file)

        menu_project = Menu(self)
        menu_project.add_command(label='Add', command=self.gui_add)
        menu_project.add_command(label='Edit', command=self.gui_edit)
        menu_project.add_command(label='Remove', command=self.gui_remove)

        self.add_cascade(label='Project', menu=menu_project)

        menu_tools = Menu(self)
        menu_tools.add_command(label='Search')
        menu_tools.add_command(label='Zoom in')
        menu_tools.add_command(label='Zoom out')

        self.add_cascade(label='Tools', menu=menu_tools)

        menu_settings = Menu(self)
        menu_settings.add_command(label='Preferences')

        self.add_cascade(label='Settings', menu=menu_settings)

        self.master.config(menu=self)


def clear_frame(window):
    if window is not None:
        widget_list = window.winfo_children()

        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
        for item in widget_list:
            item.grid_forget()


class App:
    def __init__(self):
        self.root = Tk()
        self.root.title('Gantt Chart')
        self.menuBar = MenuBar(self.root, self)
        self.frame = LabelFrame(self.root)
        # self.frame1 = LabelFrame(self.frame)
        # self.frame2 = LabelFrame(self.frame)
        self.projectFrame = ProjectFrame(self.frame, self, width=620, height=550)
        self.calendarFrame = CalendarFrame(self.frame, self, width=570, height=550)

        # self.frame1.grid(row=0, column=0)
        # self.frame2.grid(row=0, column=1)
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

    def update(self):
        self.frame.grid(row=0, column=0)
        self.projectFrame.grid(row=0, column=0)
        self.calendarFrame.grid(row=0, column=1)
        # print('Updating app:', 4, len(self.projectFrame.projects))
        self.projectFrame.update()
        self.calendarFrame.update(4, self.projectFrame.projects[self.projectFrame.start_index:])

    def run(self):
        self.update()

        self.menuBar.run()
        self.root.mainloop()


app = App()
app.run()
