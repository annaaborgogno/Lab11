import copy
import networkx as nx
from networkx.classes import Graph
from database.DAO import DAO


class Model:
    def __init__(self):
        self._nodes = []
        self._graph = nx.Graph()
        self._idMap = {}
        self._bestPath = []

    def getAllColori(self):
        return DAO.getAllColori()

    def addAllEdges(self, year, color):
        edges = DAO.getArchi(year, color)
        for edge in edges:
            u = self._idMap[edge.p1ID]
            v = self._idMap[edge.p2ID]
            self._graph.add_edge(u, v, weight=edge.peso)

    def buildGraph(self, year, color):
        self._nodes = DAO.getNodes(color)
        for node in self._nodes:
            self._idMap[node.Product_number] = node
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges(year, color)
        return self._graph

    def getNumNodes(self, graph):
        return graph.number_of_nodes()

    def getNumEdges(self, graph):
        return graph.number_of_edges()

    def getNodesGraph(self):
        return self._graph.nodes

    def getBestPath(self, source):
        self._bestPath = []
        path = [source]
        self.ricorsione(source, path, [])
        path.remove(source) #rimuovo il primo nodo
        return self._bestPath

    def ricorsione(self, current, path, pesi):
        if len(path) > len(self._bestPath): # la condizione migliore si basa sul numero di archi
            self._bestPath = copy.deepcopy(path)

        for n in self._graph.neighbors(current):
            if n in path:
                continue #altrimenti cicla all'infinito
            peso = self._graph[current][n]["weight"]
            if not pesi or peso >= pesi[-1]:
                path.append(n)
                pesi.append(peso)
                self.ricorsione(n, path, pesi)
                path.pop()
                pesi.pop()