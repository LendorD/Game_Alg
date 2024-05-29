import random
from .constants import MOB_GO, MOB_TURN_LEFT, MOB_TURN_RIGHT, MOB_EAT, MOB_LOOK, MOB_TRANSFORM, FOOD_ENERGY_BOOST, MOB_FREE_COMMAND


def map_move(the_obj, where, all_obj: list):  # тут происходит отрисовка и передвижение мобов на карте
    if all_obj[where[0]][where[1]] is None:
        map_remove(the_obj, all_obj)
        the_obj.coordinates = where
        all_obj[where[0]][where[1]] = the_obj
        the_obj.look = the_obj.get_look()


def map_remove(the_obj, all_obj: list):  # удаляем объекты с карты
    all_obj[the_obj.coordinates[0]][the_obj.coordinates[1]] = None


def map_transform(the_obj, all_obj: list):  # изменение яда на еду (вызывают мобы)
    all_obj[the_obj.coordinates[0]][the_obj.coordinates[1]] = Food(the_obj.coordinates[0], the_obj.coordinates[1])


class Mob:
    def __init__(self, x, y, gen, id, colour=(255, 255, 255), energy: int = 20, life: int = 0):
        self.coordinates = [x, y]
        self.id = id
        self.orientation = random.randint(0, 7)  # изначально задается случайное направление куда он смотрит
        self.gen = gen  # генотип моба
        self.counter = 0  # счетчик, указывающий на текущую команду
        self.look = self.get_look()  # объект на который он смотрит
        self.sees = None
        self.direction(0)
        self.energy = energy
        self.colour = colour
        self.life = life  # кол-во прожитых раундов

    def __str__(self):  # позволяет вывести инфу о мобе, если тык в него на карте
        return "> id: %s\n> look: %s\tsees: %s\n> energy: %s\n> command: %s\ngen: %s\ngenotype: %s\n life: %s\n coor: %s" % (
            self.id, self.look, self.sees, self.energy, self.gen[self.counter], self.gen, sum(self.gen), self.life,
            self.coordinates)

    def next_counter(self, all_obj: list, rec = 0):  # тут происходит управление счетчиком
        temp_count = self.counter

        if self.gen[self.counter] < MOB_FREE_COMMAND or rec >= 10:  # если команда, означает какое-то действие
            if self.gen[self.counter] != MOB_LOOK:
                temp_count += 1

            else:
                can_see = [Food, Mob, Wall, Poison]
                for j in range(0, len(can_see)):
                    if type(self.sees) is can_see[j]:
                        temp_count += (j + 2)
                        break
                else:
                    temp_count += 1
            self.counter = temp_count % len(self.gen)
            self.energy -= 1

        else:  # команды 13-31
            temp_count += self.gen[self.counter]
            self.counter = temp_count % len(self.gen)
            self.update(all_obj, rec + 1)

    def update(self, all_obj: list, rec=0):
        # Проверяем, видна ли еда, и если да, то в первую очередь её едим
        if self.sees is not None and isinstance(self.sees, Food):
            self.eat(all_obj)
        else:
            # Если еда не видна, продолжаем с обычными действиями
            status = self.gen[self.counter]
            if MOB_GO + 8 > status >= MOB_GO:
                self.move(status - MOB_GO, all_obj)
            elif status == MOB_LOOK:
                pass
            elif status == MOB_TRANSFORM:
                self.transform_poison(all_obj)
            elif status == MOB_TURN_RIGHT:
                self.direction(1)
            elif status == MOB_TURN_LEFT:
                self.direction(-1)

            # Добавляем случайный поворот
            if random.random() < 0.2:  # Например, шанс поворота 20%
                self.direction(random.choice([-1, 1]))
        if self.life >= 50:
            print("died")
            map_remove(self, all_obj)  # Удаляем моба из карты
            return
        # Выполняем остальные действия и обновляем счетчики
        self.next_counter(all_obj, rec)
        self.look = self.get_look()
        if self.energy <= 0:
            print("0 energy")
            map_remove(self, all_obj)

    def can_be_eaten(self, by_obj):
        if self.energy < by_obj.energy:
            return by_obj.energy - self.energy
        else:
            return 0

    def eat(self, all_obj: list):  # КУСЬ (если можем)
        if self.sees is not None:
            if self.sees.can_be_eaten(self):

                if type(self.sees) is Food:
                    self.energy += FOOD_ENERGY_BOOST
                    map_remove(self.sees, all_obj)
                elif type(self.sees) is Poison:
                    self.energy += FOOD_ENERGY_BOOST
                    map_remove(self, all_obj)

    def move(self, where, all_obj: list):  # передвижение, а так же если мы наступаем в еду или яд, мы ее кусаем
        self.life += 1
        self.eat(all_obj)
        next_position = self.get_look(orientation = where)
        if not self.check_wall_collision(next_position, all_obj):
            map_move(self, next_position, all_obj)

    def check_wall_collision(self, next_position, all_obj):
        x, y = next_position
        if x < 0 or x >= len(all_obj) or y < 0 or y >= len(all_obj[0]) or isinstance(all_obj[x][y], Wall):
            # Попытка движения в обратном направлении
            opposite_direction = (self.orientation + 4) % 8
            opposite_position = self.get_look(orientation = opposite_direction)
            opposite_x, opposite_y = opposite_position
            if not (opposite_x < 0 or opposite_x >= len(all_obj) or opposite_y < 0 or opposite_y >= len(
                    all_obj[0]) or isinstance(all_obj[opposite_x][opposite_y], Wall)):
                # Поворачиваем моб на 180 градусов и двигаем его в обратном направлении
                self.direction(4)
                return False
            else:
                # Иначе продолжаем двигаться вперед
                self.direction(0)
                return True
        return False

    def transform_poison(self, all_obj: list):  # вызов функции превращения яда в еду
        if type(self.sees) is Poison:
            map_transform(self.sees, all_obj)

    # эта функция позволяет нам определить куда смотрит клетка, когда крутится
    def get_look(self, coordinates: list = None, orientation = None):

        if orientation is None:
            orientation = self.orientation

        if coordinates is None:
            x, y = self.coordinates[0], self.coordinates[1]
        else:
            x, y = coordinates[0], coordinates[1]

        if orientation == 0:
            return [x, y + 1]
        elif orientation == 1:
            return [x + 1, y + 1]
        elif orientation == 2:
            return [x + 1, y]
        elif orientation == 3:
            return [x + 1, y - 1]
        elif orientation == 4:
            return [x, y - 1]
        elif orientation == 5:
            return [x - 1, y - 1]
        elif orientation == 6:
            return [x - 1, y]
        elif orientation == 7:
            return [x - 1, y + 1]

    def direction(self, arg: int):
        self.orientation = (self.orientation + arg) % 8


class Wall:
    def __init__(self, x, y):
        self.coordinates = [x, y]
        self.id = 2
        self.colour = (31, 52, 56)

    def can_be_eaten(self, by_obj):
        return 0


class Food:
    def __init__(self, x, y):
        self.coordinates = [x, y]
        self.id = 3
        self.colour = (235, 235, 97)

    def can_be_eaten(self, by_obj):  # функция позволяющая узнать, можно ли кусь этот объект
        return FOOD_ENERGY_BOOST


class Poison:
    def __init__(self, x, y):
        self.coordinates = [x, y]
        self.id = 4
        self.colour = (139, 0, 255)

    def can_be_eaten(self, by_obj):
        return -10

# 0 поворот налево на 45 +
# 1 поворот направо на 45 +
# 2 посмотреть (1 - пусто; 2 - еда; 3 - моб; 4 - стена; 5 - яд)+
# 3 преобразовать яд в еду +
# 4 съесть
# 5 - 12 переход по направлению
# 13-63 переход на такое кол-во клеток по таблице
