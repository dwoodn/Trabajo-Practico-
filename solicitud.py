class Solicitud:
    def __init__(self, id_carga, peso_kg, origen, destino):
        """
        Representa una solicitud de transporte de carga.

        """
        self.id_carga = id_carga
        self.peso_kg = peso_kg
        self.origen = origen
        self.destino = destino


    def __str__(self):
        return (f"Carga ID: {self.id_carga} | Peso: {self.peso_kg} kg | "
                f"Origen: {self.origen} ➜ Destino: {self.destino}")

import csv

def leer_solicitudes_csv(ruta_archivo):
    solicitudes = []
    with open(ruta_archivo, newline='', encoding='utf-8') as f:
        lector = csv.DictReader(f)
        for fila in lector:
            solicitud = Solicitud(
                id_carga=fila["id_carga"],
                peso_kg=float(fila["peso_kg"]),
                origen=fila["origen"],
                destino=fila["destino"]
            )
            solicitudes.append(solicitud)
    return solicitudes
