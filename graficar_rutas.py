import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

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

    # Definir los grupos de modos para cada gráfico
    grupos_modos = {
        'Automotor': ['automotor'],
        'Ferroviario': ['ferroviaria'],
        'Fluvial + Marítimo': ['fluvial', 'maritimo'],
        'Aéreo': ['aerea']
    }
    
    # Crear un gráfico separado para cada grupo
    for titulo_grupo, modos_grupo in grupos_modos.items():
        # Crear nueva figura para cada grupo
        plt.figure(figsize=(12, 10))
        
        # Filtrar conexiones para este grupo
        conexiones_grupo = [c for c in conexiones if c.modo in modos_grupo]
        
        # Dibujar conexiones del grupo
        for conexion in conexiones_grupo:
            x0, y0 = coordenadas[conexion.origen.nombre]
            x1, y1 = coordenadas[conexion.destino.nombre]
            color = colores_modo.get(conexion.modo, '#666666')
            
            # Dibujar línea con flecha
            plt.arrow(x0, y0, (x1-x0)*0.9, (y1-y0)*0.9, 
                     color=color, linewidth=2, alpha=0.8,
                     head_width=0.2, head_length=0.3, 
                     length_includes_head=True)
            
            # Etiqueta de distancia y modo
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

        # Dibujar todos los nodos
        for nombre, (x, y) in coordenadas.items():
            # Círculo blanco con borde negro para el nodo
            circle = Circle((x, y), 1, color='white', ec='black', lw=2, zorder=10)
            plt.gca().add_patch(circle)
        
            # Nombre del nodo con fondo blanco
            plt.text(x, y, nombre, fontsize=10, ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', alpha=0.9),
                    zorder=11)

        # Configurar el gráfico
        plt.title(f'Red de Transporte - {titulo_grupo}\n({len(conexiones_grupo)} conexiones)', 
                 fontsize=14, fontweight='bold', pad=20)
        
        # Si no hay conexiones, mostrar mensaje informativo
        if len(conexiones_grupo) == 0:
            plt.text(6, 4.5, 'Sin conexiones\nen este modo', 
                    fontsize=14, ha='center', va='center',
                    bbox=dict(facecolor='lightgray', edgecolor='black', alpha=0.7))
        
        plt.margins(0.2)
        plt.axis('equal')  # Mantener proporciones
        plt.axis('off')
        
        # Agregar leyenda específica para este grupo
        legend_elements = []
        for modo in modos_grupo:
            if any(c.modo == modo for c in conexiones_grupo):
                legend_elements.append(Line2D([0], [0], color=colores_modo[modo], 
                                           label=modo.capitalize(), linewidth=3))
        if legend_elements:
            plt.legend(handles=legend_elements, 
                      title='Modos de Transporte',
                      loc='upper right', fontsize=10)
        
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