from ga_controller import GAController
from snake import SnakeGame
import random
import numpy as np
import multiprocessing




def process_individual(individual: GAController):
    individual.reset_game()
    individual.set_display(False, individual.game)
    individual.game.run()
    return individual

class Population:
    def __init__(self, *, target: GAController, population_size: int, mutation_rate: float ) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.target = target
        self.population: list[GAController] = []

        for i in range(population_size):
            game = SnakeGame()
            controller = GAController(game, display=False)
            self.population.append(controller)
            game.run()

    def __iter__(self):
        return iter(self.population)

    def __getitem__(self, index):
        return self.population[index] 
    
    def __len__(self):
        return len(self.population)

    def mutate(self) -> None:
        for i in self.population:
            i.model.mutate(mutation_rate=self.mutation_rate)

            
    def debug(self) -> None:
        for i in sorted(self.population):
            print(i.DNA, i.fitness(self.target))

    def selection(self) -> None:
        self.population = sorted(self.population)
        self.population = self.population[len(self.population)//2:]
        while len(self.population) < self.population_size:
            parents = self.population[0].model.select_parents(self.population)  # Randomly pick two parents
            baby_model = parents[0].model + parents[1].model  # Use __add__ to combine parents
            game = SnakeGame()
            baby_controller = type(self.target)(game, display=False)
            baby_controller.model = baby_model  # Assign the new baby model
            self.population.append(baby_controller)

    

    def pop_apples(self) -> list[int]:
        apples = []
        for i in [agent.game.snake.apples for agent in self.population]:
            apples.append(i)
        return apples
    
    def best_fit(self) -> float:
        best = sorted(self.population)[-1]
        applesList = self.pop_apples()
        
        mean = np.mean(applesList)
        median = np.median(applesList)
        std = np.std(applesList)
        print(f'Fitness: {best.game.snake.fitness()}, Apples eaten: {best.game.snake.apples}, Moves: {best.game.snake.moves}')
        print(f'Mean: {mean}')
        print(f'Median: {median}')
        print(f'Standard Deviation: {std}\n')


        return best.game.snake.fitness()

    def best_agent(self) -> GAController:
        return sorted(self.population)[-1]
    
    
    
    def rerun(self): 
        # for i in self.population:
        #     i.reset_game()
        #     i.set_display(False, i.game)
        #     i.game.run()

         with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            # Map the processing function to each individual in the population
            self.population = pool.map(process_individual, self.population)


    

    

