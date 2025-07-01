from planificador import Planificador

class PlanificadorPorTiempo(Planificador):
    def planificar(self, origen, destino, peso_kg):
        modos = ["automotor", "ferroviaria", "aerea", "fluvial"]
        mejores = []

        for modo in modos:
            caminos = self.red.buscar_caminos(origen, destino, modo)
            for camino in caminos:
                try:
                    costo, tiempo = self.evaluar_camino(camino, peso_kg)
                    mejores.append((camino, costo, tiempo))
                except:
                    continue

        return min(mejores, key=lambda x: x[2]) if mejores else None