#!/usr/bin/env python


from snake import SnakeGame
from ga_controller import GAController
from population import Population


if __name__ == '__main__':
    game = SnakeGame()
    target = GAController(game)
    pop = Population(target=target, population_size=10000, mutation_rate=0.02)
    print(f'Generation: {1}')

    i = 0
    global best_from_generation
    best_from_generation: list[GAController] = []

    while pop.best_fit() < 4.0:
        pop.mutate()
        pop.selection()
        pop.rerun()

        best = pop.best_agent()
        best_from_generation.append(best)
            
        i += 1
        print(f'Generation: {i+1}')
    


    best = best_from_generation[-1]
    for j in range(10):
        best.reset_game()
        best.set_display(True, best.game)
        best.game.run()

