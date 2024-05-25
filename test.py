import random

SIZE_POPULATION = 20


def generate_matrix(rows, cols):
    return [[random.randint(0, 35) for _ in range(cols)] for _ in range(rows)]


def save_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(str(num) for num in row) + '\n')


for i in range(1, 6):
    matrix = generate_matrix(6, 6)
    filename = f'gen/gen{i}.txt'
    save_matrix_to_file(matrix, filename)
    print(f'Matrix saved to {filename}')


print(matrix)

all_gen = []  # здесь мы из файлов gen1-5 считываем гены в список, чтоб потом раздать их
for i in range(1, 6):
    file = open('gen/gen' + str(i) + '.txt', 'r')
    s = []
    for line in file:
        numbers = line.strip().replace('\t', ' ').split(' ')
        for number in numbers:
            if number:
                s.append(int(number))
    all_gen.append(s)
    file.close()

for line in all_gen:
    print(line)
all_gen *= SIZE_POPULATION  # умножаем, чтоб сделать 50 генов
random.shuffle(all_gen)  # мешаем их, чтоб потом раздать в случайном порядке
print()
for line in all_gen:
    print(line)