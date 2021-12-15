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
        return "Stop"

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
        fero_matrix[i[0]][i[1]] = round(fero_matrix[i[0]][i[1]], 4)

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

    count_iter = 1000
    global_min_way = []
    global_min_cost = 10**13
    for iteration in range(count_iter):
        # на каждой итерации запускаем одного муравья из каждого города
        for ant in range(length):     # запускаем из каждого города одного муравья
            ant_way_cost = 0
            ant_way = [ant]
            black_list = [ant]

            # функция для определения следующего города
            while len(ant_way) < length:
                ant_way.append(next_city(matrix, ant_way[-1], black_list, fero_matrix))
                if ant_way[-1] == "Stop":
                    ant_way_cost = 0
                    ant_way = [ant]
                    black_list = [ant]
                else:
                    black_list.append(ant_way[-1])
                    ant_way_cost += matrix[ant_way[-2]][ant_way[-1]]

                if len(ant_way) == length:
                    if matrix[ant_way[-1]][ant] == "*":
                        ant_way_cost = 0
                        ant_way = [ant]
                        black_list = [ant]
                    else:
                        ant_way_cost += matrix[ant_way[-1]][ant]

            if ant_way_cost < global_min_cost:
                global_min_cost = ant_way_cost
                global_min_way = ant_way

            fero_matrix = update_fero(fero_matrix, ant_way_cost, Lmin, ant_way)

    return global_min_way, global_min_cost, count_iter, matrix


