from vehiculo import Vehiculo
# constantes (no num mag)

FERROVIARIO_UMBRAL_DISTANCIA = 200
FERROVIARIO_COSTO_EXTRA = 20

AUTOMOTOR_UMBRAL_PESO = 15000
AUTOMOTOR_COSTO_BAJO = 1
AUTOMOTOR_COSTO_ALTO = 2

# Paso 1: Reemplazar parámetros estáticos por atributos configurables 

class VehiculoFerroviario(Vehiculo):
    def __init__(self, nombre: str,
                 velocidad_kmh: int = 100,
                 capacidad_kg: int = 150000,
                 costo_base: float = 100,
                 costo_por_km: float = 15,
                 costo_por_kg: float = 3):
        super().__init__(
            nombre=nombre,
            modo="ferroviaria",
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        costo_km = FERROVIARIO_COSTO_EXTRA if distancia_km < FERROVIARIO_UMBRAL_DISTANCIA else self.costo_km
        return self.costo_base + (costo_km * distancia_km)


class VehiculoAutomotor(Vehiculo):
    def __init__(self, nombre: str,
                 velocidad_kmh: int = 80,
                 capacidad_kg: int = 30000,
                 costo_base: float = 30,
                 costo_por_km: float = 5,
                 costo_por_kg: float = 0):
        super().__init__(
            nombre=nombre,
            modo="automotor",
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_peso(self, peso_kg):
        costo_kg_unitario = AUTOMOTOR_COSTO_BAJO if peso_kg < AUTOMOTOR_UMBRAL_PESO else AUTOMOTOR_COSTO_ALTO
        return costo_kg_unitario * peso_kg

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)


class VehiculoFluvial(Vehiculo):
    def __init__(self, nombre: str, tipo: str = "fluvial",
                 velocidad_kmh: int = 40,
                 capacidad_kg: int = 100000,
                 costo_por_km: float = 15,
                 costo_por_kg: float = 2):

        if tipo == "fluvial":
            costo_base = 500
        elif tipo == "maritimo":
            costo_base = 1500
        else:
            raise ValueError("Tipo de vehículo fluvial no reconocido. Use 'fluvial' o 'maritimo'.")

        super().__init__(
            nombre=nombre,
            modo=tipo,
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)


class VehiculoAereo(Vehiculo):
    def __init__(self, nombre: str,
                 velocidad_kmh: int = 600,
                 capacidad_kg: int = 5000,
                 costo_base: float = 750,
                 costo_por_km: float = 40,
                 costo_por_kg: float = 10):
        super().__init__(
            nombre=nombre,
            modo="aerea",
            velocidad_kmh=velocidad_kmh,
            capacidad_kg=capacidad_kg,
            costo_base=costo_base,
            costo_por_km=costo_por_km,
            costo_por_kg=costo_por_kg
        )

    def calcular_costo_por_distancia(self, distancia_km, tipo=None):
        return self.costo_base + (self.costo_km * distancia_km)
