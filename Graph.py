from collections import defaultdict
from Actor import Actor
from Movie import Movie
import logging

logging.basicConfig(filename='crawler.log',level=logging.DEBUG, format='%(asctime)s %(message)s', filemode='w+')

class Graph:


    def __init__(self):
        self._nodes = {}
        self._nummovies = 0
        self._numactors = 0
        self._actornodes = []
        self._movienodes = []

    def addNode(self, newnodeobj):
        newnode = Node(newnodeobj)
        if type(newnodeobj) is Actor:
            self._numactors += 1
            self._actornodes.append(newnode)
        else:
            self._nummovies += 1
            self._movienodes.append(newnode)
        logging.info("Added " + str(newnodeobj) + " to graph")
        self._nodes[newnodeobj] = newnode

    def addTo(self, add1, add2):
        if add1 not in self._nodes:
            self.addNode(add1)
        if add2 not in self._nodes:
            self.addNode(add2)
        self._nodes[add1].addEdge(self._nodes[add2])
        self._nodes[add2].addEdge(self._nodes[add1])

    # def checkduplicate(self, obj):
    #     for check in self._nodes:
    #         if(obj._name == check._name):
    #             print("Found duplicate")
    #             return True
    #     return False

    def __str__(self):
        string = ""
        for node in self._nodes:
            string += str(node) + ' '
        return string

    def gettopXgrossactors(self, num):
        topactors = {}
        for node in self._nodes:
            if type(node) is Actor:
                topactors[node] = node._moviegross
        sortedactors = sorted(topactors, key=topactors.__getitem__, reverse=True)
        return sortedactors[:num]

    def gettopXoldactors(self, num):
        topactors = {}
        for node in self._nodes:
            if type(node) is Actor:
                topactors[node] = node._age
        sortedactors = sorted(topactors, key=topactors.__getitem__, reverse=True)
        return sortedactors[:num]

    def moviesfromyear(self, year):
        movies = []
        for node in self._nodes:
            if type(node) is Movie and node._year == year:
                movies.append(node)
        return movies

    def actorsbornyear(self, year):
        actors = []
        theage = 2019 - year
        for node in self._nodes:
            if type(node) is Actor and node._age == theage:
                actors.append(node)
        return actors

    def getactor(self, name):
        for actor in self._actornodes:
            if actor._object._name == name:
                logging.info("Found: " + actor._object._name)
                return actor._object
        logging.warning("Couldn't find actor: " + name)
        return None

    def getmovie(self, name):
        for movie in self._movienodes:
            if movie._object._name == name:
                logging.info("Found: " + movie._object._name)
                return movie._object
        logging.warning("Couldn't find movie: " + name)
        return None

    def getfilteractors(self, name, age):
        actors = []
        for actor in self._actornodes:
            if name and name in actor._object._name and age and actor._object._age == int(age):
                actors.append(actor._object)
                print("Found actor: " + actor._object._name)
            elif name and name in actor._object._name and not age:
                actors.append(actor._object)
                print("Found actor: " + actor._object._name)
            elif age and actor._object._age == int(age) and not name:
                actors. append(actor._object)
                print("Found actor: " + actor._object._name)
            elif not name and not age:
                print("No args")
                logging.warning("No args given to getfilteractors")
                return
            else:
                continue
        if not actors:
            print("Couldn't find actors")
            logging.warning("Couln't find any actors with given args")
            return
        else:
            return actors

    def getfiltermovies(self, name, year):
        movies = []
        for movie in self._movienodes:
            if name and name in movie._object._name and year and int(movie._object._year) == int(year):
                movies.append(movie._object)
                print("Found movie: " + movie._object._name)
            elif name and name in movie._object._name and not year:
                movies.append(movie._object)
                print("Found movie: " + movie._object._name)
            elif year and int(movie._object._year) == int(year) and not name:
                movies. append(movie._object)
                print("Found movie: " + movie._object._name)
            elif not name and not year:
                print("No args")
                logging.warning("No args given to getfiltermovies")
                return
            else:
                continue
        if not movies:
            print("Couldn't find movies")
            logging.warning("Couln't find any movies with given args")
            return
        else:
            return movies

class Node:
    def __init__(self, obj):
        self._object = obj
        self._edges = {}

    def addEdge(self, node2):
        if type(self._object) is Actor:
            weight = self._object._age * node2._object._gross
            self._object._moviegross += float(node2._object._gross)
        else:
            weight = node2._object._age * self._object._gross
        self._edges[node2] = weight

    def __str__(self):
        string = str(self._object) + ": \n" + str(self._edges)
        return string

    def __repr__(self):
        string = str(self._object)
        return string

    def getconnections(self):
        return self._edges






