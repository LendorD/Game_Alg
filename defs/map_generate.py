import random
import copy
import pygame
from .constants import MAP_WIDTH, MAP_HEIGHT, NUM_GENERATIONS, POPULATION_SIZE, MUTATION_RATE, WALL, EMPTY, FOOD, POISON, MOB, COLORS, MOB_ENERGY
from .classes import Mob, Wall, Poison, Food

pygame.init()
random.seed()


# Fitness function to evaluate the map
def evaluate_map(map_data):
    food_count = sum(row.count(FOOD) for row in map_data)
    poison_count = sum(row.count(POISON) for row in map_data)
    wall_count = sum(row.count(WALL) for row in map_data)
    empty_count = sum(row.count(EMPTY) for row in map_data)
    mob_count = sum(row.count(MOB) for row in map_data)

    # Example fitness function
    return food_count - poison_count + (empty_count / 10) - (wall_count / 20)


# Add random walls to the map
def add_random_walls(map_data):
    num_walls = random.randint(10, 30)  # Adjust the number of walls as needed
    for _ in range(num_walls):
        wall_length = random.randint(2, 10)
        start_x = random.randint(1, MAP_WIDTH - 2)
        start_y = random.randint(1, MAP_HEIGHT - 2)
        direction = random.choice(['horizontal', 'vertical'])
        for _ in range(wall_length):
            if 1 <= start_x < MAP_WIDTH - 1 and 1 <= start_y < MAP_HEIGHT - 1:
                if map_data[start_y][start_x] == EMPTY:  # Ensure wall only replaces empty space
                    map_data[start_y][start_x] = WALL
                if direction == 'horizontal':
                    if random.random() < 0.7:
                        start_x += random.choice([-1, 1])  # Mostly continue in the same direction
                    else:
                        direction = 'vertical'  # Occasionally change direction
                else:
                    if random.random() < 0.7:
                        start_y += random.choice([-1, 1])  # Mostly continue in the same direction
                    else:
                        direction = 'horizontal'  # Occasionally change direction


# Create initial population of maps with walls around the edges and few special items
def create_initial_population():
    population = []
    for _ in range(POPULATION_SIZE):
        map_data = []
        for y in range(MAP_HEIGHT):
            row = []
            for x in range(MAP_WIDTH):
                if x == 0 or x == MAP_WIDTH - 1 or y == 0 or y == MAP_HEIGHT - 1:
                    row.append(WALL)
                else:
                    row.append(EMPTY)
            map_data.append(row)
        add_random_walls(map_data)
        for y in range(1, MAP_HEIGHT - 1):
            for x in range(1, MAP_WIDTH - 1):
                if map_data[y][x] == EMPTY:
                    rand_val = random.random()
                    if rand_val < 0.01:
                        map_data[y][x] = FOOD
                    elif rand_val < 0.02:
                        map_data[y][x] = POISON
                    elif rand_val < 0.03:
                        map_data[y][x] = MOB
        population.append(map_data)
    return population


# Selection function to select parents based on fitness
def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [fitness / total_fitness for fitness in fitnesses]
    parent1 = population[random.choices(range(POPULATION_SIZE), weights=selection_probs, k=1)[0]]
    parent2 = population[random.choices(range(POPULATION_SIZE), weights=selection_probs, k=1)[0]]
    return parent1, parent2


# Crossover function to create a child map from two parents
def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if not (i == 0 or i == MAP_HEIGHT - 1 or j == 0 or j == MAP_WIDTH - 1):  # Skip the borders
                if random.random() < 0.5:
                    child[i][j] = parent2[i][j]
    return child


# Mutation function to introduce random changes in the map
def mutate(map_data):
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if not (i == 0 or i == MAP_HEIGHT - 1 or j == 0 or j == MAP_WIDTH - 1):  # Skip the borders
                if random.random() < MUTATION_RATE:
                    rand_val = random.random()
                    if rand_val < 0.01:
                        map_data[i][j] = FOOD
                    elif rand_val < 0.02:
                        map_data[i][j] = POISON
                    elif rand_val < 0.03:
                        map_data[i][j] = MOB
                    elif rand_val < 0.10:
                        map_data[i][j] = WALL
                    else:
                        map_data[i][j] = EMPTY
    return map_data


# Genetic algorithm to evolve maps
def genetic_algorithm():
    population = create_initial_population()
    for generation in range(NUM_GENERATIONS):
        fitnesses = [evaluate_map(map_data) for map_data in population]
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent1, parent2 = select_parents(population, fitnesses)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)
        population = new_population

    # Select the best map
    fitnesses = [evaluate_map(map_data) for map_data in population]
    best_map = population[fitnesses.index(max(fitnesses))]
    return best_map


# Function to save the generated map to an image
def save_map_to_image(map_data, file_path):
    width = len(map_data[0])
    height = len(map_data)
    map_surface = pygame.Surface((width, height), depth = 32)  # Use 32-bit color depth
    map_surface = map_surface.convert_alpha()  # Convert to alpha surface for transparency support
    for y in range(height):
        for x in range(width):
            color = (255, 255, 255)  # Default color is white
            if map_data[y][x] == WALL:
                color = (0, 0, 0)
            elif map_data[y][x] == FOOD:
                color = (0, 255, 0)
            elif map_data[y][x] == POISON:
                color = (255, 0, 0)
            elif map_data[y][x] == MOB:
                color = (0, 0, 255)
            map_surface.set_at((x, y), color)
    pygame.image.save(map_surface, file_path)


# Main function to generate and save the map
def generate_map_gen_al():
    pygame.display.set_mode((1, 1))  # Set video mode to initialize Pygame
    best_map = genetic_algorithm()
    save_map_to_image(best_map, 'img/generated_map.png')


def draw_map(map_img, all_gen):  # функция отрисовки карты из карты.пнг (лежит в папке img)
    obj_map = []
    all_emp_cells = int(0)
    for i in range(0, map_img.get_width()):
        s = []
        for j in range(0, map_img.get_height()):
            _obj = None
            if map_img.get_at([i, j]) == pygame.color.Color(0, 0, 0):  # определяя цвет на рисунке, мы расставляем мобов
                _obj = Wall(i, j)  # стены, яд и еду
            elif map_img.get_at([i, j]) == pygame.color.Color(255, 0, 0):
                r = random.randint(1, 2)
                if r == 1:
                    _obj = Poison(i, j)
                else:
                    _obj = Food(i, j)
            elif map_img.get_at([i, j]) == pygame.color.Color(0, 0, 255):
                _obj = Mob(i, j, all_gen[0], i * j + i + j,
                           (sum(all_gen[0]) % 140, sum(all_gen[0]) % 55, sum(all_gen[0]) % 255), MOB_ENERGY)
                all_gen.pop(0)  # удаляем из пула генов, ген, который использовали
            elif map_img.get_at([i, j]) == pygame.color.Color(255, 255, 255):
                all_emp_cells += 1
            s.append(_obj)
        obj_map.append(s)
    # print(all_emp_cells)
    return obj_map
