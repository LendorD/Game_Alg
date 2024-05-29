import random
import os

random.seed()
game_folder = os.path.dirname(os.path.dirname(__file__))  # Определение пути с игрой


def generate_matrix(rows, cols):
    return [[random.randint(0, 35) for _ in range(cols)] for _ in range(rows)]


def save_matrix_to_file(matrix, filename):
    with open(filename, encoding = 'utf-8', mode = 'w') as file:
        for row in matrix:
            file.write(' '.join(str(num) for num in row) + '\n')


def gen_create():  # Используется ли???
    for i in range(1, 6):
        matrix = generate_matrix(6, 6)
        filename = f'gen/gen{i}.txt'
        save_matrix_to_file(matrix, filename)


def all_gen_generate():
    all_gen = []  # здесь мы из файлов gen1-5 считываем гены в список, чтоб потом раздать их
    for i in range(1, 6):
        file = open(os.path.join(game_folder, 'gen') + '/gen' + str(i) + '.txt', 'r')
        s = []
        for line in file:
            numbers = line.strip().replace('\t', ' ').split(' ')
            for number in numbers:
                if number:
                    s.append(int(number))
        all_gen.append(s)
        file.close()
    return all_gen
