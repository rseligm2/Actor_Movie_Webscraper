class Actor(object):

    def __init__(self, name, age):
        self._name = name
        self._age = age

    def __str__(self):
        return self._name

    def getAge(self):
        return self._age
