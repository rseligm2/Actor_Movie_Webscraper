from Graph import Graph
from Actor import Actor
from Movie import Movie
import json
import string
import logging

logging.basicConfig(filename='graph_from_json.log', level=logging.DEBUG, format='%(asctime)s %(message)s',
                    filemode='w+')


class GraphFromData:

    def __init__(self, filename):
        self._filename = filename

    # create graph object from given json file
    def createGraph(self):
        with open('data.json', "r") as f:
            data = json.load(f)
        newgraph = Graph()
        # loop goes through json file and adds nods for Actors and Movies
        for obj in data:
            for object in obj.values():
                if object["json_class"] == "Actor":
                    printable = set(string.printable)
                    namestr = filter(lambda x: x in printable, object["name"])
                    actor = Actor(namestr, object["age"])
                    actor._moviegross = object["total_gross"]
                    logging.info("Got actor " + actor._name + " from JSON")
                    newgraph.addNode(actor)
                else:
                    printable = set(string.printable)
                    namestr = filter(lambda x: x in printable, object["name"])
                    movie = Movie(namestr, object["wiki_page"], object["box_office"] / 1000000, object["year"])
                    logging.info("Got movie " + movie._name + " from JSON")
                    newgraph.addNode(movie)
        # loop goes through json fil and adds edges for existing Movie and Actor nodes
        for obj in data:
            for object in obj.values():
                if object["json_class"] == "Actor":
                    printable = set(string.printable)
                    namestr = filter(lambda x: x in printable, object["name"])
                    actor = newgraph.getactor(namestr)
                    for movie in object["movies"]:
                        printable = set(string.printable)
                        namestr = filter(lambda x: x in printable, movie)
                        addmovie = newgraph.getmovie(namestr)
                        if addmovie == None:
                            logging.warning(namestr + " not in given JSON")
                            continue
                        logging.info("Linking movie " + addmovie._name)
                        newgraph.addTo(actor, addmovie)
                else:
                    printable = set(string.printable)
                    namestr = filter(lambda x: x in printable, object["name"])
                    movie = newgraph.getmovie(namestr)
                    for actor in object["actors"]:
                        printable = set(string.printable)
                        namestr = filter(lambda x: x in printable, actor)
                        addactor = newgraph.getactor(namestr)
                        if addactor == None:
                            logging.warning(namestr + " not in given JSON")
                            continue
                        logging.info("Linking actor " + addactor._name)
                        newgraph.addTo(movie, addactor)

        return newgraph
