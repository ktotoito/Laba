class Matrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.vector_not_zero = []  # ненулевые значение
        self.vector_not_zero_cols = []  # номера соотвествущих столбцов
        self.vector_elemets_in_row = [0] # кол-во ненулевых эл-тов в первых i строках + 0
        # (чтобы не возникала ошибка при обращении по индексу к пустому списку)

    def add_el(self, val, col):
        if val != 0:
            self.vector_not_zero.append(val)
            self.vector_not_zero_cols.append(col)

    def add(self, k):
        self.vector_elemets_in_row.append(k + self.vector_elemets_in_row[-1])

    def get(self, x, y):
        x1 = self.vector_elemets_in_row[x - 1]
        x2 = self.vector_elemets_in_row[x]
        y = y - 1
        for i in range(x1, min(x2, len(self.vector_not_zero_cols))):
            if self.vector_not_zero_cols[i] == y:
                return self.vector_not_zero[i]
        return 0

    def trace(self):
        ans = 0
        if self.n == self.m:
            for i in range(self.n + 1):
                ans = ans + self.get(i, i)
            return ans
        else:
            raise ValueError("След может быть вычислен только для квадратной матрицы.")

    def __add__(self, other):
        if (self.n != other.n) or (self.m != other.m):
            raise ValueError('Несоответствие размеров матриц')
        matrix_sum = Matrix(self.n, self.m)
        for y in range(self.n):
            # будем добавлять элементы построчно в порядке возрастания номера столбца
            k_el_in_row = 0  # счетчик кол-ва добавленных элементов в данную строку

            # p1 - указывает на первый недобавленный элемент из первой матрицы
            # (с наименьшим номером столбца из данной строчки)
            # аналогично p2
            p1, p2 = self.vector_elemets_in_row[y], other.vector_elemets_in_row[y]
            while (p1 < (self.vector_elemets_in_row[y + 1])) or (p2 < (other.vector_elemets_in_row[y + 1])):
                # пока добавлены не все ненулевые эл-ты
                if p1 == (self.vector_elemets_in_row[y + 1]):
                    # если в 1 матрице не осталось ненулевых элементов из данной строки
                    matrix_sum.add_el(other.vector_not_zero[p2], other.vector_not_zero_cols[p2])
                    p2 += 1
                elif p2 == (other.vector_elemets_in_row[y + 1]):
                    # если во 2 матрице не осталось ненулевых элементов из данной строки
                    matrix_sum.add_el(self.vector_not_zero[p1], self.vector_not_zero_cols[p1])
                    p1 += 1
                elif self.vector_not_zero_cols[p1] < other.vector_not_zero_cols[p2]:
                    # если номер столбца первого недобавленного из 1 матрицы < первого недобавленного из второй
                    matrix_sum.add_el(self.vector_not_zero[p1], self.vector_not_zero_cols[p1])
                    p1 += 1
                elif self.vector_not_zero_cols[p1] > other.vector_not_zero_cols[p2]:
                    # если номер столбца первого недобавленного из 2 матрицы < первого недобавленного из первой
                    matrix_sum.add_el(other.vector_not_zero[p2], other.vector_not_zero_cols[p2])
                    p2 += 1
                else:
                    # если номера колонок совпадают, то следует записать сумму первых эл-тов
                    matrix_sum.add_el(self.vector_not_zero[p1] + other.vector_not_zero[p2],
                                      self.vector_not_zero_cols[p1])
                    p1 += 1
                    p2 += 1
                k_el_in_row += 1
            matrix_sum.add(k_el_in_row)  # добавляем кол-во ненулевых эл-тов в строках до (y+1) + 1
        return matrix_sum

    def __str__(self):
        return '\n'.join(
            [' '.join(map(lambda y: str(self.get(x, y)), range(1, self.n + 1))) for x in range(1, self.m + 1)])

    def __mul__(self, other):
        mul_matrix = Matrix(self.n, self.m)
        mul_matrix.vector_not_zero_cols = self.vector_not_zero_cols.copy()
        mul_matrix.vector_elemets_in_row = self.vector_elemets_in_row.copy()
        mul_matrix.vector_not_zero = list(map(lambda x: x * other, self.vector_not_zero))
        return mul_matrix

    def __rmul__(self, other):
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
            # будем построчно вычислять итоговую матрицу
            k_el_in_row = 0 # счетчик ненулевых значений итоговой матрицы  y+1 строчке
            for x in range(other.m):
                new_val = 0  # элемент итоговой матрицы из y+1 строчки x+1 колонки
                for p1 in range(self.vector_elemets_in_row[y], self.vector_elemets_in_row[y + 1]):
                    # p1 пробегает по всем ненулевым эл-там 1 матрицы из y+1 строчки
                    new_val += self.vector_not_zero[p1] * other.get(self.vector_not_zero_cols[p1] + 1, x + 1)
                mul_matrix.add_el(new_val, x)
                k_el_in_row += bool(new_val)
            mul_matrix.add(k_el_in_row) # добавляем кол-во ненулевых эл-тов в строках до (y+1) + 1
        return mul_matrix

    def determinant_and_is_reversed(self):
        det = self.determinant()
        a = 'нет'
        if det:
            a = 'да'
        return det, a

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
        minor_n = self.n - 1
        minor_m = self.m - 1
        minor = Matrix(minor_n, minor_m)

        for i in range(1, self.n + 1):
            k = 0
            for j in range(1, self.m + 1):
                if i != row and j != col:
                    elem = self.get(i, j)
                    if j > col:
                        minor.add_el(elem, j-2)
                    else:
                        minor.add_el(elem, j-1)
                    if elem != 0:
                        k += 1
            if i != row:
                minor.add(k)
        return minor

# print('Введите размеры матрицы N и M через пробелы:\n')
# n, m = map(int, input().split())
# print('Введите элементы матрицы через пробел:\n')
# matrix = Matrix(n,m)
# for i in range(n): # проходимся по строкам
#     k = 0 # счётчик количества элементов в строке
#     row = list(map(int, input().split()))
#     for j in range(m): # проходимся по столбцам
#         elem = row[j]
#         if elem != 0:
#             k += 1 # Прибавляем ненулевой элемент
#         matrix.add_el(elem, j) # Добавляем элемент
#     matrix.add(k) # Добавляем строку
