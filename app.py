from tkinter import *
import datetime
from project import *
import json


def clear_window(window):
    if window is not None:
        widget_list = window.winfo_children()

        for item in widget_list:
            if item.winfo_children():
                widget_list.extend(item.winfo_children())
        for item in widget_list:
            item.grid_forget()


def exit_window(window):
    if window is not None:
        window.destroy()


class Application:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("200x200+30+30")
        self.root.title('Gantt Chart')
        self.frame_template = LabelFrame(self.root, width=800, height=450)
        self.frame_project = LabelFrame(self.frame_template)
        self.frame_calendar = LabelFrame(self.root, width=620, height=450)
        self.frame_buttons = LabelFrame(self.root)
        self.canvas_calendar = Canvas(self.frame_calendar, width=620, height=450)

        self.projects = []
        self.file_path = ''

        self.win_add_project = None
        self.win_remove_project = None
        self.win_save = None
        self.win_open = None
        self.as_new = True
        self.week = 1
        self.calendar_start = datetime.datetime.strptime('01.10.2020', '%d.%m.%Y')
        self.calendar_span_weeks = 4
        self.n_row = 0

    def refresh_project(self):
        clear_window(self.frame_project)
        self.frame_project.grid(row=1, column=1, columnspan=7)
        # self.frame_project.grid_propagate(0)
        n_row = 0
        for i, project in enumerate(self.projects):
            if i < self.n_row:
                continue

            label_title = Label(self.frame_project, text=str(i) + '. ' + project.name, width=15,
                                bg='yellow')
            label_title.grid(row=n_row, column=0)
            # print('nrow:', n_row)
            n_row += 1
            # print('prj:', project.name)
            for j, step in enumerate(project.steps):
                # print(' > step:', j, 'row #:', n_row+1)
                completion = 0
                step.duration = (datetime.datetime.strptime(step.end, '%d.%m.%Y') -
                                 datetime.datetime.strptime(step.start, '%d.%m.%Y')).days
                dt = (datetime.datetime.now() - datetime.datetime.strptime(step.start, '%d.%m.%Y')).days
                if 0 <= dt < step.duration:
                    completion = 100 * dt/step.duration
                elif dt >= step.duration:
                    completion = 100
                label_step = Label(self.frame_project, text=step.name, width=15)
                label_start = Label(self.frame_project, text=step.start, width=15)
                label_end = Label(self.frame_project, text=step.end, width=15)
                label_duration = Label(self.frame_project, text=str(step.duration), width=15)
                label_members = Label(self.frame_project, text=step.tell_members(), width=15)
                label_complete = Label(self.frame_project, text=str(completion), width=15)

                label_step.grid(row=n_row, column=0)
                label_start.grid(row=n_row, column=1)
                label_end.grid(row=n_row, column=2)
                label_duration.grid(row=n_row, column=3)
                label_members.grid(row=n_row, column=4)
                label_complete.grid(row=n_row, column=5)

                n_row += 1
        self.refresh_calendar()

    def refresh_calendar(self):
        # TO DO
        # clear_window(self.frame_calendar)
        self.canvas_calendar.delete('all')
        self.frame_calendar.grid(row=1, column=2)
        # self.canvas_calendar.grid_propagate(0)
        self.canvas_calendar.grid(row=0, column=0)
        self.canvas_calendar.create_line(0, 2, 620, 2, fill='purple')
        self.canvas_calendar.create_line(0, 35, 620, 35)

        for i in range(4):
            self.canvas_calendar.create_text(154*i+75, 10, text='Week'+str(self.week+i))
            self.canvas_calendar.create_text(154*i+10, 25, text='M')
            self.canvas_calendar.create_text(154*i+32, 25, text='T')
            self.canvas_calendar.create_text(154*i+54, 25, text='W')
            self.canvas_calendar.create_text(154*i+76, 25, text='Th')
            self.canvas_calendar.create_text(154*i+98, 25, text='F')
            self.canvas_calendar.create_text(154*i+120, 25, text='St')
            self.canvas_calendar.create_text(154*i+142, 25, text='S')
            self.canvas_calendar.create_line(154*i+155, 0, 154*i+155, 194)

        total_row = len(self.projects)
        for project in self.projects:
            total_row += len(project.steps)
        # print('total row:', total_row)

        for i in range(28):
            for j in range(total_row):
                self.canvas_calendar.create_rectangle(22*i, 40+22*j, 22+22*i, 62+22*j, fill='orange')

        n_row = 0
        for n, project in enumerate(self.projects):
            if n < self.n_row:
                continue
            n_row += 1

            for step in project.steps:
                for i in range(step.duration):
                    start = datetime.datetime.strptime(step.start, '%d.%m.%Y')
                    x = (start - self.calendar_start).days + i
                    y = n_row
                    if x < 0:
                        continue
                    self.canvas_calendar.create_rectangle(22*x+5, 40+22*y+5, 22*x+22-3, 62+22*y-3, fill='blue')
                n_row += 1
        n = (datetime.datetime.now() - self.calendar_start).days
        if n >= 0:
            self.canvas_calendar.create_line(22*n, 0, 22*n, 625, fill='green', width=2)

    def click_open(self, file_path):
        self.as_new = False
        self.file_path = file_path
        self.root.geometry('1450x500')

        json_string = ''
        with open(file_path+'.json', 'r') as f:
            json_string = json.load(f)
        f.close()

        for project in json_string['projects']:
            prj = Project('', [])
            prj.name = project['title']
            for step in project['steps']:
                s = Step()
                s.name = step['name']
                s.start = step['start']
                s.end = step['end']
                for member in step['members']:
                    s.members.append(member)
                prj.steps.append(s)
            self.projects.append(prj)

        self.win_open.destroy()
        clear_window(self.root)
        self.gui_chart()

    def click_new(self):
        self.as_new = True
        clear_window(self.root)
        self.root.geometry('1450x500')
        self.gui_chart()

    def click_add_project(self, name_entry, start_entry, end_entry, duration_entry, members_entry):
        step = Step()
        step.name = name_entry.get()
        step.start = start_entry.get()
        step.end = end_entry.get()
        step.duration = duration_entry.get()
        step.members = members_entry.get()

        name_entry.delete(0, END)
        start_entry.delete(0, END)
        end_entry.delete(0, END)
        duration_entry.delete(0, END)
        members_entry.delete(0, END)

        # print('step:', step.name, ',', step.start, '-', step.end, ',', step.duration, ',', step.members)

        self.projects[-1].steps.append(step)

    def click_remove_project(self, index):
        exit_window(self.win_remove_project)
        self.projects.remove(self.projects[index])
        self.refresh_project()

    def click_save_project(self, title_entry):
        self.projects[-1].name = title_entry.get()
        # print('saving project...', self.projects[-1].name)
        exit_window(self.win_add_project)
        self.refresh_project()

    def click_save_chart(self, file_path):
        with open(file_path+'.json', 'w') as f:
            json.dump(projects_to_json(self.projects), f)
        f.close()
        if self.win_save is not None:
            self.win_save.destroy()
        self.gui_chart()

    def click_slide_left(self):
        self.calendar_start -= datetime.timedelta(days=7)
        self.refresh_calendar()

    def click_slide_right(self):
        self.calendar_start += datetime.timedelta(days=7)
        self.refresh_calendar()

    def click_slide_up(self):
        if self.n_row > 0:
            self.n_row -= 1
        self.refresh_project()

    def click_slide_down(self):
        if self.n_row < len(self.projects) - 1:
            self.n_row += 1
        self.refresh_project()

    def gui_welcome(self):
        label_welcome = Label(self.root, text='Gantt Chart')
        button_new = Button(self.root, text='New chart', command=self.click_new)
        button_open = Button(self.root, text='Open chart', command=self.gui_open_chart)

        label_welcome.grid()
        button_new.grid()
        button_open.grid()

    def gui_chart(self):
        # TO DO: template
        self.frame_buttons.grid(row=0, column=0)

        button_add_project = Button(self.frame_buttons, text='+', command=self.gui_add_project)
        button_remove_project = Button(self.frame_buttons, text='-', command=self.gui_remove_project)
        button_save = Button(self.frame_buttons, text='Save', command=self.gui_save_chart)
        button_slide_left = Button(self.frame_buttons, text='<', command=self.click_slide_left)
        button_slide_right = Button(self.frame_buttons, text='>', command=self.click_slide_right)

        button_add_project.grid(row=0, column=0)
        button_remove_project.grid(row=0, column=1)
        button_save.grid(row=0, column=2)
        button_slide_left.grid(row=0, column=3)
        button_slide_right.grid(row=0, column=4)

        self.frame_template.grid(row=1, column=0)
        self.frame_template.grid_propagate(0)

        label_projects = Label(self.frame_template, text='Projects', bg='cyan', width=15)
        label_start = Label(self.frame_template, text='Start date', bg='cyan', width=15)
        label_end = Label(self.frame_template, text='End date', bg='cyan', width=15)
        label_duration = Label(self.frame_template, text='Duration', bg='cyan', width=15)
        label_members = Label(self.frame_template, text='Members', bg='cyan', width=15)
        label_complete = Label(self.frame_template, text='Completed', bg='cyan', width=15)

        button_slide_up = Button(self.frame_template, text='U', command=self.click_slide_up)
        button_slide_down = Button(self.frame_template, text='D', command=self.click_slide_down)

        label_projects.grid(row=0, column=1)
        label_start.grid(row=0, column=2)
        label_end.grid(row=0, column=3)
        label_duration.grid(row=0, column=4)
        label_members.grid(row=0, column=5)
        label_complete.grid(row=0, column=6)

        button_slide_up.grid(row=0, column=0, sticky=S)
        button_slide_down.grid(row=1, column=0, sticky=N)

        self.refresh_project()
        # self.refresh_calendar()

    def gui_add_project(self):
        self.win_add_project = Toplevel(self.root)
        self.projects.append(Project('', []))

        label_title = Label(self.win_add_project, text='Project name')
        label_steps = Label(self.win_add_project, text='Steps')
        label_name = Label(self.win_add_project, text='Name')
        label_start = Label(self.win_add_project, text='From')
        label_end = Label(self.win_add_project, text='To')
        label_duration = Label(self.win_add_project, text='Duration')
        label_members = Label(self.win_add_project, text='Members')

        entry_title = Entry(self.win_add_project)
        entry_name = Entry(self.win_add_project)
        entry_start = Entry(self.win_add_project)
        entry_end = Entry(self.win_add_project)
        entry_duration = Entry(self.win_add_project)
        entry_members = Entry(self.win_add_project)

        button_add = Button(self.win_add_project, text='Add step',
                            command=lambda: self.click_add_project(entry_name,
                                                                   entry_start,
                                                                   entry_end,
                                                                   entry_duration,
                                                                   entry_members))
        button_save = Button(self.win_add_project, text='Save',
                             command=lambda: self.click_save_project(entry_title))

        label_title.grid(row=0, column=0)
        label_steps.grid(row=2, column=0)
        label_name.grid(row=3, column=0)
        label_start.grid(row=4, column=0)
        label_end.grid(row=4, column=2)
        label_duration.grid(row=5, column=0)
        label_members.grid(row=6, column=0)

        entry_title.grid(row=0, column=1)
        entry_name.grid(row=3, column=1)
        entry_start.grid(row=4, column=1)
        entry_end.grid(row=4, column=3)
        entry_duration.grid(row=5, column=1)
        entry_members.grid(row=6, column=1)

        button_add.grid(row=2, column=1)
        button_save.grid(row=7, column=0)

    def gui_remove_project(self):
        self.win_remove_project = Toplevel(self.root)

        label_index = Label(self.win_remove_project, text='ID')
        entry_index = Entry(self.win_remove_project)
        button_remove = Button(self.win_remove_project, text='Remove',
                               command=lambda: self.click_remove_project(int(entry_index.get())))

        label_index.grid(row=0, column=0)
        entry_index.grid(row=0, column=1)
        button_remove.grid(row=1, column=0)

    def gui_save_chart(self):
        if not self.as_new:
            self.click_save_chart(self.file_path)
        else:
            self.win_save = Toplevel(self.root)

            label_name = Label(self.win_save, text='File name')
            entry_name = Entry(self.win_save)
            button_save = Button(self.win_save, text='Save', command=lambda: self.click_save_chart(entry_name.get()))

            label_name.grid(row=0, column=0)
            entry_name.grid(row=0, column=1)
            button_save.grid(row=1, column=0, columnspan=2)

    def gui_open_chart(self):
        self.win_open = Toplevel(self.root)

        label_name = Label(self.win_open, text='File name')
        entry_name = Entry(self.win_open)
        button_open = Button(self.win_open, text='Open', command=lambda: self.click_open(entry_name.get()))

        label_name.grid(row=0, column=0)
        entry_name.grid(row=0, column=1)
        button_open.grid(row=1, column=0, columnspan=2)

    def run(self):
        self.gui_welcome()
        self.root.mainloop()
