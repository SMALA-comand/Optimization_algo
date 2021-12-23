import csv
import random


def input_graph():
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
        path = input('Путь: ')
        matr = []
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


if __name__ == "__main__":
    a = input_graph()
    print(a)
