from nodo import Nodo

class Conexion:
    def __init__(self, origen, destino, modo, distancia_km, restricciones=None):
        """
        Crea una conexión entre dos nodos con modo de transporte y restricciones específicas.
        """
        self.origen = origen
        self.destino = destino
        self.modo = modo.lower()
        self.distancia = distancia_km
        self.restricciones = restricciones or {}

    def es_valida_para(self, vehiculo, peso_envio):
        """
        Verifica si un vehículo puede transitar esta conexión para cierto peso.
        """
        if self.modo != vehiculo.modo:
            return False

        if self.modo == "ferroviario":
            vel_max = self.restricciones.get("velocidad_maxima")
            if vel_max and vehiculo.velocidad > vel_max:
                return False

        elif self.modo == "automotor":
            peso_max = self.restricciones.get("peso_maximo")
            if peso_max and peso_envio > peso_max:
                return False

        # Aéreo y marítimo no tienen validación estricta por ahora
        return True

    def __str__(self):
        return (f"{self.modo.upper()} | {self.origen.nombre} ➜ {self.destino.nombre} "
                f"({self.distancia} km) | Restricciones: {self.restricciones}")
    
    # Crear nodos
bahia = Nodo("Bahía Blanca")
laplata = Nodo("La Plata")


# Crear una conexión ferroviaria con límite de velocidad
conexion_ferro = Conexion(
    origen=bahia,
    destino=laplata,
    modo="ferroviario",
    distancia_km=550,
    restricciones={"velocidad_maxima": 90}
)

# Asociar la conexión a los nodos
bahia.agregar_conexion(conexion_ferro)
laplata.agregar_conexion(conexion_ferro)
# Imprimir información de la conexión

