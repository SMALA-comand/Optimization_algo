# -*- coding: utf-8 -*-

import csv
import math
import time
import random
from copy import deepcopy
from bisect import bisect_left

__all__ = ['ants_colony', 'simulated_annealing']


def _input_graph():
    """Реализует ввод/создание матрицы весов графа"""
    csv_true = None
    while csv_true is None:
        try:
            csv_t = int(input('Если хотите использовать csv-файл, введите число 1, если не хотите, то 0: '))
        except ValueError:
            print('Попробуйте снова!')
            continue
        if csv_t in (1, 0):
            csv_true = csv_t
        else:
            continue

    if csv_true == 1:
        print("Разделитель в csv - точка с запятой (;), без заголовков")
        path = input('Путь: ')
        matr = []
        try:
            with open(path, 'r', encoding='UTF-8') as f:
                data = csv.reader(f, delimiter=';')
                for row in data:
                    string = row[0]
                    numbers = string.split()
                    for i in range(len(numbers)):
                        if numbers[i] == "*":
                            continue
                        else:
                            numbers[i] = float(numbers[i])
                    matr.append(numbers)
        except IOError:
            print("An IOError")
            return None
        except FileNotFoundError:
            print("An FileNotFoundError")
            return None
        return matr

    n = None
    while n is None:
        try:
            nu = int(input("Количество городов: "))
        except ValueError:
            print('Попробуйте снова!')
            continue
        else:
            n = nu

    print(f"Каким способом вы хотите ввести матрицу весов для {n} городов?")
    print("Введите 1, если хотите ввести вручную. "
          "Введите 2, если хотите использовать рандом")

    mode = None
    while mode is None:
        try:
            m = int(input("Введите режим: "))
        except ValueError:
            print("Попробуйте снова!")
            continue
        if m not in (1, 2):
            continue
        else:
            mode = m

    matrix = [[0]*n for i in range(n)]    # невозможность попасть в точку отмечаем символом *
    if mode == 1:
        for i in range(0, n):
            for j in range(0, n):
                if i == j:
                    matrix[i][j] = "*"
                    continue

                numb = None
                while numb is None:
                    number = input(f"Введите стоимость маршрута ({i+1}->{j+1}). "
                                   f"Если маршрута нет, введите символ '*': ")
                    if number == "*":
                        matrix[i][j] = "*"
                        break
                    else:
                        try:
                            float(number)
                        except ValueError:
                            print('Введите снова!')
                            continue
                        else:
                            matrix[i][j] = float(number)
                            break

    elif mode == 2:
        print('С вероятностью 10% пути из города N в город M не будет существовать')
        print('Укажите границы рандомизатора: ')
        low, high, int_or_float = None, None, None

        while low is None:
            try:
                l = float(input("Нижняя граница: "))
            except ValueError:
                print('Введите снова!')
                continue
            else:
                low = l

        while high is None:
            try:
                h = float(input("Верхняя граница: "))
            except ValueError:
                print('Введите снова!')
                continue
            else:
                high = h

        while int_or_float is None:
            i_or_f = input("Введите int или float: ")
            if i_or_f.lower() in ('int', 'float'):
                int_or_float = i_or_f

        for i in range(n):
            for j in range(n):
                if i == j:
                    matrix[i][j] = "*"
                    continue
                x = random.random()
                if x <= 0.10:
                    matrix[i][j] = "*"
                else:
                    if int_or_float == 'float':
                        matrix[i][j] = round(random.uniform(low, high), 2)
                    else:
                        matrix[i][j] = random.randint(int(low), int(high))
    return matrix


def _get_column(matrix, k):
    """Взятие столбца по его номеру (нумерация с 0) из двумерного массива"""
    column = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if j == k:
                column.append(matrix[i][j])
    return column


def _next_city(matrix, city, black_list, fero_matrix, alpha, beta):
    """Выбор следующего города, в который отправится муравей"""
    plan = []
    indexes = []
    for i, el in enumerate(matrix[city]):
        if i in black_list or el == "*":
            continue
        indexes.append(i)
        t = (fero_matrix[city][i] ** alpha) * ((1 / el) ** beta)
        plan.append(t)
    if len(indexes) == 0:
        return "Stop"

    probability = [i / sum(plan) for i in plan]
    for i in range(1, len(probability)):
        probability[i] += probability[i - 1]

    random_point = random.random()
    our_city = indexes[bisect_left(probability, random_point)]
    return our_city


def _update_fero(fero_matrix, L_k, L_min, ant_way, p):
    """Обновление феромонов"""
    const = L_min / L_k
    tuples = [(ant_way[i], ant_way[i + 1]) for i in range(0, len(ant_way) - 1)]
    last_way = (ant_way[-1], ant_way[0])
    tuples.append(last_way)

    for i in tuples:
        fero_matrix[i[0]][i[1]] *= (1 - p)
        fero_matrix[i[0]][i[1]] += const
        fero_matrix[i[0]][i[1]] = round(fero_matrix[i[0]][i[1]], 4)

    return fero_matrix


