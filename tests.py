import unittest
from main11 import Matrix


def setUpMatrix(n_in,m_in,sample_in):
    matrix_in = Matrix(n_in,m_in)
    for i in range(n_in):
        k = 0
        row = sample_in[i]
        for j in range(m_in):
            elem = row[j]
            if elem != 0:
                k += 1
            matrix_in.add_el(elem, j)
        matrix_in.add(k)
    return matrix_in


class Matrix_test(unittest.TestCase):

    def test1_can_store_right_way(self):
        n, m = 5, 5
        sample = [[0, 0, -74, 0, 1], [0, 62, 0, -5, 0], [8, -3, 0, 0, 0], [0, 0, 100, -9, 0], [0, -25, 0, 0, 45]]
        matrix = setUpMatrix(n, m, sample)

        self.assertEqual([-74, 1, 62, -5, 8, -3, 100, -9, -25, 45], matrix.vector_not_zero)
        self.assertEqual([2, 4, 1, 3, 0, 1, 2, 3, 1, 4], matrix.vector_not_zero_cols)
        self.assertEqual([0, 2, 4, 6, 8, 10], matrix.vector_elemets_in_row)

    def test2_can_display_elem(self):
        n, m = 5, 5
        sample = [[0, 0, -74, 0, 1], [0, 62, 0, -5, 0], [8, -3, 0, 0, 0], [0, 0, 100, -9, 0], [0, -25, 0, 0, 45]]
        matrix = setUpMatrix(n, m, sample)

        pos1 = matrix.get(5, 5)
        pos2 = matrix.get(3, 2)
        self.assertEqual(45, pos1)
        self.assertEqual(-3, pos2)

    def test3_can_find_the_trace(self):
        n, m = 5, 5
        sample = [[0, 0, -74, 0, 1], [0, 62, 0, -5, 0], [8, -3, 0, 0, 0], [0, 0, 100, -9, 0], [0, -25, 0, 0, 45]]
        matrix = setUpMatrix(n, m, sample)

        trace1 = matrix.trace()
        self.assertEqual(98, trace1)

    def test4_can_find_the_trace_error(self):
        n, m = 6, 5
        sample = [[0, 0, -74, 0, 1], [0, 62, 0, -5, 0], [8, -3, 0, 0, 0], [0, 0, 100, -9, 0], [0, -25, 0, 0, 45], [0, -25, 0, 0, 45]]
        matrix = setUpMatrix(n, m, sample)

        e1 = None
        try:
            trace = matrix.trace()
        except Exception as e:
            e1 = e.__str__()
        self.assertEqual("След может быть вычислен только для квадратной матрицы.", e1)


    def test5_can_sum_matrix(self):
        n, m = 6, 5
        sample1 = [[0, 0, 0, 0, 0], [0, 62, 0, 5, 0], [0, 3, 5, 0, 0], [0, 0, 32, 9, 0], [1, 0, 25, 0, 0], [6, 0, 46, 0, 0]]
        sample2 = [[8, 0, 0, -2, 0], [0, 7, 0, 43, 0], [0, 0, 49, 0, -9], [46, 33, 0, 0, 0], [4, 0, -8, 50, 0],
               [10, 0, -20, 0, 0]]
        matrix1 = setUpMatrix(n, m, sample1)
        matrix2 = setUpMatrix(n, m, sample2)

        matrix_sum = matrix1 + matrix2
        self.assertEqual([8, -2, 69, 48, 3, 54, -9, 46, 33, 32, 9, 5, 17, 50, 16, 26], matrix_sum.vector_not_zero)
        self.assertEqual([0, 3, 1, 3, 1, 2, 4, 0, 1, 2, 3, 0, 2, 3, 0, 2], matrix_sum.vector_not_zero_cols)
        self.assertEqual([0, 2, 4, 7, 11, 14, 16], matrix_sum.vector_elemets_in_row)

    def test6_can_sum_matrix_error(self):
        n, m = 6, 5
        sample1 = [[0, 0, 0, 0, 0], [0, 62, 0, 5, 0], [0, 3, 5, 0, 0], [0, 0, 32, 9, 0], [1, 0, 25, 0, 0], [6, 0, 46, 0, 0]]
        sample2 = [[8, 0, 0, 2, 0, 0], [0, 7, 0, 4, 0, 0], [11, 0, 49, 5, 9, 1], [46, 0, 0, 0, 0, 3], [0, 0, 20, 0, 0, 4]]
        matrix1 = setUpMatrix(n, m, sample1)
        matrix2 = setUpMatrix(n - 1, m + 1, sample2)

        e1 = None
        try:
            matrix_sum = matrix1 + matrix2
        except Exception as e:
            e1 = e.__str__()
        self.assertEqual('Несоответствие размеров матриц', e1)

    def test7_can_multiplicate_by_scalar(self):
        n, m = 6, 5
        sample = [[0, 0, 0, 0, 0], [0, 62, 0, 5, 0], [0, 3, 5, 0, 0], [0, 0, 32, 9, 0], [1, 0, 25, 0, 0], [6, 0, 46, 0, 0]]
        matrix = setUpMatrix(n, m, sample)

        new_matrix = matrix * 3
        new_matrix2 = 3 * matrix
        self.assertEqual([186, 15, 9, 15, 96, 27, 3, 75, 18, 138], new_matrix.vector_not_zero,)
        self.assertEqual([186, 15, 9, 15, 96, 27, 3, 75, 18, 138], new_matrix2.vector_not_zero)

    def test8_can_multiplicate_matrixes(self):
        n, m = 6, 5
        sample1 = [[0, 0, 0, 0, 0], [0, 62, 0, 5, 0], [0, 3, 5, 0, 0], [0, 0, 32, 9, 0], [1, 0, 25, 0, 0], [6, 0, 46, 0, 0]]
        sample2 = [[8, 0, 0, 2, 0, 0], [0, 7, 0, 4, 0, 0], [11, 0, 49, 5, 9, 1], [46, 0, 0, 0, 0, 3], [0, 0, 20, 0, 0, 4]]
        matrix1 = setUpMatrix(n, m, sample1)
        matrix2 = setUpMatrix(m, n, sample2)

        new_matrix = matrix2 @ matrix1
        self.assertEqual([64, 18, 434, 128, 71, 15, 147, 676, 45, 18, 138, 24, 60, 284], new_matrix.vector_not_zero)
        self.assertEqual([2, 3, 1, 2, 3, 0, 1, 2, 3, 0, 2, 0, 1, 2], new_matrix.vector_not_zero_cols)
        self.assertEqual([0, 2, 5, 9, 11, 14], new_matrix.vector_elemets_in_row)

    def test9_can_multiplicate_matrixes_error(self):
        n, m = 6, 5
        sample1 = [[0, 0, 0, 0, 0], [0, 62, 0, 5, 0], [0, 3, 5, 0, 0], [0, 0, 32, 9, 0], [1, 0, 25, 0, 0], [6, 0, 46, 0, 0]]
        sample2 = [[8, 0, 0, -2, 0], [0, 7, 0, 43, 0], [0, 0, 49, 0, -9], [46, 33, 0, 0, 0], [4, 0, -8, 50, 0],
               [10, 0, -20, 0, 0]]
        matrix1 = setUpMatrix(n, m, sample1)
        matrix2 = setUpMatrix(n - 1, m, sample2)

        e1 = None
        try:
            matrix_mul = matrix1 @ matrix2
        except Exception as e:
            e1 = e.__str__()
        self.assertEqual('Несоответствие размеров матриц', e1)

    def test10_can_find_determinant_4x4(self):
        n, m = 4, 4
        sample = [[-7, 0, 5, 4], [0, -6, 0, 5], [0, 3, 5, 0], [0, -1, -3, 9]]
        matrix = setUpMatrix(n, m, sample)

        det = matrix.determinant_and_is_reversed()
        self.assertEqual((2030, 'да'), det)

    def test11_can_find_determinant_2x2(self):
        n, m = 2, 2
        sample = [[-7, 2], [4, -6]]
        matrix = setUpMatrix(n, m, sample)

        det = matrix.determinant_and_is_reversed()

        self.assertEqual((34, 'да'), det)

    def test12_can_find_determinant_0(self):
        n, m = 3, 3
        sample = [[0, 0, 0], [0, 0, 5], [0, 3, 5]]
        matrix = setUpMatrix(n, m, sample)

        det = matrix.determinant_and_is_reversed()

        self.assertEqual((0, 'нет'), det)

    def test13_can_find_determinant_error(self):
        n, m = 5, 4
        sample = [[27, 0, 74, 4], [0, 62, 0, 5], [0, 3, 5, 0], [0, 0, 32, 9], [0, 0, 2, 5]]
        matrix = setUpMatrix(n, m, sample)

        e1 = None
        try:
            det = matrix.determinant_and_is_reversed()
        except Exception as e:
            e1 = e.__str__()
        self.assertEqual(e1, 'Определитель может быть вычислен только для квадратной матрицы.')
