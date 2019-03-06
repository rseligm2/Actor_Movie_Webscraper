class Movie(object):

    def __init__(self, name, url, gross = 0, year = 0):
        self._name = name
        self._url = url
        self._gross = gross
        self._year = year

    def __str__(self):
        return self._name

    def setgross(self, gross):
        self._gross = gross

    def setyear(self, year):
        self._year = year

    def getgross(self):
        return self._gross

