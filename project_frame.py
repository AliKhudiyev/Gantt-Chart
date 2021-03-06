from tkinter import *
from tkinter import ttk
import datetime
from tkcalendar import *
import numpy as np
import copy
from project import *


def clear_frame(window):
    if window is not None:
        widget_list = window.winfo_children()

        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
        for item in widget_list:
            item.grid_forget()


def reset_frame(window):
    if window is not None:
        widget_list = window.winfo_children()

        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
        for item in widget_list:
            item.grid_remove()


class ProjectFrame(LabelFrame):
    def __init__(self, master, app, width, height):
        LabelFrame.__init__(self, master, width=width, height=height)
        self.app = app
        self.mainFrame = LabelFrame(self, width=width - 45, height=height)
        self.sliderFrame = LabelFrame(self, width=45, height=height)

        self.header = LabelFrame(self.mainFrame)
        self.body = LabelFrame(self.mainFrame, width=width - 45, height=height - 65)

        self.projects = []
        self.file_path = ''
        self.start_index = 0
        self.time_format = '%d/%m/%Y'

        self.button_up = Button(self.sliderFrame, text=u'\u2191', command=self.click_up)
        self.button_down = Button(self.sliderFrame, text=u'\u2193', command=self.click_down)
        self.gui_template()

    def load_file(self, file_path):
        if len(file_path) == 0:
            return 1

        self.projects = list()
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
                stp.start = datetime.datetime.strptime(step['start'], self.time_format)
                stp.end = datetime.datetime.strptime(step['end'], self.time_format)
                for member in step['members']:
                    stp.members.append(member)
                prj.steps.append(stp)
            # print('loaded:', project['description'])
            # print('stringtitized:', str(project['description']))
            prj.about = str(project['description'])
            self.projects.append(prj)

    def save_frame(self, file_path=''):
        if len(file_path) == 0:
            file_path = self.file_path

        with open(file_path, 'w') as f:
            json.dump(to_json(self.projects), f)
        f.close()

    def expand_project(self, index):
        win = Toplevel(self)
        win.title('Project description')
        win.minsize(100, 100)
        project = self.projects[index]
        steps = ''

        for i, step in enumerate(project.steps):
            steps += str(i+1) + '. ' + step.name + '\n'

        label_title = Label(win, text=project.title, bg='purple')
        label_about = Label(win, text=project.about, bg='yellow')
        label_steps = Label(win, text=steps[:-1], bg='orange')
        label_members = Label(win, text=project.tell_members(), bg='cyan')

        label_title.pack()
        label_about.pack()
        label_steps.pack()
        label_members.pack()

    def click_up(self):
        if self.start_index > 0:
            self.start_index -= 1
        self.app.update()

    def click_down(self):
        if self.start_index + 1 < len(self.projects):
            self.start_index += 1
        self.app.update()

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
        self.body.grid_propagate(0)

        label_projects = Label(self.header, text='Projects', bg='cyan', width=15, height=3)
        label_start = Label(self.header, text='From', bg='cyan', width=10, height=3)
        label_end = Label(self.header, text='To', bg='cyan', width=10, height=3)
        label_duration = Label(self.header, text='Duration\n(days)', bg='cyan', width=10, height=3)
        label_members = Label(self.header, text='Member(s)', bg='cyan', width=10, height=3)
        label_completion = Label(self.header, text='Completed\n(%)', bg='cyan', width=10, height=3)

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
            if n_row > 17:
                break

            project.update()
            duration = (project.end - project.start).days
            dt = (datetime.datetime.now() - project.start).days
            completed = 0
            if dt > 0:
                completed = int(np.round(100 * dt / duration, decimals=0))
            if completed > 100:
                completed = 100

            label_title = Label(self.body, text=str(i) + '. ' + project.title, bg='yellow', width=15)
            label_start = Label(self.body, text=project.start.strftime(self.time_format), bg='yellow', width=10)
            label_end = Label(self.body, text=project.end.strftime(self.time_format), bg='yellow', width=10)
            label_duration = Label(self.body, text=str(duration), bg='yellow', width=10)
            label_members = Label(self.body, text=project.tell_members(), bg='yellow', width=10)
            label_completion = Label(self.body, text=str(completed), bg='yellow', width=10)

            label_title.grid(row=n_row, column=0, padx=1, pady=2)
            label_start.grid(row=n_row, column=1, padx=1, pady=2)
            label_end.grid(row=n_row, column=2, padx=1, pady=2)
            label_duration.grid(row=n_row, column=3, padx=1, pady=2)
            label_members.grid(row=n_row, column=4, padx=1, pady=2)
            label_completion.grid(row=n_row, column=5, padx=1, pady=2)

            label_title.bind('<Button-1>', lambda e, index=i: self.expand_project(index))
            label_title.bind('<Enter>',
                             lambda e, label=label_title: label.config(bg='purple'))
            label_title.bind('<Leave>',
                             lambda e, label=label_title: label.config(bg='yellow'))

            for step in project.steps:
                start = step.start.strftime(self.time_format)
                end = step.end.strftime(self.time_format)
                step.duration = (step.end - step.start).days
                dt = (datetime.datetime.now() - step.start).days
                completed = 0
                if step.duration > 0 and dt > 0:
                    completed = int(np.round(100 * dt / step.duration, decimals=0))
                if completed > 100:
                    completed = 100

                label_name = Label(self.body, text=step.name, width=15)
                label_start = Label(self.body, text=start, width=10)
                label_end = Label(self.body, text=end, width=10)
                label_duration = Label(self.body, text=step.duration, width=10)
                label_members = Label(self.body, text=step.tell_members(), width=10)
                label_completion = Label(self.body, text=str(completed), width=10)

                label_name.grid(row=n_row + 1, column=0, padx=1, pady=2)
                label_start.grid(row=n_row + 1, column=1, padx=1, pady=2)
                label_end.grid(row=n_row + 1, column=2, padx=1, pady=2)
                label_duration.grid(row=n_row + 1, column=3, padx=1, pady=2)
                label_members.grid(row=n_row + 1, column=4, padx=1, pady=2)
                label_completion.grid(row=n_row + 1, column=5, padx=1, pady=2)

                n_row += 1
            n_row += 1


