import matplotlib.pyplot as plt

def graficar_grafo_matplotlib(nodos, conexiones, coordenadas):
    """
    nodos: dict nombre -> Nodo
    conexiones: lista de Conexion
    coordenadas: dict nombre -> (x, y)
    """
    # Paleta de colores más distintiva
    colores_modo = {
        'ferroviaria': '#FF0000',     # Rojo brillante
        'automotor': '#0066FF',       # Azul royal
        'fluvial': '#00CC00',         # Verde brillante
        'aerea': '#9933FF',           # Púrpura
        'maritimo': '#FF9900'         # Naranja
    }

    plt.figure(figsize=(15, 10))
    

    # Primero dibujamos las conexiones
    for conexion in conexiones:
        x0, y0 = coordenadas[conexion.origen.nombre]
        x1, y1 = coordenadas[conexion.destino.nombre]
        color = colores_modo.get(conexion.modo, '#666666')
        # Dibujar línea con flecha
        plt.arrow(x0, y0, (x1-x0)*0.9, (y1-y0)*0.9, 
                 color=color, linewidth=2, alpha=0.8,
                 head_width=0.2, head_length=0.3, 
                 length_includes_head=True)
        
        # Etiqueta de distancia y modo, con offset para evitar superposición
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        # Calcular offset perpendicular a la línea
        dx = x1 - x0
        dy = y1 - y0
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            offset_x = -dy/length * 0.3
            offset_y = dx/length * 0.3
        else:
            offset_x = offset_y = 0
            
        plt.text(mid_x + offset_x, mid_y + offset_y, 
                f'{conexion.modo}\n{conexion.distancia}km', 
                fontsize=8, color='black',
                bbox=dict(facecolor='white', edgecolor=color, alpha=0.9),
                ha='center', va='center')

    # Luego dibujamos los nodos encima
    for nombre, (x, y) in coordenadas.items():
        # Círculo blanco con borde negro para el nodo
        circle = plt.Circle((x, y), 1, color='white', ec='black', lw=2, zorder=10)
        ax = plt.gca()
    
        # Nombre del nodo con fondo blanco
        plt.text(x, y, nombre, fontsize=10, ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', alpha=0.9),
                zorder=11)

    # Leyenda con recuadro
    legend_elements = []
    for modo, color in colores_modo.items():
        legend_elements.append(plt.Line2D([0], [0], color=color, 
                                       label=modo.capitalize(), linewidth=3))
    plt.legend(handles=legend_elements, 
              title='Modos de Transporte',
              bbox_to_anchor=(1.15, 1), 
              loc='upper right')

    plt.title('Red de Transporte - Rutas Disponibles\nConexiones entre ciudades y modos de transporte', 
             pad=20, fontsize=14)
    
    # Ajustar los límites del gráfico para dar más espacio
    plt.margins(0.2)
    plt.axis('equal')  # Mantener proporciones
    plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    from lectura_archivo import LecturaArchivos
    # Coordenadas ajustadas para mejor distribución
    coordenadas = {
        'Zarate': (2, 6),
        'Buenos_Aires': (6, 8),
        'Junin': (3, 3),
        'Azul': (8, 3),
        'Mar_del_Plata': (10, 1),
    }
    lector = LecturaArchivos()
    lector.leer_nodos("archivos_ejemplo/nodos.csv")
    lector.leer_conexiones("archivos_ejemplo/conexiones.csv")
    nodos, conexiones = lector.obtener_red()
    graficar_grafo_matplotlib(nodos, conexiones, coordenadas) 