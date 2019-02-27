from collections import defaultdict

class Graph(object):


    def __init__(self, edge, directed = False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_edge(edge)

    def add_edge(self, edge):
        for node1, node2 in edge:
            self.add(node1, node2)

    def add(self, node1, node2):
        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        for n, cxns in self._graph.iteritems():
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        return node1 in self._graph and node2 in self._graph[node1]

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    def getMovies(self, key):
        return self._graph.get(key)

    def jdefault(o):
        return o.__dict__

"""https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python"""