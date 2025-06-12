class RedTransporte:
    def _init_(self, nodos, conexiones):
        self.nodos = nodos  # dict con nombre → Nodo
        self.conexiones = conexiones  # lista de todas las conexiones

    def buscar_caminos(self, origen, destino, modo=None, max_nivel=10):
        """
        Devuelve todos los caminos posibles desde origen a destino (sin loops).
        Si se pasa un modo, solo considera conexiones de ese tipo.
        """
        caminos = []

        def dfs(actual, camino, visitados):
            if actual == destino:
                caminos.append(list(camino))
                return
            if len(visitados) > max_nivel:
                return
            for conexion in self.nodos[actual].conexiones:
                if modo and conexion.modo != modo:
                    continue
                siguiente = conexion.destino.nombre
                if siguiente not in visitados:
                    camino.append(conexion)
                    dfs(siguiente, camino, visitados | {siguiente})
                    camino.pop()

        dfs(origen, [], {origen})
        return caminos
