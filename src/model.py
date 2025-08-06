import numpy as np

# Constantes para os estados das células
# Adicionamos o estado VAZIO para representar espaços sem indivíduos
SUSCETIVEL = 0
INFECTADO = 1
RECUPERADO = 2
VAZIO = 3

ESTADOS = [SUSCETIVEL, INFECTADO, RECUPERADO, VAZIO]
ESTADO_MAPA_CORES = {
    SUSCETIVEL: 'blue',
    INFECTADO: 'red',
    RECUPERADO: 'green',
    VAZIO: 'black'
}

class EpidemiaCA:
    """
    Simula a propagação de uma epidemia usando autômatos celulares com
    movimento de indivíduos.
    """
    def __init__(self, size, inf_rate, rec_time, imm_loss_rate, pop_density, move_rate):
        self.size = size
        self.inf_rate = inf_rate
        self.rec_time = rec_time
        self.imm_loss_rate = imm_loss_rate
        self.pop_density = pop_density
        self.move_rate = move_rate
        
        self.grid = np.zeros((size, size), dtype=int)
        self.infected_duration = np.zeros((size, size), dtype=int)
        self.immune_duration = np.zeros((size, size), dtype=int)

        self.initialize_population()

    def initialize_population(self):
        """
        Inicializa a grade com indivíduos (Suscetíveis) e espaços vazios
        de acordo com a densidade populacional.
        """
        num_cells = self.size * self.size
        num_individuals = int(num_cells * self.pop_density)
        
        flat_indices = np.random.choice(num_cells, num_cells - num_individuals, replace=False)
        empty_indices = np.unravel_index(flat_indices, (self.size, self.size))
        self.grid[empty_indices] = VAZIO

    def initialize_random_infection(self, num_infected):
        """
        Inicia a simulação com um número 'num_infected' de indivíduos
        infectados, escolhendo apenas entre as células que são indivíduos.
        """
        individuals_indices = np.argwhere(self.grid != VAZIO)
        if len(individuals_indices) < num_infected:
            raise ValueError("O número de infectados é maior que a população de indivíduos.")
        
        chosen_indices = np.random.choice(len(individuals_indices), num_infected, replace=False)
        for idx in chosen_indices:
            x, y = individuals_indices[idx]
            self.grid[x, y] = INFECTADO
            self.infected_duration[x, y] = 0

    def step(self):
        """
        Avança a simulação em um passo de tempo, aplicando as regras de movimento e transição.
        """
        # 1. Passo de Movimento: Apenas uma porcentagem dos indivíduos se move
        self.move_individuals()
        
        # 2. Passo de Transição: Infecção, recuperação, etc.
        new_grid = self.grid.copy()
        
        for i in range(self.size):
            for j in range(self.size):
                state = self.grid[i, j]

                if state == SUSCETIVEL:
                    infected_neighbors = 0
                    for x in range(max(0, i - 1), min(self.size, i + 2)):
                        for y in range(max(0, j - 1), min(self.size, j + 2)):
                            if self.grid[x, y] == INFECTADO:
                                infected_neighbors += 1

                    if infected_neighbors > 0:
                        prob_infection = 1 - (1 - self.inf_rate)**infected_neighbors
                        if np.random.rand() < prob_infection:
                            new_grid[i, j] = INFECTADO
                            self.infected_duration[i, j] = 0

                elif state == INFECTADO:
                    self.infected_duration[i, j] += 1
                    if self.infected_duration[i, j] >= self.rec_time:
                        new_grid[i, j] = RECUPERADO
                        self.infected_duration[i, j] = 0
                        self.immune_duration[i, j] = 0
                
                elif state == RECUPERADO:
                    if self.imm_loss_rate > 0:
                         self.immune_duration[i, j] += 1
                         if self.immune_duration[i, j] >= 1 / self.imm_loss_rate:
                             new_grid[i, j] = SUSCETIVEL
                             self.immune_duration[i, j] = 0
        
        self.grid = new_grid

    def move_individuals(self):
        """
        Permite que os indivíduos se movam para células vazias adjacentes.
        """
        individuals_to_move = np.argwhere(self.grid != VAZIO)
        
        # Embaralha os indivíduos para que a ordem de movimento seja aleatória
        np.random.shuffle(individuals_to_move)

        for i, j in individuals_to_move:
            if np.random.rand() < self.move_rate:
                # Encontra vizinhos vazios
                empty_neighbors = []
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        if x_offset == 0 and y_offset == 0:
                            continue
                        
                        ni, nj = i + x_offset, j + y_offset
                        
                        if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni, nj] == VAZIO:
                            empty_neighbors.append((ni, nj))
                
                # Se houver vizinhos vazios, move para um aleatório
                if empty_neighbors:
                    ni, nj = empty_neighbors[np.random.randint(len(empty_neighbors))]
                    
                    # Move o indivíduo e atualiza os contadores
                    self.grid[ni, nj] = self.grid[i, j]
                    self.grid[i, j] = VAZIO
                    
                    self.infected_duration[ni, nj] = self.infected_duration[i, j]
                    self.infected_duration[i, j] = 0
                    
                    self.immune_duration[ni, nj] = self.immune_duration[i, j]
                    self.immune_duration[i, j] = 0
    
    def get_state_counts(self):
        """
        Retorna a contagem de cada estado (S, I, R) na grade atual.
        O estado VAZIO é ignorado na contagem para o gráfico SIR.
        """
        counts = {
            SUSCETIVEL: np.sum(self.grid == SUSCETIVEL),
            INFECTADO: np.sum(self.grid == INFECTADO),
            RECUPERADO: np.sum(self.grid == RECUPERADO),
            VAZIO: np.sum(self.grid == VAZIO)
        }
        return counts