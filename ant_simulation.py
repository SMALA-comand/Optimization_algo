from input_graph import input_graph
import random
from bisect import bisect_left
from copy import deepcopy
import time


def get_column(matrix, k):
    column = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j == k:
                column.append(matrix[i][j])
    return column


def next_city(matrix, city, black_list, fero_matrix):
    alpha = 1
    beta = 1

    plan = []
    indexes = []
    for i, el in enumerate(matrix[city]):
        if i in black_list or el == "*":
            continue
        indexes.append(i)
        t = (fero_matrix[city][i]**alpha) * ((1/el)**beta)
        plan.append(t)
    if len(indexes) == 0:
        return False

    probability = [i/sum(plan) for i in plan]
    for i in range(1, len(probability)):
        probability[i] += probability[i-1]

    random_point = random.random()
    our_city = indexes[bisect_left(probability, random_point)]
    return our_city


def update_fero(fero_matrix, L_k, L_min, ant_way):
    # определим константу испарения p
    p = 0.1
    const = L_min/L_k
    tuples = [(ant_way[i], ant_way[i+1]) for i in range(0, len(ant_way)-1)]
    last_way = (ant_way[-1], ant_way[0])
    tuples.append(last_way)

    for i in tuples:
        fero_matrix[i[0]][i[1]] *= (1 - p)
        fero_matrix[i[0]][i[1]] += const

    return fero_matrix


def ants_colony(matrix=None):
    if matrix is None:
        matrix = input_graph()
    length = len(matrix)        # количество городов (количество муравьёв)

    clear_mat = deepcopy(matrix)
    # заполним матрицу феромонов
    fero_matrix = [[0.1]*length for i in range(length)]
    for i in range(length):
        for j in range(length):
            if matrix[i][j] == "*":
                fero_matrix[i][j] = 0
                clear_mat[i][j] = 10**12

    # найдём минимальную стоимость маршрута жадным алгоритмом
    Lmin = 0
    rows = []
    for i in range(length):
        el = min(clear_mat[i])
        Lmin += el
        rows.append(matrix[i].index(el))
    for i in range(length):
        if i not in rows:
            # берём i-ый столбец
            column = get_column(clear_mat, i)
            el = min(column)
            Lmin += el

    count_iter = 1
    global_min_way = []
    global_min_cost = 10**13
    for iteration in range(count_iter):
        # на каждой итерации запускаем одного муравья из каждого города
        for ant in range(length):     # запускаем из каждого города одного муравья
            good_way = False
            while not good_way:
                ant_way_cost = 0
                ant_way = [ant]
                black_list = [ant]

                # функция для определения следующего города
                while len(ant_way) < length:
                    ant_way.append(next_city(matrix, ant_way[-1], black_list, fero_matrix))
                    if not ant_way[-1]:
                        print('Мы тут')
                        break
                    black_list.append(ant_way[-1])
                    ant_way_cost += matrix[ant_way[-2]][ant_way[-1]]
                else:
                    if matrix[ant_way[-1]][ant] != "*":
                        ant_way_cost += matrix[ant_way[-1]][ant]
                        good_way = True

            if ant_way_cost < global_min_cost:
                global_min_cost = ant_way_cost
                global_min_way = ant_way

            fero_matrix = update_fero(fero_matrix, ant_way_cost, Lmin, ant_way)

    return global_min_way, global_min_cost, count_iter, matrix


if __name__ == "__main__":
    matr = [['*', 40.0, 1.0, 16.0, 8.0],
            [7.0, '*', 1.0, 7.0, 20.0],
            [10.0, 10.0, '*', 5.0, 3.0],
            [7.0, 9.0, 7.0, '*', 2.0],
            [1.0, 9.0, 2.0, 18.0, '*']]

    start_time = time.time()
    a, b, c, m = ants_colony(matr)
    seconds = time.time() - start_time
    a = '-'.join([str(i+1) for i in a])+f'-{str(a[0]+1)}'
    print("Алгоритм: Муравьиный алгоритм")
    print(f"Количество итераций: {c}")
    print(f"Время выполнения: {seconds} секунд")
    print(f"Маршрут обхода: {a}")
    print(f"Стоимость: {round(b, 1)}")

