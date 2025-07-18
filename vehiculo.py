class Vehiculo:
    def __init__(self, nombre: str, modo: str, velocidad_kmh: int, capacidad_kg: int,
                 costo_base: float, costo_por_km: float, costo_por_kg: float):
        """
        Crea un vehículo con sus características operativas.
        """
        self.nombre = nombre
        self.modo = modo.lower()
        self.velocidad = velocidad_kmh
        self.capacidad = capacidad_kg
        self.costo_base = costo_base
        self.costo_km = costo_por_km
        self.costo_kg = costo_por_kg

    def calcular_costo_por_peso(self, peso_kg):
        return self.costo_kg * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)

    def __str__(self):
        return (f"{self.nombre} [{self.modo.upper()}] | Velocidad: {self.velocidad} km/h | "
                f"Capacidad: {self.capacidad} kg | Costos: Base ${self.costo_base}, "
                f"xKm ${self.costo_km}, xKg ${self.costo_kg}")
    
#     #ejemplo de uso
#
# camion = Vehiculo(
#     nombre="Camión Estándar",
#     modo="automotor",
#     velocidad_kmh=80,
#     capacidad_kg=10000,
#     costo_base=200,
#     costo_por_km=5,
#     costo_por_kg=0.1
# )
#
# # Calcular costo de un tramo de 100 km y 5000 kg
# costo = camion.calcular_costo_por_distancia(distancia_km=100)