class ProjectFormWindow(Toplevel):
    def __init__(self, master, app, option=0):
        Toplevel.__init__(self, master)
        self.app = app
        self.option = option
        self.title('New project')

        self.entry_title = Entry(self)
        self.entry_name = Entry(self)
        self.entry_members = Entry(self)
        self.entry_about = Text(self, width=30, height=5)
        self.button_start = None
        self.button_end = None
        self.calendar = None
        self.calendarWindow = None

        self.step = Step()
        self.project = Project(steps=[])

    def click_add(self):
        self.step.name = self.entry_name.get()
        if self.step.start is not None and self.step.end is not None:
            self.step.duration = (self.step.end - self.step.start).days
        self.step.members.append(self.entry_members.get())

        if self.step.is_valid():
            self.project.steps.append(self.step)
            self.step = Step()

        self.entry_name.delete(0, END)
        self.entry_members.delete(0, END)
        self.entry_name.delete(0, END)

        self.button_start.configure(text='Choose a date')
        self.button_end.configure(text='Choose a date')

    def click_save(self):
        title = self.entry_title.get()
        if len(title) > 0:
            self.project.title = title
            self.project.about = self.entry_about.get('1.0', END)
        self.project.update()
        if self.project.is_valid():
            self.app.projectFrame.projects.append(self.project)
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