def ants_colony(matrix=None, p=0.1, alpha=1.0, beta=1.0):
    """
    Solving the traveling salesman problem by an Ant algorithm.

    For the weight matrix of a graph representing a network of cities, finds the Hamiltonian cycle with the lowest cost.

    Parameters
    ----------
    matrix : 2d array NxN, optional
        Coefficient matrix, default is None object.
    p : float, between 0 and 1, optional
        Drying speed, default is 0.1.
    alpha : float, optional
        Shift of attention to the intensity of the trace, default is 1.0.
    beta : float, optional
        Shift of attention to the length of the way, default is 1.0.
    Returns
    -------
    global_min_way : [int] array like [1, 4, 2, ..., 1]
        The most optimal way.
    global_min_way : float
        The cost of the most optimal way.
    count_iter : int
        Number of iterations of the algorithm.
    matrix : 2d array NxN
        Initial weight matrix.

    """
    while matrix is None:
        matrix = _input_graph()
    length = len(matrix)

    clear_mat = deepcopy(matrix)
    fero_matrix = [[0.1] * length for i in range(length)]
    for i in range(length):
        for j in range(length):
            if matrix[i][j] == "*":
                fero_matrix[i][j] = 0
                clear_mat[i][j] = 10 ** 12

    Lmin = 0
    rows = []
    for i in range(length):
        el = min(clear_mat[i])
        Lmin += el
        rows.append(matrix[i].index(el))
    for i in range(length):
        if i not in rows:
            # берём i-ый столбец
            column = _get_column(clear_mat, i)
            el = min(column)
            Lmin += el

    count_iter = 1000
    global_min_way = []
    global_min_cost = 10 ** 13
    for iteration in range(count_iter):
        for ant in range(length):
            ant_way_cost = 0
            ant_way = [ant]
            black_list = [ant]

            while len(ant_way) < length:
                ant_way.append(_next_city(matrix, ant_way[-1], black_list, fero_matrix, alpha=alpha, beta=beta))
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

            fero_matrix = _update_fero(fero_matrix, ant_way_cost, Lmin, ant_way, p=p)

    return global_min_way, global_min_cost, count_iter, matrix


def _compute_way_cost(matrix, path):
    """Рассчёт стоимости пути"""
    total_cost = 0
    for i in range(0, len(path) - 1):
        first_city = path[i]
        second_city = path[i + 1]
        if matrix[first_city][second_city] == '*':
            return False
        total_cost += matrix[first_city][second_city]
    first_city = path[-1]
    second_city = path[0]
    if matrix[first_city][second_city] == "*":
        return False
    total_cost += matrix[first_city][second_city]
    return total_cost


def _get_new_way(path):
    """Swapping two elements in our path-array"""
    new_way = deepcopy(path)
    first = random.randint(0, len(path) - 1)
    second = random.randint(0, len(path) - 1)
    while second == first:
        second = random.randint(0, len(path) - 1)

    new_way[first], new_way[second] = new_way[second], new_way[first]
    return new_way


def simulated_annealing(matrix=None, t_0=1000.0, t_min=0.005):
    """
    The solution of the traveling salesman problem by the algorithm of simulated annealing.

    For the weight matrix of a graph representing a network of cities, finds the Hamiltonian cycle with the lowest cost.

    Parameters
    ----------
    matrix : 2d array NxN, optional
        Coefficient matrix, default is None object.
    t_0 : float, optional
        Starting temperature value, default is 1000.0.
    t_min : float, optional
        Final temperature value, default is 0.005.

    Returns
    -------
    global_min_way : [int] array like [1, 4, 2, ..., 1]
        The most optimal way.
    global_min_way : float
        The cost of the most optimal way.
    k : int
        Number of iterations of the algorithm.
    matrix : 2d array NxN
        Initial weight matrix.

    """
    while matrix is None:
        matrix = _input_graph()
    length = len(matrix)
    template = list(range(0, length))

    global_min_cost = False
    while not global_min_cost:
        random.shuffle(template)
        global_min_cost = _compute_way_cost(matrix, template)
        global_min_way = template

    t_k = t_0
    k = 1
    current_way = template
    current_way_cost = _compute_way_cost(matrix, template)

    while t_k > t_min:
        # t_k = t_0 / math.log(1+k)
        t_k = t_0 / (1 + k)
        k += 1

        cost = False
        while not cost:
            new_way = _get_new_way(current_way)
            cost = _compute_way_cost(matrix, new_way)

        dcost = cost - current_way_cost
        if dcost <= 0:
            current_way_cost = cost
            current_way = new_way
        else:
            change_prob = math.exp(-dcost / t_k)
            random_point = random.random()
            if random_point > change_prob:
                continue
            else:
                current_way_cost = cost
                current_way = new_way

        if current_way_cost < global_min_cost and current_way_cost != False:
            global_min_cost = current_way_cost
            global_min_way = current_way
            
    return global_min_way, global_min_cost, k, matrix