if __name__ == "__main__":
    # matr = [['*', 40.0, 1.0, 16.0, 8.0],
    #         [7.0, '*', 1.0, 7.0, 20.0],
    #         [10.0, 10.0, '*', 5.0, 3.0],
    #         [7.0, 9.0, 7.0, '*', 2.0],
    #         [1.0, 9.0, 2.0, 18.0, '*']]

    matr = [
['*', 13, 29, 60, 12, 6, 38, 6, 27, 29, 44, 59, 49, 45, 6, 13, 9, 43, 38, 27, 15, 21, 15, 59, 10, 30, 16, 64, 47, 41],
[42, '*', 51, 45, 45, 21, 55, 38, 27, 33, 58, 34, 57, 9, 55, 63, 34, 60, 65, 33, 28, 15, 16, 34, 62, 49, 58, 40, 12, 56],
[20, 17, '*', 54, 44, 64, 38, 31, 26, 40, 11, 7, 10, 47, 11, 34, 57, 34, 29, 15, 9, 11, 51, 7, 63, 63, 34, 30, 45, 39],
[31, 65, 39, '*', 19, 49, 22, 18, 56, 52, 62, 23, 38, 10, 12, 6, 55, 37, 27, 60, 46, 43, 27, 7, 61, 52, 28, 9, 51, 6],
[10, 47, 60, 29, '*', 43, 15, 44, 27, 55, 38, 66, 44, 10, 55, 64, 47, 9, 18, 56, 23, 17, 39, 10, 55, 36, 50, 25, 40, 51],
[8, 41, 49, 61, 13, '*', 44, 33, 22, 51, 9, 55, 63, 52, 38, 30, 11, 34, 27, 10, 46, 37, 64, 62, 36, 66, 21, 36, 65, 40],
[55, 47, 9, 31, 11, 30, '*', 50, 14, 12, 28, 49, 62, 50, 58, 26, 45, 39, 39, 34, 62, 34, 63, 21, 11, 6, 12, 60, 23, 19],
[66, 40, 14, 52, 49, 55, 9, '*', 41, 19, 53, 65, 40, 42, 64, 39, 52, 16, 33, 7, 63, 48, 43, 10, 42, 66, 61, 23, 10, 62],
[33, 41, 22, 6, 58, 57, 6, 13, '*', 8, 50, 22, 25, 18, 9, 18, 15, 56, 7, 52, 8, 66, 8, 22, 51, 35, 14, 50, 66, 30],
[32, 40, 8, 49, 28, 23, 57, 11, 31, '*', 36, 28, 45, 20, 39, 13, 66, 44, 24, 42, 57, 32, 16, 57, 64, 39, 19, 13, 57, 53],
[42, 62, 43, 49, 7, 25, 52, 32, 23, 29, '*', 41, 17, 15, 47, 44, 54, 47, 19, 37, 21, 38, 46, 29, 29, 26, 25, 66, 30, 43],
[20, 33, 49, 20, 64, 7, 33, 48, 8, 38, 49, '*', 7, 18, 15, 54, 65, 44, 42, 52, 28, 41, 47, 38, 50, 45, 43, 45, 62, 61],
[54, 54, 47, 65, 64, 65, 7, 27, 14, 51, 22, 37, '*', 18, 56, 50, 59, 39, 16, 12, 17, 26, 14, 38, 61, 60, 8, 20, 41, 49],
[60, 53, 42, 20, 49, 64, 55, 21, 56, 7, 20, 45, 62, '*', 13, 14, 53, 34, 30, 22, 30, 20, 17, 32, 21, 16, 63, 34, 21, 17],
[17, 45, 64, 31, 43, 25, 29, 57, 44, 52, 40, 24, 49, 55, '*', 16, 65, 7, 39, 33, 45, 32, 62, 16, 12, 56, 52, 61, 53, 64],
[38, 49, 61, 64, 26, 7, 48, 56, 18, 10, 8, 36, 62, 56, 43, '*', 47, 43, 36, 66, 53, 26, 37, 22, 40, 57, 52, 16, 65, 8],
[63, 8, 60, 26, 63, 34, 60, 17, 29, 17, 20, 36, 42, 7, 66, 7, '*', 44, 64, 13, 50, 43, 39, 39, 59, 58, 54, 45, 45, 54],
[39, 11, 46, 63, 38, 26, 45, 51, 24, 52, 26, 36, 6, 60, 7, 50, 52, '*', 64, 40, 60, 29, 28, 15, 46, 9, 31, 10, 21, 48],
[59, 38, 37, 61, 47, 54, 9, 54, 16, 39, 20, 50, 58, 36, 54, 18, 61, 36, '*', 61, 42, 45, 52, 41, 12, 32, 49, 19, 44, 8],
[28, 34, 30, 66, 44, 6, 35, 22, 21, 9, 52, 44, 66, 22, 6, 45, 24, 48, 45, '*', 11, 56, 18, 48, 49, 35, 13, 16, 39, 42],
[8, 55, 15, 62, 26, 32, 13, 34, 35, 44, 66, 57, 7, 41, 30, 56, 66, 53, 55, 61, '*', 18, 66, 45, 48, 58, 53, 26, 62, 47],
[15, 36, 43, 52, 32, 33, 43, 50, 58, 48, 25, 34, 64, 54, 13, 41, 23, 12, 35, 12, 40, '*', 8, 7, 66, 63, 65, 42, 50, 51],
[14, 48, 40, 8, 52, 31, 6, 18, 21, 18, 66, 25, 39, 29, 66, 29, 43, 11, 48, 38, 43, 37, '*', 57, 41, 31, 22, 44, 55, 23],
[11, 64, 33, 62, 27, 37, 43, 8, 55, 48, 41, 38, 31, 17, 62, 53, 64, 44, 65, 9, 30, 42, 54, '*', 41, 47, 8, 42, 37, 18],
[45, 31, 64, 32, 32, 10, 44, 50, 60, 20, 31, 54, 45, 16, 17, 20, 24, 41, 24, 39, 30, 33, 7, 58, '*', 52, 32, 64, 24, 37],
[14, 16, 54, 17, 12, 19, 66, 25, 29, 41, 8, 30, 25, 46, 47, 55, 15, 56, 56, 9, 54, 7, 16, 8, 44, '*', 23, 41, 17, 44],
[37, 6, 17, 36, 17, 47, 33, 18, 10, 50, 40, 6, 12, 42, 32, 6, 27, 18, 19, 28, 65, 66, 52, 28, 48, 48, '*', 22, 30, 46],
[56, 22, 17, 40, 13, 22, 13, 28, 28, 13, 57, 41, 49, 24, 56, 66, 60, 31, 11, 17, 8, 24, 65, 26, 23, 38, 30, '*', 55, 7],
[26, 57, 21, 64, 17, 34, 45, 60, 27, 42, 23, 32, 51, 35, 30, 12, 49, 49, 11, 35, 22, 46, 63, 45, 36, 42, 30, 8, '*', 9],
[23, 56, 62, 29, 62, 16, 48, 30, 6, 16, 55, 24, 30, 66, 12, 35, 11, 61, 37, 10, 20, 33, 56, 54, 65, 59, 21, 59, 28, '*']]

    start_time = time.time()
    a, b, c, m = ants_colony(matr)
    seconds = time.time() - start_time
    a = '-'.join([str(i+1) for i in a])+f'-{str(a[0]+1)}'
    print("Алгоритм: Муравьиный алгоритм")
    print(f"Количество итераций: {c}")
    print(f"Время выполнения: {seconds} секунд")
    print(f"Маршрут обхода: {a}")
    print(f"Стоимость: {round(b, 1)}")

