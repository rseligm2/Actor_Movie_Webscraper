class Actor(object):

    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._url = ""
        self._moviegross = 0.0
        self._othermovies = []

    def __str__(self):
        return self._name

