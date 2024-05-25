SIZE_CELL = 14  # Размер клетки (для отрисовки)

SIZE_OBJ = 10  # Размер объекта (для отрисовки)

SIZE_POPULATION = 1000  # Размер популяции на один ген

# тут мы для удобства сделали команды константами
MOB_TURN_LEFT, MOB_TURN_RIGHT, MOB_LOOK, MOB_TRANSFORM, MOB_EAT, MOB_GO = 0, 1, 2, 3, 4, 5

# столько дается энергии за съеденную еду
FOOD_ENERGY_BOOST, MOB_ENERGY = 10, 100

# кол-во команд всего (изначально их было 64)
COMMAND_AMOUNT, MOB_FREE_COMMAND = 35, 13

current_ticks = 10  # условно, скорость отрисовки
evo_life = 0  # кол-во раундов в одной симуляции
evo_years = 0  # кол-во симуляций

# Constants for the map
MAP_WIDTH = 102
MAP_HEIGHT = 52
NUM_GENERATIONS = 100
POPULATION_SIZE = 20
MUTATION_RATE = 0.1

# Constants for objects on the map
WALL = 0
EMPTY = 1
FOOD = 2
POISON = 3
MOB = 4

# Colors for objects
COLORS = {
    WALL:   (0, 0, 0),
    EMPTY:  (255, 255, 255),
    FOOD:   (255, 0, 0),
    POISON: (0, 0, 255),
    MOB:    (0, 255, 0)
}
