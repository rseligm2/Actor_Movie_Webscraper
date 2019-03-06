from GraphFromData import GraphFromData
from Graph import Graph

graph = Graph()
json = GraphFromData("data.json")
graph = json.createGraph()
print(str(graph))