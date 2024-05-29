import random
import pygame
import os
import sys
import copy
import csv
from defs.constants import *
from defs.gen_generate import gen_create, all_gen_generate, game_folder
from defs.classes import Mob, Food, Poison
from map_generate import generate_map_gen_al, draw_map

def generate_unique_id():
    return random.randint(0, 9999)

pygame.init()  # инициализация библиотеки
generate_map_gen_al()
img_folder = os.path.join(game_folder, 'img')  # Определение пути к пнг файлам
map_img = pygame.image.load(os.path.join(img_folder, 'generated_map.png'))  # путь к карте

gen_create()
all_gen = all_gen_generate()
last_gens = copy.deepcopy(all_gen)  # список с выжившими мобами
all_gen *= SIZE_POPULATION  # умножаем, чтоб сделать 50 генов
random.shuffle(all_gen)  # мешаем их, чтоб потом раздать в случайном порядке

screen = pygame.display.set_mode((1500, 950))  # наше окно с симуляцией
clock = pygame.time.Clock()
all_obj = draw_map(map_img, all_gen)

while evo_life < 100000:
    for event in pygame.event.get():  # закрытие окна
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # клик по мобу, чтоб вызвать сведения о нем
            try:
                obj = all_obj[event.pos[0] // SIZE_CELL][event.pos[1] // SIZE_CELL]

                if event.button == 1:
                    print('click (x: %s y: %s)' % (event.pos[0] // SIZE_CELL, event.pos[1] // SIZE_CELL))
                    print(obj)

            except IndexError:
                pass

        elif event.type == pygame.MOUSEWHEEL:  # круть колесико, чтоб изменить скорость
            current_ticks += (event.y * 10)
            if current_ticks < 1:
                current_ticks = 1

    f = open('data.csv', 'a', encoding='UTF8', newline='')  # собираем инфу для графиков
    writer = csv.writer(f)

    screen.fill(pygame.color.Color(180, 180, 180))

    evo_life += 1

    mob_survived = []

    for i in range(0, map_img.get_width()):  # поклеточная отрисовка и логика
        for j in range(0, map_img.get_height()):
            if all_obj[i][j] is not None:
                if type(all_obj[i][j]) is Mob:
                    mob_survived.append(all_obj[i][j])
                    all_obj[i][j].sees = all_obj[all_obj[i][j].look[0]][all_obj[i][j].look[1]]
                    if all_obj[i][j].life <= evo_life:
                        all_obj[i][j].life += 1
                        all_obj[i][j].update(all_obj)
            else:
                if random.randint(1, 2000) == 1:
                    if random.randint(1, 10) == 1:
                        all_obj[i][j] = Poison(i, j)
                    else:
                        all_obj[i][j] = Food(i, j)

    for i in range(0, map_img.get_width()):
        for j in range(0, map_img.get_height()):
            if all_obj[i][j] is not None:
                pygame.draw.rect(screen, all_obj[i][j].colour, pygame.Rect(all_obj[i][j].coordinates[0] * SIZE_CELL + 1,
                                                                           all_obj[i][j].coordinates[1] * SIZE_CELL + 1,
                                                                           SIZE_OBJ, SIZE_OBJ))

    for mob in mob_survived:
        mob.sees = all_obj[mob.look[0]][mob.look[1]]
        if mob.life <= evo_life:
            mob.life += 1
            mob.update(all_obj)

        # Check if a mob has enough energy to reproduce
        if mob.energy >= REPRODUCTION_ENERGY or mob.life > SEX_AGE:
            # Create a new mob with mutated genes
            new_gen = copy.deepcopy(mob.gen)
            for _ in range(3):  # Increase mutation frequency
                r1 = random.randint(0, COMMAND_AMOUNT)
                r2 = random.randint(1, COMMAND_AMOUNT + 1)
                new_gen[r1] = r2 - 1
            offspring = Mob(mob.coordinates[0], mob.coordinates[1], new_gen, generate_unique_id(), (255,255,255))
            all_obj[mob.coordinates[0]][mob.coordinates[1]] = offspring
            mob.energy -= REPRODUCTION_ENERGY  # Deduct energy for reproduction

    # print(evo_years)

    if len(mob_survived) <= 5:  # работа с выжившими генами
        all_gen = []
        evo_years += 1
        # print(evo_years)

        mob_s_text = " | "
        if len(mob_survived) > 0:
            for i in range(5):
                all_gen.append(mob_survived[i % len(mob_survived)].gen)
                mob_s_text += "%s (%s)   " % (
                    mob_survived[i % len(mob_survived)].energy, sum((mob_survived[i % len(mob_survived)].gen)))

            last_gens = copy.deepcopy(all_gen)

        else:
            all_gen = copy.deepcopy(last_gens)

        for i in range(5):
            for j in range(SIZE_POPULATION - 1):
                all_gen.append(copy.deepcopy(all_gen[i]))

        for i in range(5):  # тут происходит мутация трех случайных команд, у каждого пяти мобов с разными генами
            for j in range(3):
                r1 = random.randint(0, COMMAND_AMOUNT)
                r2 = random.randint(1, COMMAND_AMOUNT + 1)
                # print('all_gen', all_gen[i], len(all_gen), len(all_gen[i]))
                all_gen[i][r1] = r2 - 1

        random.shuffle(all_gen)  # опять мешаем гены, чтоб потом раздать
        #print(evo_years, mob_s_text, evo_life)
        writer.writerow([evo_life])
        f.flush()
        evo_life = 0

    f.close()
    pygame.display.flip()
    clock.tick(current_ticks)
