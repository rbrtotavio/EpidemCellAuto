import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os
import pandas as pd
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches

from model import SUSCETIVEL, INFECTADO, RECUPERADO, VAZIO, ESTADOS, ESTADO_MAPA_CORES, EXPOSTO

def plot_seir_curves(df_counts, output_path, total_pop):
    """
    Plota e salva as curvas de Suscetível, Exposto, Infectado e Recuperado,
    mantendo a escala do eixo Y consistente.
    """
    os.makedirs(output_path, exist_ok=True)

    plt.figure(figsize=(10, 6))
    
    df_fractions = df_counts.copy()
    df_fractions = df_fractions / total_pop
    
    plt.plot(df_fractions['susceptible'], label='Suscetível', color=ESTADO_MAPA_CORES[SUSCETIVEL], linewidth=2)
    plt.plot(df_fractions['exposed'], label='Exposto', color=ESTADO_MAPA_CORES[EXPOSTO], linewidth=2)
    plt.plot(df_fractions['infected'], label='Infectado', color=ESTADO_MAPA_CORES[INFECTADO], linewidth=2)
    plt.plot(df_fractions['recovered'], label='Recuperado', color=ESTADO_MAPA_CORES[RECUPERADO], linewidth=2)
    
    plt.ylim(0, 1.0)
    
    plt.title('Dinâmica da Epidemia (SEIRS)')
    plt.xlabel('Passos de Tempo')
    plt.ylabel('Fração da População')
    
    patches = [
        mpatches.Patch(color=ESTADO_MAPA_CORES[SUSCETIVEL], label='Suscetível'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[EXPOSTO], label='Exposto'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[INFECTADO], label='Infectado'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[RECUPERADO], label='Recuperado')
    ]
    plt.legend(handles=patches)
    
    plt.grid(True)
    plt.savefig(os.path.join(output_path, "seir_curves.png"))
    plt.close()


def save_grid_animation(history, output_path):
    """
    Cria e salva uma animação da grade com uma legenda manual.
    """
    os.makedirs(output_path, exist_ok=True)

    cmap_colors = [ESTADO_MAPA_CORES[SUSCETIVEL], ESTADO_MAPA_CORES[EXPOSTO], ESTADO_MAPA_CORES[INFECTADO], ESTADO_MAPA_CORES[RECUPERADO], ESTADO_MAPA_CORES[VAZIO]]
    cmap = ListedColormap(cmap_colors)
    norm = BoundaryNorm(ESTADOS + [VAZIO + 1], cmap.N)
    
    fig, ax = plt.subplots(figsize=(9, 6))
    
    img = ax.imshow(history[0], cmap=cmap, norm=norm)
    
    patches = [
        mpatches.Patch(color=ESTADO_MAPA_CORES[SUSCETIVEL], label='Suscetível'),
        mpatches.Patch(color=ESTADO_MAPA_CORES[EXPOSTO], label='Exposto'),
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