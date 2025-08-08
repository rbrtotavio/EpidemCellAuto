import numpy as np

# Constantes para os estados das células
SUSCETIVEL = 0
EXPOSTO = 1
INFECTADO = 2
RECUPERADO = 3
VAZIO = 4

ESTADOS = [SUSCETIVEL, EXPOSTO, INFECTADO, RECUPERADO, VAZIO]
ESTADO_MAPA_CORES = {
    SUSCETIVEL: 'blue',
    EXPOSTO: 'yellow',
    INFECTADO: 'red',
    RECUPERADO: 'green',
    VAZIO: 'black'
}

class EpidemiaCA:
    def __init__(self, size, inf_rate, rec_time, exposed_time, imm_loss_rate, pop_density, move_rate):
        
        self.size = size
        self.inf_rate = inf_rate
        self.rec_time = rec_time
        self.exposed_time = exposed_time
        self.imm_loss_rate = imm_loss_rate
        self.pop_density = pop_density
        self.move_rate = move_rate
        
        self.grid = np.zeros((size, size), dtype=int)
        self.infected_duration = np.zeros((size, size), dtype=int)
        self.exposed_duration = np.zeros((size, size), dtype=int)
        self.immune_duration = np.zeros((size, size), dtype=int)

        self.initialize_population()

    def initialize_population(self):
        num_cells = self.size * self.size
        num_individuals = int(num_cells * self.pop_density)
        
        flat_indices = np.random.choice(num_cells, num_cells - num_individuals, replace=False)
        empty_indices = np.unravel_index(flat_indices, (self.size, self.size))
        self.grid[empty_indices] = VAZIO

    def initialize_random_infection(self, num_infected):
        individuals_indices = np.argwhere(self.grid != VAZIO)
        if len(individuals_indices) < num_infected:
            raise ValueError("O número de infectados é maior que a população de indivíduos.")
        
        chosen_indices = np.random.choice(len(individuals_indices), num_infected, replace=False)
        for idx in chosen_indices:
            x, y = individuals_indices[idx]
            self.grid[x, y] = EXPOSTO
            self.exposed_duration[x, y] = 0

    def step(self):
        self.move_individuals()
        
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
                            new_grid[i, j] = EXPOSTO
                            self.exposed_duration[i, j] = 0
                
                elif state == EXPOSTO:
                    self.exposed_duration[i, j] += 1
                    if self.exposed_duration[i, j] >= self.exposed_time:
                        new_grid[i, j] = INFECTADO
                        self.exposed_duration[i, j] = 0
                
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
        individuals_to_move = np.argwhere(self.grid != VAZIO)
        
        np.random.shuffle(individuals_to_move)

        for i, j in individuals_to_move:
            if np.random.rand() < self.move_rate:
                empty_neighbors = []
                for x_offset in [-1, 0, 1]:
                    for y_offset in [-1, 0, 1]:
                        if x_offset == 0 and y_offset == 0:
                            continue
                        
                        ni, nj = i + x_offset, j + y_offset
                        
                        if 0 <= ni < self.size and 0 <= nj < self.size and self.grid[ni, nj] == VAZIO:
                            empty_neighbors.append((ni, nj))
                
                if empty_neighbors:
                    ni, nj = empty_neighbors[np.random.randint(len(empty_neighbors))]
                    
                    self.grid[ni, nj] = self.grid[i, j]
                    self.grid[i, j] = VAZIO
                    
                    self.exposed_duration[ni, nj] = self.exposed_duration[i, j]
                    self.exposed_duration[i, j] = 0
                    
                    self.infected_duration[ni, nj] = self.infected_duration[i, j]
                    self.infected_duration[i, j] = 0
                    
                    self.immune_duration[ni, nj] = self.immune_duration[i, j]
                    self.immune_duration[i, j] = 0
    
    def get_state_counts(self):
        counts = {
            SUSCETIVEL: np.sum(self.grid == SUSCETIVEL),
            EXPOSTO: np.sum(self.grid == EXPOSTO),
            INFECTADO: np.sum(self.grid == INFECTADO),
            RECUPERADO: np.sum(self.grid == RECUPERADO),
            VAZIO: np.sum(self.grid == VAZIO)
        }
        return counts