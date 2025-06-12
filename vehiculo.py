class Vehiculo:
    def __init__(self, nombre, modo, velocidad_kmh, capacidad_kg,
                 costo_base, costo_por_km, costo_por_kg):
        """
        Crea un vehículo con sus características operativas.

        Args:
            nombre (str): nombre del modelo del vehículo
            modo (str): tipo de transporte (automotor, ferroviario, aéreo, marítimo)
            velocidad_kmh (float): velocidad nominal del vehículo
            capacidad_kg (float): carga máxima que puede transportar
            costo_base (float): costo fijo por tramo
            costo_por_km (float): costo variable por kilómetro
            costo_por_kg (float): costo variable por kilo transportado
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

