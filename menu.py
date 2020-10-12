from tkinter import filedialog
import os
from project_frame import *
import webbrowser


class MenuBar(Menu):
    def __init__(self, master, app):
        Menu.__init__(self, master)
        self.master = master
        self.app = app

    def click_show_completion(self):
        self.app.calendarFrame.show_completion = not self.app.calendarFrame.show_completion
        self.app.update()

    def click_display_dates(self):
        if self.app.calendarFrame.display_dates:
            self.app.calendarFrame.label_date.place_forget()
        self.app.calendarFrame.display_dates = not self.app.calendarFrame.display_dates
        self.app.update()

    def click_about(self, event):
        webbrowser.open_new('https://github.com/AliKhudiyev/Gantt-Chart/wiki')

    def gui_new(self):
        self.app.reset()
        self.app.update()

    def gui_open(self):
        file_type = [('Gantt Chart', '*.json')]
        file_path = filedialog.askopenfilename(parent=self.master,
                                               initialdir=os.getcwd(),
                                               title='Please select a chart:',
                                               filetypes=file_type)
        # print('Open', file_path)
        self.app.projectFrame.load_file(file_path)
        self.app.update()

    def gui_save(self):
        # print(to_json(self.app.projectFrame.projects))
        file_path = self.app.projectFrame.file_path
        if len(file_path) > 0:
            self.app.projectFrame.save_frame(file_path)

    def gui_save_as(self):
        file_type = [('Gantt Chart', '*.json')]
        file_path = filedialog.asksaveasfilename(parent=self.master,
                                                 initialdir=os.getcwd(),
                                                 title='Please select a chart name for saving:',
                                                 filetypes=file_type)
        # print('Save as', file_path)
        self.app.projectFrame.save_frame(file_path + '.json')

    def gui_add(self):
        # print('Adding...')
        form = ProjectFormWindow(self.master, self.app)
        form.run()

    def gui_edit(self):
        # print('Editing...')
        form = ProjectEditWindow(self.master, self.app)
        form.run()

    def gui_remove(self):
        # print('Removing...')
        form = ProjectRemoveWindow(self.master, self.app)
        form.run()

    def gui_about(self):
        # print('About...')
        text = '''Gantt Chart Software
        
        Version: 1.7
        License: MIT
        '''

        win = Toplevel(self)
        win.title('About')

        label_about = Label(win, text=text)
        label_link = Label(win, text='To learn more about the software visit my github wiki page.', cursor='hand2')

        label_about.pack()
        label_link.pack()
        label_link.bind('<Button-1>', self.click_about)

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
        menu_settings.add_command(label='Show completion', command=self.click_show_completion)
        menu_settings.add_command(label='Show dependencies')
        menu_settings.add_command(label='Display dates', command=self.click_display_dates)
        menu_settings.add_command(label='Preferences')
        menu_settings.add_separator()
        menu_settings.add_command(label='About', command=self.gui_about)

        self.add_cascade(label='Settings', menu=menu_settings)

        self.master.config(menu=self)
