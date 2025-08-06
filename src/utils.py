import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os
import pandas as pd
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches

from model import SUSCETIVEL, INFECTADO, RECUPERADO, VAZIO, ESTADOS, ESTADO_MAPA_CORES

def plot_sir_curves(df_counts, output_path, total_pop=None):
    """
    Plota e salva as curvas de Suscetível, Infectado e Recuperado,
    usando as cores definidas no modelo.
    """
    os.makedirs(output_path, exist_ok=True)

    plt.figure(figsize=(10, 6))
    
    if total_pop:
        df_counts = df_counts / total_pop
        ylabel = 'Fração da População'
    else:
        ylabel = 'Contagem da População'
        
    plt.plot(df_counts['susceptible'], label='Suscetível', color=ESTADO_MAPA_CORES[SUSCETIVEL], linewidth=2)
    plt.plot(df_counts['infected'], label='Infectado', color=ESTADO_MAPA_CORES[INFECTADO], linewidth=2)
    plt.plot(df_counts['recovered'], label='Recuperado', color=ESTADO_MAPA_CORES[RECUPERADO], linewidth=2)
    
    plt.title('Dinâmica da Epidemia (SIRS)')
    plt.xlabel('Passos de Tempo')
    plt.ylabel(ylabel)
    
    # Cria uma legenda com os nomes e cores dos estados
    patches = [
        mpatches.Patch(color=ESTADO_MAPA_CORES[SUSCETIVEL], label='Suscetível'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[INFECTADO], label='Infectado'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[RECUPERADO], label='Recuperado')
    ]
    plt.legend(handles=patches)
    
    plt.grid(True)
    plt.savefig(os.path.join(output_path, "sir_curves.png"))
    plt.close()

def save_grid_animation(history, output_path):
    """
    Cria e salva uma animação da grade com uma legenda manual.
    """
    os.makedirs(output_path, exist_ok=True)

    # Define o mapa de cores e a norma para os estados discretos
    cmap_colors = [ESTADO_MAPA_CORES[SUSCETIVEL], ESTADO_MAPA_CORES[INFECTADO], ESTADO_MAPA_CORES[RECUPERADO], ESTADO_MAPA_CORES[VAZIO]]
    cmap = ListedColormap(cmap_colors)
    norm = BoundaryNorm(ESTADOS + [VAZIO + 1], cmap.N)
    
    fig, ax = plt.subplots(figsize=(7, 6))
    
    img = ax.imshow(history[0], cmap=cmap, norm=norm)
    
    # Adiciona a legenda manual
    patches = [
        mpatches.Patch(color=ESTADO_MAPA_CORES[SUSCETIVEL], label='Suscetível'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[INFECTADO], label='Infectado'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[RECUPERADO], label='Recuperado'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[VAZIO], label='Vazio')
    ]
    ax.legend(handles=patches, loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)
    
    def update(frame):
        img.set_data(history[frame])
        ax.set_title(f'Passo de tempo: {frame}', fontsize=14)
        return [img]

    anim = FuncAnimation(fig, update, frames=len(history), interval=50, blit=True)
    anim.save(os.path.join(output_path, 'simulation.gif'), writer='pillow')
    plt.close(fig)

def calculate_box_counting_dimension(grid, thresholds=[1, 2, 4, 8, 16]):
    """
    Calcula a dimensão de box-counting para as células infectadas na grade.
    """
    infected_cells = np.argwhere(grid == INFECTADO)
    if infected_cells.size == 0:
        return 0
    
    num_boxes = []
    box_sizes = []
    
    for size in thresholds:
        boxes_with_cells = set()
        for x, y in infected_cells:
            box_x = x // size
            box_y = y // size
            boxes_with_cells.add((box_x, box_y))
        
        num_boxes.append(len(boxes_with_cells))
        box_sizes.append(1/size)
    
    log_N = np.log(num_boxes)
    log_r = np.log(box_sizes)
    
    if len(log_N) > 1:
        d = np.polyfit(log_r, log_N, 1)[0]
        return d
    else:
        return 0