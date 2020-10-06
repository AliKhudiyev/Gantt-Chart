import json


class Step:
    def __init__(self, name='', start='', end='', duration=0, members=[]):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.members = members

    def tell_members(self):
        members = ''
        for i, name in enumerate(self.members):
            members += name
            if i < len(self.members) - 1:
                members += ', '
        return members

    def to_json(self):
        string = '{"name":"' + self.name + '","start":"' + self.start + '","end":"' + self.end + '",'
        string += '"members":['

        for i, member in enumerate(self.members):
            string += '"' + member + '"'
            if i < len(self.members) - 1:
                string += ','
        string += ']}'

        return string


class Project:
    def __init__(self, name='', steps=[]):
        self.name = name
        self.steps = steps

    def to_json(self):
        string = '{"title":"' + self.name + '","steps":['

        for i, step in enumerate(self.steps):
            string += step.to_json()
            if i < len(self.steps) - 1:
                string += ','
        string += ']}'

        return string


def projects_to_json(projects):
    json_str = '{"projects":['

    for i, project in enumerate(projects):
        json_str += project.to_json()
        if i < len(projects) - 1:
            json_str += ','
    json_str += ']}'

    return json.loads(json_str)
