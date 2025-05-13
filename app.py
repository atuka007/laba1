import copy
def read_matrix_from_file(filename, N): # Чтение квадратной матрицы из файла
    with open(filename, 'r') as file:
        numbers = []
        for line in file:
            numbers.extend(map(int, line.split()))
    matrix = []
    index = 0
    for i in range(N):
        row = numbers[index: index + N]
        matrix.append(row)
        index += N
    return matrix

def print_matrix(matrix, name): # Печать матрицы с названием
    print(f"Матрица {name}:") # f - форматированная строка, которая позволяет встраивать выражения прямо в строку с помощью фигурных скобок {}
    for row in matrix:
        print(' '.join(f"{elem:4}" for elem in row))

def is_in_area1(i, j, N): # Область 1: ниже главной диагонали и выше побочной
    return i > j and i + j < N - 1

def is_in_area2(i, j, N): # Область 2: выше главной и побочной диагоналей
    return i < j and i + j < N - 1

def is_in_area3(i, j, N): # Область 3: выше главной диагонали, но ниже побочной
    return i < j and i + j > N - 1

def is_in_area4(i, j, N): # Область 4: ниже главной и побочной диагоналей
    return i > j and i + j > N - 1

def count_pos_in_even_cols_area2(matrix, N): # Подсчет положительных элементов в четных столбцах области 2
    count = 0
    for i in range(N):
        for j in range(N):
            if is_in_area2(i, j, N) and j % 2 == 1 and matrix[i][j] > 0:
                count += 1
    return count

def count_neg_in_odd_cols_area4(matrix, N): # Подсчет отрицательных элементов в нечетных столбцах области 4
    count = 0
    for i in range(N):
        for j in range(N):
            if is_in_area4(i, j, N) and j % 2 == 0 and matrix[i][j] < 0:
                count += 1
    return count

def swap_areas_1_and_2_symmetrically(matrix, N): # Обмен областей 1 и 2 симметрично
    for i in range(N):
        for j in range(N):
            if is_in_area1(i, j, N):
                mirror_i = j
                mirror_j = i
                if is_in_area2(mirror_i, mirror_j, N):
                    matrix[i][j], matrix[mirror_i][mirror_j] = matrix[mirror_i][mirror_j], matrix[i][j]


def swap_areas_3_and_4_non_symmetrically(matrix, N): # Обмен областей 3 и 4 несимметрично
    area3 = []
    area4 = []
    for i in range(N): # Собираем элементы областей
        for j in range(N):
            if is_in_area3(i, j, N):
                area3.append(matrix[i][j])
            elif is_in_area4(i, j, N):
                area4.append(matrix[i][j])
    area3, area4 = area4, area3 # Меняем местами
    idx3 = 0 # Записываем обратно
    idx4 = 0
    for i in range(N):
        for j in range(N):
            if is_in_area3(i, j, N):
                matrix[i][j] = area3[idx3]
                idx3 += 1
            elif is_in_area4(i, j, N):
                matrix[i][j] = area4[idx4]
                idx4 += 1

def matrix_add(A, B, N): # Сложение матриц
    return [[A[i][j] + B[i][j] for j in range(N)] for i in range(N)]

def matrix_transpose(A, N): # Транспонирование матрицы
    return [[A[j][i] for j in range(N)] for i in range(N)]

def matrix_multiply(A, B, N): # Умножение матриц
    return [[sum(A[i][k] * B[k][j] for k in range(N)) for j in range(N)] for i in range(N)]

def matrix_multiply_scalar(matrix, scalar, N): # Умножение матрицы на скаляр
    return [[matrix[i][j] * scalar for j in range(N)] for i in range(N)]

def matrix_subtract(A, B, N): # Вычитание матриц
    return [[A[i][j] - B[i][j] for j in range(N)] for i in range(N)]

try: # Основная программа
    K = int(input("Введите число K: "))
    N = int(input("Введите размер матрицы N: "))
    A = read_matrix_from_file("test.txt", N)  # Чтение матрицы A из файла
    print_matrix(A, "A")
    F = copy.deepcopy(A) # Создаем копию матрицы A
    pos_area2 = count_pos_in_even_cols_area2(F, N) # Подсчет элементов по условиям
    neg_area4 = count_neg_in_odd_cols_area4(F, N)
    print(f"Положительных в чётных столбцах области 2: {pos_area2}")
    print(f"Отрицательных в нечётных столбцах области 4: {neg_area4}")

    if pos_area2 > neg_area4:  # Выполняем преобразования F
        print("Меняем области 1 и 2 симметрично")
        swap_areas_1_and_2_symmetrically(F, N)
    else:
        print("Меняем области 3 и 4 несимметрично")
        swap_areas_3_and_4_non_symmetrically(F, N)
    print_matrix(F, "F после преобразований")

    F_plus_A = matrix_add(F, A, N) # Вычисляем (F + A)
    print_matrix(F_plus_A, "F + A")

    AT = matrix_transpose(A, N) # Вычисляем AT (транспонированная A)
    print_matrix(AT, "A^T")

    temp = matrix_multiply(F_plus_A, AT, N) # Вычисляем (F + A) * AT
    print_matrix(temp, "(F + A) * A^T")

    KF = matrix_multiply_scalar(F, K, N) # Вычисляем K * F
    print_matrix(KF, "K * F")

    result = matrix_subtract(temp, KF, N) # Итоговый результат: (F + A)*AT - K * F
    print_matrix(result, "Результат (F + A)*A^T - K*F")

except FileNotFoundError:
    print("Файл 'test.txt' не найден!")
except ValueError as e:
    print("Ошибка: " + {e})