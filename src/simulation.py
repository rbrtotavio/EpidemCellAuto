import os
import numpy as np
import pandas as pd
import json
from model import EpidemiaCA, SUSCETIVEL, EXPOSTO, INFECTADO, RECUPERADO
from utils import plot_seir_curves, save_grid_animation

def load_parameters(filepath):
    """
    Carrega parâmetros de um arquivo JSON.
    """
    with open(filepath, 'r') as f:
        return json.load(f)
    
def save_metadata_to_json(simulation_id, params, box_counting_dim, output_dir):
    """
    Salva os parâmetros da simulação e a dimensão de box-counting
    em um arquivo JSON.
    """
    results_path = os.path.join(output_dir, f"simulation_{simulation_id}")
    metadata = {
        "simulation_parameters": params,
        "box_counting_dimension": box_counting_dim
    }
    with open(os.path.join(results_path, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=4)

def run_simulation(params):
    random_seed = params['random_seed']
    np.random.seed(random_seed)
    
    size = params['grid_size']
    initial_infected = params['initial_infected']
    inf_rate = params['infection_rate']
    rec_time = params['recovery_time']
    imm_loss_rate = params.get('immunity_loss_rate', 0.0)
    num_steps = params['num_steps']
    pop_density = params['population_density']
    move_rate = params['movement_rate']
    exposed_time = params['exposed_time']
    
    model = EpidemiaCA(size, inf_rate, rec_time, exposed_time, imm_loss_rate, pop_density, move_rate)
    model.initialize_random_infection(initial_infected)
    
    history = []
    state_counts = {'susceptible': [], 'exposed': [], 'infected': [], 'recovered': []}
    
    for step in range(num_steps):
        model.step()
        history.append(model.grid.copy())
        
        counts = model.get_state_counts()
        state_counts['susceptible'].append(counts[SUSCETIVEL])
        state_counts['exposed'].append(counts[EXPOSTO])
        state_counts['infected'].append(counts[INFECTADO])
        state_counts['recovered'].append(counts[RECUPERADO])
            
    return history, state_counts

def save_results(simulation_id, history, state_counts, params, box_counting_dim, output_dir="data/results"):
    """
    Salva os resultados da simulação em arquivos CSV e imagens,
    adaptado para o modelo SEIR.
    """
    results_path = os.path.join(output_dir, f"simulation_{simulation_id}")
    os.makedirs(results_path, exist_ok=True)
    
    save_metadata_to_json(simulation_id, params, box_counting_dim, output_dir)
    
    df_counts = pd.DataFrame(state_counts)
    
    total_pop = params['grid_size'] * params['grid_size']
    plot_seir_curves(df_counts, results_path, total_pop)
    
    df_counts.rename(columns={
        SUSCETIVEL: 'susceptible',
        EXPOSTO: 'exposed',
        INFECTADO: 'infected',
        RECUPERADO: 'recovered'
    }, inplace=True)
    df_counts.to_csv(os.path.join(results_path, "data.csv"), index=False)

    np.save(os.path.join(results_path, "final_grid.npy"), history[-1])
    
    print(f"Resultados da simulação {simulation_id} salvos em {results_path}")
    
    save_grid_animation(history, results_path)