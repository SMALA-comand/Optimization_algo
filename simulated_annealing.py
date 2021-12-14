from input_graph import input_graph
import random
import math
from copy import deepcopy
import time


def compute_way_cost(matrix, path):
    total_cost = 0
    for i in range(0, len(path)-1):
        first_city = path[i]
        second_city = path[i+1]
        if matrix[first_city][second_city] == '*':
            return False
        total_cost += matrix[first_city][second_city]
    first_city = path[-1]
    second_city = path[0]
    if matrix[first_city][second_city] == "*":
        return False
    total_cost += matrix[first_city][second_city]
    return total_cost


def get_new_way(path):
    new_way = deepcopy(path)
    first = random.randint(0, len(path)-1)
    second = random.randint(0, len(path)-1)
    while second == first:
        second = random.randint(0, len(path)-1)

    new_way[first], new_way[second] = new_way[second], new_way[first]
    return new_way


def simulated_annealing(matrix=None):
    if matrix is None:
        matrix = input_graph()
    length = len(matrix)
    template = list(range(0, length))
    t_0 = 1000
    t_min = 0.005

    random.shuffle(template)
    global_min_cost = compute_way_cost(matrix, template)
    global_min_way = template

    t_k = t_0
    k = 1
    current_way = template
    current_way_cost = compute_way_cost(matrix, template)

    while t_k > t_min:
        # изменяем температуру
        # t_k = t_0 / math.log(1+k)
        t_k = t_0 / (1+k)
        k += 1

        cost = False
        while not cost:
            new_way = get_new_way(current_way)
            cost = compute_way_cost(matrix, new_way)

        dcost = cost - current_way_cost
        if dcost <= 0:
            current_way_cost = cost
            current_way = new_way
        else:
            change_prob = math.exp(-dcost/t_k)
            random_point = random.random()
            if random_point > change_prob:
                continue
            else:
                current_way_cost = cost
                current_way = new_way

        if current_way_cost < global_min_cost:
            global_min_cost = current_way_cost
            global_min_way = current_way

    return global_min_way, global_min_cost, k, matrix


if __name__ == "__main__":
    matr = [['*', 4.0, 1.0, 16.0, 8.0],
            [7.0, '*', 1.0, 7.0, 20.0],
            [10.0, 10.0, '*', 5.0, 3.0],
            [7.0, 9.0, 7.0, '*', 2.0],
            [1.0, 9.0, 2.0, 18.0, '*']]

    start_time = time.time()
    a, b, c, m = simulated_annealing(matrix=matr)
    seconds = time.time() - start_time
    a = '-'.join([str(i+1) for i in a])
    print("Алгоритм: Имитация отжига")
    print(f"Количество итераций: {c}")
    print(f"Время выполнения: {seconds} секунд")
    print(f"Маршрут обхода: {a}")
    print(f"Стоимость: {round(b, 1)}")