class ProjectEditWindow(Toplevel):
    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.title('Edit project')
        self.app = app

        self.entry_index = Entry(self)

        self.entry_title = Entry(self)
        self.entry_name = Entry(self)
        self.button_start = Button(self, command=lambda: self.click_datepicker('start'))
        self.button_end = Button(self, command=lambda: self.click_datepicker('end'))
        self.entry_members = Entry(self)
        self.entry_about = Text(self, width=30, height=5)

        self.calendarWindow = None
        self.calendar = None

        self.start_date = None
        self.end_date = None

        self.project_index = 0
        self.step_index = 0

    def set_step_date(self, date_type):
        picked_date = self.calendar.selection_get()
        date = datetime.datetime(year=picked_date.year, month=picked_date.month, day=picked_date.day)

        if date_type == 'start':
            # self.app.projectFrame.projects[self.project_index].steps[self.step_index].start = date
            self.start_date = date
            self.button_start.configure(text=date.strftime('%d/%m/%Y'))
        else:
            # self.app.projectFrame.projects[self.project_index].steps[self.step_index].end = date
            self.end_date = date
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

    def click_left(self):
        if self.step_index > 0:
            self.step_index -= 1
        self.click_goto()

    def click_right(self):
        if self.step_index + 1 < len(self.app.projectFrame.projects[self.project_index].steps):
            self.step_index += 1
        self.click_goto()

    def click_edit(self):
        project = self.app.projectFrame.projects[self.project_index]
        project.title = self.entry_title.get()
        project.steps[self.step_index].name = self.entry_name.get()
        project.steps[self.step_index].start = self.start_date
        project.steps[self.step_index].end = self.end_date
        project.steps[self.step_index].members = list()  # Re-write this!
        project.steps[self.step_index].members.append(self.entry_members.get())  # ...
        project.about = self.entry_about.get('1.0', END)
        self.app.projectFrame.projects[self.project_index] = project

    def click_add(self):
        self.app.projectFrame.projects[self.project_index].steps.insert(self.step_index + 1, Step())

    def click_remove(self):
        step = self.app.projectFrame.projects[self.project_index].steps[self.step_index]
        self.app.projectFrame.projects[self.project_index].steps.remove(step)

    def click_replace(self):
        size = len(self.app.projectFrame.projects[self.project_index].steps)
        tmp = copy.deepcopy(self.app.projectFrame.projects[self.project_index].steps[self.step_index])
        tmp2 = self.app.projectFrame.projects[self.project_index].steps[(self.step_index + 1) % size]
        self.app.projectFrame.projects[self.project_index].steps[self.step_index] = tmp2
        self.app.projectFrame.projects[self.project_index].steps[(self.step_index + 1) % size] = tmp

    def click_save(self):
        self.destroy()
        self.app.update()

    def click_goto(self):
        ans = self.entry_index.get()
        if not ans.isnumeric() or int(ans) >= len(self.app.projectFrame.projects):
            self.destroy()
            return 0

        self.project_index = int(ans)
        self.entry_title.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_members.delete(0, END)
        self.entry_about.delete('1.0', END)

        label_title = Label(self, text='Title')
        label_steps = Label(self, text='Steps')
        label_name = Label(self, text='Name')
        label_start = Label(self, text='From')
        label_end = Label(self, text='To')
        label_members = Label(self, text='Members')
        label_about = Label(self, text='Description')

        button_left = Button(self, text=u'\u2190', command=self.click_left)
        button_right = Button(self, text=u'\u2192', command=self.click_right)
        button_edit = Button(self, text='Edit', command=self.click_edit)
        button_add = Button(self, text='Add', command=self.click_add)
        button_remove = Button(self, text='Remove', command=self.click_remove)
        button_replace = Button(self, text='Replace', command=self.click_replace)
        button_save = Button(self, text='Save', command=self.click_save)

        label_title.grid(row=0, column=0)
        label_steps.grid(row=1, column=1)
        label_name.grid(row=3, column=0)
        label_start.grid(row=4, column=0)
        label_end.grid(row=4, column=2)
        label_members.grid(row=5, column=0)
        label_about.grid(row=6, column=0)

        self.entry_title.grid(row=0, column=1)
        self.entry_name.grid(row=3, column=1)
        self.button_start.grid(row=4, column=1)
        self.button_end.grid(row=4, column=3)
        self.entry_members.grid(row=5, column=1)
        self.entry_about.grid(row=6, column=1)

        button_left.grid(row=1, column=0)
        button_right.grid(row=1, column=2)
        button_edit.grid(row=2, column=0)
        button_add.grid(row=2, column=1)
        button_remove.grid(row=2, column=2)
        button_replace.grid(row=2, column=3)
        button_save.grid(row=7, column=0, columnspan=4)

        members = self.app.projectFrame.projects[self.project_index].steps[self.step_index].tell_members()
        self.entry_title.insert(0, self.app.projectFrame.projects[self.project_index].title)
        self.entry_name.insert(0, self.app.projectFrame.projects[self.project_index].steps[self.step_index].name)
        self.entry_members.insert(0, members)
        for i, line in enumerate(self.app.projectFrame.projects[self.project_index].about.split('\n')):
            self.entry_about.insert(END, line + '\n')
        # self.entry_about.insert('1.0', self.app.projectFrame.projects[self.project_index].about)

        self.start_date = self.app.projectFrame.projects[self.project_index].steps[self.step_index].start
        self.end_date = self.app.projectFrame.projects[self.project_index].steps[self.step_index].end

        if self.start_date is not None and self.end_date is not None:
            self.button_start.configure(text=self.start_date.strftime('%d.%m.%Y'))
            self.button_end.configure(text=self.end_date.strftime('%d.%m.%Y'))
        else:
            self.button_start.configure(text='Choose a date')
            self.button_end.configure(text='Choose a date')

    def gui_edit(self):
        clear_frame(self)
        self.click_goto()

    def run(self):
        label_index = Label(self, text='ID')
        button_index = Button(self, text='Go to', command=self.gui_edit)

        label_index.grid(row=0, column=0)
        self.entry_index.grid(row=0, column=1)
        button_index.grid(row=1, column=0, columnspan=2)


class ProjectRemoveWindow(Toplevel):
    def __init__(self, master, app):
        Toplevel.__init__(self, master)
        self.title('Remove project')
        self.app = app

        self.entry_index = Entry(self)

    def click_remove(self):
        ans = self.entry_index.get()
        if ans.isnumeric():
            index = int(ans)
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
