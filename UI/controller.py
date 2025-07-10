from collections import Counter

import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        colors = self._model.getAllColori()
        for c in colors:
            self._listColor.append(c[0]) #è una tupla, quindi accedo in modo posizionale
        for color in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(color))

    def fillDDYear(self):
        self._listYear = [2015, 2016, 2017, 2018]
        for y in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(y))


    def handle_graph(self, e):
        anno = self._view._ddyear.value
        colore = self._view._ddcolor.value
        if anno is None or colore is None:
            self._view.txtOut.controls.clear()
            self._view.txtOut.controls.append(ft.Text("Attenzione, selezionare tutti i parametri!", color="red"))
            self._view.update_page()
        grafo = self._model.buildGraph(anno, colore)
        self._view.txtOut.controls.clear()
        self._view.txtOut.controls.append(ft.Text(f"Grafo correttamente creato"))
        self.fillDDProduct()
        self._view.txtOut.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodes(grafo)}, numero di archi: {self._model.getNumEdges(grafo)}"))
        edges_sorted = sorted(grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
        self._view.txtOut.controls.append(ft.Text("Gli archi sono:"))
        nodesTemp = []
        for u,v, data in edges_sorted[0:3]:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {u.Product_number} a {v.Product_number} con peso {data["weight"]}"))
            nodesTemp.append(u)
            nodesTemp.append(v)
        cont = Counter(nodesTemp)
        ripetuti = [nodo for nodo, count in cont.items() if count > 1]
        self._view.txtOut.controls.append(ft.Text("I nodi ripetuti sono:"))
        for r in ripetuti:
            self._view.txtOut.controls.append(ft.Text(r.Product_number))
        self._view.update_page()

    def fillDDProduct(self):
        nodes = self._model.getNodesGraph()
        seen = set()
        for n in nodes:
            if n.Product_number not in seen:
                seen.add(n.Product_number)
                self._view._ddnode.options.append(ft.dropdown.Option(n.Product_number))


    def handle_search(self, e):
        sourceInput = int(self._view._ddnode.value)
        source = self._model._idMap[sourceInput]
        path = self._model.getBestPath(source)
        self._view.txtOut2.controls.clear()
        self._view.txtOut2.controls.append(ft.Text(f"Numero archi del percorso più lungo: {len(path)}"))
        self._view.update_page()