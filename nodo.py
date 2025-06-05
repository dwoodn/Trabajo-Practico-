class Nodo:
    def __init__(self, nombre):
        """
        Crea un nodo identificado por el nombre de la ciudad.
        """
        self.nombre = nombre
        self.modos = set()        # modos disponibles (automotor, ferroviario, etc.)
        self.conexiones = []      # lista de conexiones salientes

    def agregar_conexion(self, conexion):
        """
        Agrega una conexión saliente desde este nodo.
        """
        self.conexiones.append(conexion)
        self.modos.add(conexion.modo)

    def soporta_modo(self, modo):
        """
        Verifica si el nodo soporta un modo de transporte.
        """
        return modo in self.modos

    def __str__(self):
        return f"Nodo: {self.nombre} | Modos disponibles: {', '.join(self.modos)}"
    
