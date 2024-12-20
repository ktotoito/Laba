class Matrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.vector_not_zero = []  # Ненулевые значение
        self.vector_not_zero_cols = []  # Номера соответствующих столбцов
        self.vector_elemets_in_row = [0] # Количество ненулевых элементов в первых i строках + 0
        # (чтобы не возникала ошибка при обращении по индексу к пустому списку)

    def add_el(self, val, col):  # Добавляет новый элемент
        if val != 0:
            self.vector_not_zero.append(val)
            self.vector_not_zero_cols.append(col)

    def add(self, k):  # Добавляет количество ненулевых элементов в новой строке
        self.vector_elemets_in_row.append(k + self.vector_elemets_in_row[-1])

    def get(self, x, y):
        # Получаем диапазон элементов, в котором будем искать
        x1 = self.vector_elemets_in_row[x - 1]
        x2 = self.vector_elemets_in_row[x]
        y = y - 1
        for i in range(x1, min(x2, len(self.vector_not_zero_cols))):
            # Проходим по диапазону, ищем нужный столбец
            if self.vector_not_zero_cols[i] == y:
                return self.vector_not_zero[i]
        return 0

    def trace(self):
        ans = 0
        if self.n != self.m:
            raise ValueError("След может быть вычислен только для квадратной матрицы.")
        else:
            for i in range(self.n + 1):
                ans += self.get(i, i)
            return ans

    def __add__(self, other):
        if (self.n != other.n) or (self.m != other.m):
            raise ValueError('Несоответствие размеров матриц')
        matrix_sum = Matrix(self.n, self.m)
        for y in range(self.n):
            # Будем добавлять элементы построчно в порядке возрастания номера столбца
            k_el_in_row = 0  # Счетчик кол-ва добавленных элементов в данную строку

            # p1 - указывает на первый недобавленный элемент из первой матрицы,
            # с наименьшим номером столбца из данной строчки,
            # аналогично p2
            p1, p2 = self.vector_elemets_in_row[y], other.vector_elemets_in_row[y]
            while (p1 < (self.vector_elemets_in_row[y + 1])) or (p2 < (other.vector_elemets_in_row[y + 1])):
                # Пока добавлены не все ненулевые элементы
                if p1 == (self.vector_elemets_in_row[y + 1]):
                    # Если в 1-й матрице не осталось ненулевых элементов из данной строки
                    matrix_sum.add_el(other.vector_not_zero[p2], other.vector_not_zero_cols[p2])
                    p2 += 1
                elif p2 == (other.vector_elemets_in_row[y + 1]):
                    # Если во 2-й матрице не осталось ненулевых элементов из данной строки
                    matrix_sum.add_el(self.vector_not_zero[p1], self.vector_not_zero_cols[p1])
                    p1 += 1
                elif self.vector_not_zero_cols[p1] < other.vector_not_zero_cols[p2]:
                    # Если номер столбца первого недобавленного из 1-й матрицы < первого недобавленного из второй
                    matrix_sum.add_el(self.vector_not_zero[p1], self.vector_not_zero_cols[p1])
                    p1 += 1
                elif self.vector_not_zero_cols[p1] > other.vector_not_zero_cols[p2]:
                    # Если номер столбца первого недобавленного из 2-й матрицы < первого недобавленного из первой
                    matrix_sum.add_el(other.vector_not_zero[p2], other.vector_not_zero_cols[p2])
                    p2 += 1
                else:
                    # Если номера колонок совпадают, то следует записать сумму первых элементов
                    matrix_sum.add_el(self.vector_not_zero[p1] + other.vector_not_zero[p2],
                                      self.vector_not_zero_cols[p1])
                    p1 += 1
                    p2 += 1
                k_el_in_row += 1
            matrix_sum.add(k_el_in_row)  # Добавляем количество ненулевых элементов в строках до (y+1) + 1
        return matrix_sum

    def __mul__(self, other):
        mul_matrix = Matrix(self.n, self.m)
        # Копируем списки с номерами столбцов и количеством элементов в строках, поскольку они не изменяются
        mul_matrix.vector_not_zero_cols = self.vector_not_zero_cols.copy()
        mul_matrix.vector_elemets_in_row = self.vector_elemets_in_row.copy()
        mul_matrix.vector_not_zero = list(map(lambda x: x * other, self.vector_not_zero))
        return mul_matrix

    def __rmul__(self, other): # Для коммутативности
        mul_matrix = Matrix(self.n, self.m)
        mul_matrix.vector_not_zero_cols = self.vector_not_zero_cols.copy()
        mul_matrix.vector_elemets_in_row = self.vector_elemets_in_row.copy()
        mul_matrix.vector_not_zero = list(map(lambda x: x * other, self.vector_not_zero))
        return mul_matrix

    def __matmul__(self, other):
        if self.m != other.n or self.n != other.m:
            raise ValueError('Несоответствие размеров матриц')

        mul_matrix = Matrix(self.n, other.m)
        for y in range(self.n):
            # Будем построчно вычислять итоговую матрицу
            k_el_in_row = 0 # Счетчик ненулевых значений итоговой матрицы y+1 строчке
            for x in range(other.m):
                new_val = 0  # Элемент итоговой матрицы из y+1 строчки x+1 колонки
                for p1 in range(self.vector_elemets_in_row[y], self.vector_elemets_in_row[y + 1]):
                    # p1 пробегает по всем ненулевым элементам 1 матрицы из y+1 строчки
                    new_val += self.vector_not_zero[p1] * other.get(self.vector_not_zero_cols[p1] + 1, x + 1)
                mul_matrix.add_el(new_val, x)
                k_el_in_row += bool(new_val)
            mul_matrix.add(k_el_in_row) # Добавляем количество ненулевых элементов в строках до (y+1) + 1
        return mul_matrix

    def determinant_and_is_reversed(self):
        det = self.determinant()
        if det:
            return det, 'да'
        else:
            return det, 'нет'

    def determinant(self):
        # Проверяем, что это квадратная матрица
        if self.n != self.m:
            raise ValueError("Определитель может быть вычислен только для квадратной матрицы.")

        # Базовый случай: определитель 1x1
        if self.n == 1:
            return self.get(1, 1)

        # Базовый случай: определитель 2x2
        if self.n == 2:
            return self.get(1, 1) * self.get(2, 2) - self.get(1, 2) * self.get(2, 1)

        det = 0
        for col in range(1, self.n + 1):
            # Вычисляем минор для текущего столбца
            minor = self._get_minor(1, col)
            det += ((-1) ** (1 + col)) * self.get(1, col) * minor.determinant()

        return det

    def _get_minor(self, row, col):
        # Создаём новую матрицу (N-1)x(M-1) как объект Matrix
        minor_n = self.n - 1
        minor_m = self.m - 1
        minor = Matrix(minor_n, minor_m)

        for i in range(2, self.n + 1): # Начинаем с 2-х, чтобы исключить 1-ю строку
            k = 0 # Счётчик количества элементов в строке
            for j in range(1, self.m + 1):
                if j != col: # Проверяем, что не проходимся по столбцу, содержащему элемент
                    elem = self.get(i, j)
                    # Меняем номера столбцов для новой матрицы
                    if j > col:
                        minor.add_el(elem, j-2)
                    else:
                        minor.add_el(elem, j-1)
                    if elem != 0:
                        k += 1 # Прибавляем ненулевой элемент
            minor.add(k) # Добавляем строку
        return minor

# print('Введите размеры матрицы N и M через пробелы:\n')
# n, m = map(int, input().split())
# print('Введите элементы матрицы через пробел:\n')
# matrix = Matrix(n,m)
# for i in range(n): # Проходимся по строкам
#     k = 0 # Счётчик количества элементов в строке
#     row = list(map(int, input().split()))
#     for j in range(m): # Проходимся по столбцам
#         elem = row[j]
#         if elem != 0:
#             k += 1 # Прибавляем ненулевой элемент
#         matrix.add_el(elem, j) # Добавляем элемент
#     matrix.add(k) # Добавляем строку

