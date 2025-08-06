import numpy as np
import pandas as pd
import json
from model import EpidemiaCA, ESTADOS, SUSCETIVEL, INFECTADO, RECUPERADO
from utils import plot_sir_curves, save_grid_animation

def load_parameters(filepath):
    """
    Carrega parâmetros de um arquivo JSON.
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def run_simulation(params):
    """
    Executa a simulação completa com os parâmetros fornecidos.
    """
    size = params['grid_size']
    initial_infected = params['initial_infected']
    inf_rate = params['infection_rate']
    rec_time = params['recovery_time']
    imm_loss_rate = params.get('immunity_loss_rate', 0.0)
    num_steps = params['num_steps']
    
    # NOVOS PARÂMETROS
    pop_density = params['population_density']
    move_rate = params['movement_rate']
    
    # A chamada ao construtor agora inclui os novos parâmetros
    model = EpidemiaCA(size, inf_rate, rec_time, imm_loss_rate, pop_density, move_rate)
    
    model.initialize_random_infection(initial_infected)
    
    history = []
    state_counts = {'susceptible': [], 'infected': [], 'recovered': []}
    
    for step in range(num_steps):
        model.step()
        history.append(model.grid.copy())
        
        counts = model.get_state_counts()
        state_counts['susceptible'].append(counts[SUSCETIVEL])
        state_counts['infected'].append(counts[INFECTADO])
        state_counts['recovered'].append(counts[RECUPERADO])
            
    return history, state_counts

def save_results(simulation_id, history, state_counts, output_dir="data/results"):
    """
    Salva os resultados da simulação em arquivos CSV e imagens.
    """
    import os
    results_path = os.path.join(output_dir, f"simulation_{simulation_id}")
    os.makedirs(results_path, exist_ok=True)
    
    # Salva os dados brutos da contagem de estados
    df_counts = pd.DataFrame(state_counts)
    df_counts.rename(columns={SUSCETIVEL: 'susceptible', INFECTADO: 'infected', RECUPERADO: 'recovered'}, inplace=True)
    df_counts.to_csv(os.path.join(results_path, "data.csv"), index=False)
    
    # Salva a grade final
    np.save(os.path.join(results_path, "final_grid.npy"), history[-1])
    
    print(f"Resultados da simulação {simulation_id} salvos em {results_path}")
    
    # Gera e salva as visualizações
    plot_sir_curves(df_counts, results_path)
    save_grid_animation(history, results_path)