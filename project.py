import json


class Step:
    def __init__(self, name=''):
        self.name = name
        self.start = None
        self.end = None
        self.duration = 0
        self.members = []

    def is_valid(self):
        if len(self.name) == 0 or self.start is None or self.end is None or \
                self.duration < 0 or len(self.members) < 0:
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
        for step in self.steps:
            if not step.is_valid():
                return False

        if len(self.title) == 0 or len(self.steps) == 0:
            return False

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
        json_str += '], "description": ' + json.dumps(self.about) + '}'
        # print('prepared:', json.dumps(self.about))
        # print('saved:', json.loads(json.dumps(self.about)))

        return json_str


def to_json(projects):
    json_str = '{"projects": ['
    for i, project in enumerate(projects):
        json_str += project.to_json()
        if i < len(projects) - 1:
            json_str += ', '
    json_str += ']}'

    return json.loads(json_str)
