from project_frame import *


class CalendarFrame(LabelFrame):
    def __init__(self, master, app, width, height):
        LabelFrame.__init__(self, master, width=width, height=height)
        self.app = app
        self.mainFrame = LabelFrame(self)
        self.sliderFrame = LabelFrame(self, width=width, height=35)

        self.header = LabelFrame(self.mainFrame)
        self.body = Canvas(self.mainFrame, width=560, height=470)

        self.button_left = Button(self.sliderFrame, text=u'\u2190', command=self.click_left)
        self.button_right = Button(self.sliderFrame, text=u'\u2192', command=self.click_right)
        self.label_date = Label(self.sliderFrame, text='?', width=10, bg='orange')

        self.week_pad = 1
        self.n_week = 4
        self.calendar_start = datetime.datetime.now()
        self.weekdays = ['M', 'T', 'W', 'Th', 'F', 'St', 'S']

        self.sliderFrame.grid(row=0, column=0)
        self.mainFrame.grid(row=1, column=0)
        self.sliderFrame.grid_propagate(0)

        self.marked_dates = []
        self.w = 18
        self.h = 26
        self.x_offset = 3
        self.y_offset = 0
        self.week_pad_pixels = 15
        self.show_completion = False
        self.display_dates = False

    def tell_position(self, x_pos, y_pos):
        week_index = np.floor((x_pos - self.x_offset) / (7 * self.w + self.week_pad_pixels))
        x = np.floor((x_pos - self.x_offset - self.week_pad_pixels * week_index) / self.w)
        y = np.floor((y_pos - self.y_offset) / self.h)

        return int(x), int(y)

    def on_click(self, event):
        x, y = self.tell_position(event.x, event.y)
        text = ''
        if x >= 0 and y >= 0:
            time = self.calendar_start + datetime.timedelta(x)
            text = time.strftime('%d/%m/%Y')
        self.label_date.configure(text=text)

    def click_left(self):
        self.calendar_start -= datetime.timedelta(7)
        self.update(self.n_week,
                    self.app.projectFrame.projects[self.app.projectFrame.start_index:],
                    self.calendar_start)

    def click_right(self):
        self.calendar_start += datetime.timedelta(7)
        self.update(self.n_week,
                    self.app.projectFrame.projects[self.app.projectFrame.start_index:],
                    self.calendar_start)

    def date_index(self, date):
        dt = (date - self.calendar_start).days
        n = 0

        if dt < 0:
            return -1

        while n < dt:
            n += 1
            if (n + 1) % 8 == 0:
                dt += 1
        return n

    def mark_date(self, row_index, date, color, span=1):
        for i in range(span):
            if row_index > 17 or self.date_index(date) + i > 27 + 3:
                continue
            label = Label(self.body, width=1, bg=color)
            label.grid(row=row_index, column=self.date_index(date) + i)

            self.marked_dates.append(label)

    def mark_date_cell(self, row_index, date, color, span=1, show_completion=False):
        w = self.w
        h = self.h
        x_offset = self.x_offset
        offset = (date - self.calendar_start).days
        x_pad = (offset // 7) * self.week_pad_pixels
        begin = 0
        now = datetime.datetime.now()
        now = datetime.datetime(year=now.year, month=now.month, day=now.day)

        if offset < 0:
            x_pad = 0
            begin = -offset

        for i in range(begin, span):
            current_date = date + datetime.timedelta(i)
            if offset + i > 27 + 3 or row_index > 17:
                break
            if i > begin and current_date.weekday() == 0:
                x_pad += self.week_pad_pixels

            self.body.create_rectangle(w * (offset + i) + x_offset + x_pad, h * row_index,
                                       w * (offset + i + 1) + x_offset + x_pad, h * (row_index + 1),
                                       fill=color)

            if show_completion and now > current_date:
                self.body.create_rectangle(w * (offset + i) + x_offset + x_pad + 5, h * row_index + 5,
                                           w * (offset + i + 1) + x_offset + x_pad - 5, h * (row_index + 1) - 5,
                                           fill='green')
            elif show_completion and now == current_date:
                self.body.create_oval(w * (offset + i) + x_offset + x_pad + 5, h * row_index + 8,
                                      w * (offset + i + 1) + x_offset + x_pad - 5, h * (row_index + 1) - 8,
                                      fill='cyan')

    def display_today(self):
        now = datetime.datetime.now()
        n = self.date_index(now)

        if 0 <= n <= 27 + 3:
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
        # print('Calendar starts in', self.calendar_start)

    def gui_template(self, n_week=4):
        if self.display_dates:
            self.label_date.place(relx=0.1, y=5)

        for i in range(n_week):
            for j in range(7):
                label = Label(self.header, text=self.weekdays[j], width=1)
                label.grid(row=0, column=8 * i + j, padx=2)
            label = Label(self.header, width=self.week_pad)
            label.grid(row=0, column=8 * (i + 1) - 1)

        w = self.w
        h = self.h
        x_offset = self.x_offset
        y_offset = self.y_offset

        for r in range(18):
            x_pad = 0
            for i in range(n_week):
                for j in range(7):
                    if j == 0 and i != 0:
                        x_pad += self.week_pad_pixels

                    self.body.create_rectangle(w * (7 * i + j) + x_offset + x_pad, h * r + y_offset,
                                               w * (7 * i + j + 1) + x_offset + x_pad, h * (r + 1) + y_offset,
                                               fill='orange')

    def update(self, n_week=1, projects=[], start_date=None):
        self.body.destroy()
        self.body = Canvas(self.mainFrame, width=560, height=470)
        self.body.bind('<Button-1>', self.on_click)

        reset_frame(self.header)

        self.button_left.place(x=10)
        self.button_right.place(relx=0.9)

        self.n_week = n_week
        self.header.grid(row=0, column=0)
        self.body.grid(row=1, column=0)
        self.grid_propagate(0)

        self.gui_template()

        if start_date is None:
            self.update_calendar_start(projects)

        n_row = 0
        for project in projects:
            dt = (project.end - project.start).days
            self.mark_date_cell(n_row, project.start, 'purple', dt, self.show_completion)
            for step in project.steps:
                dt = (step.end - step.start).days
                self.mark_date_cell(n_row + 1, step.start, 'blue', dt, self.show_completion)
                n_row += 1
            n_row += 1
            if n_row > 17:
                break

        self.display_today()
