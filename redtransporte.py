class RedTransporte:
    def __init__(self, nodos, conexiones):
        self.nodos = nodos  # dict con nombre → Nodo
        self.conexiones = conexiones  # lista de todas las conexiones

    def buscar_caminos(self, origen, destino, modo=None, max_nivel=10):
        """
        Devuelve todos los caminos posibles desde origen a destino (sin loops).
        Si se pasa un modo, solo considera conexiones de ese tipo.
        """
        caminos = []
        self._dfs (origen,destino,modo, max_nivel, [], {origen}, caminos)
        return caminos

    def _dfs(self, actual, destino, modo, max_nivel, camino, visitados, caminos):
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
                    self._dfs(siguiente, destino, modo, max_nivel, camino, visitados | {siguiente}, caminos)
                    camino.pop()