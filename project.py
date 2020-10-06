class Step:
    def __init__(self, name, start, end, duration, members):
        self.name = name
        self.start = start
        self.end = end
        self.duration = duration
        self.members = members

    def tell_members(self):
        members = ''
        for i, name in enumerate(self.members):
            members += name
            if i < len(self.members)-1:
                members += ', '
        return members


class Project:
    def __init__(self, name='', steps=[]):
        self.name = name
        self.steps = steps
