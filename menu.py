from tkinter import filedialog
import os
from project_frame import *


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
