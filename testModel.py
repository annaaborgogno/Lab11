from model.model import Model

m = Model()
grafo = m.buildGraph(2018, "White")
print(m.getNumEdges(grafo))
print(m.getNumNodes(grafo))