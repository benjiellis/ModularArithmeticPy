from numpy import linalg
small_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
from mod_linalg import ModularMatrix

class Point(object):
    def __init__(self, val=None, id=-1):
        self.value = val
        self.id = id

    def __str__(self):
        return str(self.value)

    __repr__ = __str__

    def __add__(self, other):
        return Point(self.value + other.value)

class Line(object):
    def __init__(self, *points):
        self.points = list(points)

    def matrix_has(self, test):
        if test in self.points:
            return 1
        else:
            return 0

    def has(self, test):
        if test in self.points:
            return True
        else:
            return False

    def sum(self):
        return sum(point.value for point in self.points)

    def filled_out(self):
        if None not in [point.value for point in self.points]:
            return True
        else:
            return False

    def __getitem__(self, x):
        return self.points[x]

    def __len__(self):
        return len(self.points)

    def __str__(self):
        return str(self.points)

    __repr__ = __str__


class Configuration(object):
    def __init__(self, line_matrix):
        self.points = [Point(id=i) for i in range(len(line_matrix))]
        self.lines = [Line(self.points[line_matrix[i][0]], self.points[line_matrix[i][1]], self.points[line_matrix[i][2]]) for i in range(len(line_matrix))]

    def get_points(self):
        return self.points

    def get_lines(self):
        return self.lines

    def get_adjacency_matrix(self):
        return [[line.matrix_has(point) for point in self.points] for line in self.lines]

    def get_determinant(self):
        determinant = linalg.det(self.get_adjacency_matrix())
        if abs(determinant) < .0000001:
            return 0.0
        else:
            return determinant

    def test_adjacency(self, p1, *args):
        if args:
            for arg in args:
                for line in self.lines:
                    cond1 = line.has(p1)
                    cond2 = line.has(arg)
                    if cond1 and cond2:
                        return True

            return False

    def get_lines_with_point(self, p1):
        return [line for line in self.lines if line.has(p1)]

    def get_rank_vector(self):
        rank_vector = []
        adj_mat = self.get_adjacency_matrix()
        for prime in small_primes:
            rank_vector.append(ModularMatrix(adj_mat, prime).get_rank())

        return rank_vector

    def get_indices(self, alpha=False):
        if alpha == True:
            indices = [[chr(point.id + ord('a')) for point in line] for line in self.lines]
        else:
            indices = [[point.id for point in line] for line in self.lines]
        return indices

    def print_indices(self, alpha=False):
        for list in self.get_indices(alpha=alpha):
            if alpha == True:
                print '['+list[0]+', '+list[1]+', '+list[2]+']'
            else:
                print list

class Pappus(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,2],[0,3,7],[0,4,8],[1,3,6],[1,5,8],[2,4,6],[2,5,7],[3,4,5],[6,7,8]]
        super(Pappus, self).__init__(self._line_matrix)


class MobiusKantor(Configuration):
    def __init__(self):
        self._line_matrix = [[0,3,4],[0,1,5],[0,2,7],[1,4,7],[2,3,5],[1,3,6],[2,4,6],[5,6,7]]
        super(MobiusKantor, self).__init__(self._line_matrix)


class Config9_2(Configuration):
    def __init__(self):
        self._line_matrix = [[0,3,6],[0,1,8],[0,2,5],[1,2,3],[1,5,7],[3,4,7],[2,4,6],[4,5,8],[6,7,8]]
        super(Config9_2, self).__init__(self._line_matrix)


class Config9_3(Configuration):
    def __init__(self):
        self._line_matrix = [[0,4,5],[0,1,2],[2,3,4],[1,4,6],[0,7,3],[2,5,8],[5,6,7],[3,6,8],[1,7,8]]
        super(Config9_3, self).__init__(self._line_matrix)


class Sym12(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,2],[0,3,9],[2,8,11],[9,10,11],[0,5,10],[1,6,11],[2,3,4],[7,8,9],[1,4,5],[4,6,8],[3,5,7],[6,7,10]]
        super(Sym12, self).__init__(self._line_matrix)


class Desargues(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,2],[2,3,4],[2,6,5],[7,8,9],[0,5,8],[0,3,9],[3,5,7],[4,6,7],[1,6,8],[1,4,9]]
        super(Desargues, self).__init__(self._line_matrix)


class Fano(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,4],[0,2,5],[0,3,6],[1,3,5],[1,2,6],[2,3,4],[4,5,6]]
        super(Fano, self).__init__(self._line_matrix)


class CremonaRichmond(Configuration):
    def __init__(self):
        self._line_matrix = [[1,2,3],[1,4,5],[1,6,7],[2,8,9],[2,10,11],[0,3,14],[3,12,13],[4,8,12],[4,10,14],[0,5,11],[5,9,13],[6,10,13],[0,6,8],[7,9,14],[7,11,12]]
        super(CremonaRichmond, self).__init__(self._line_matrix)

class Gray(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[9,10,11],[12,13,14],[15,16,17],[9,12,15],[10,13,16],[11,14,17],[18,19,20],[21,22,23],[24,25,26],[18,21,24],[19,22,25],[20,23,26],[0,9,18],[1,10,19],[2,11,20],[3,12,21],[4,13,22],[5,14,23],[6,15,24],[7,16,25],[8,17,26]]
        super(Gray, self).__init__(self._line_matrix)

class cyclic14(Configuration):
    def __init__(self):
        self._line_matrix = [[0,1,3],[1,2,4],[2,3,5],[3,4,6],[4,5,7],[5,6,8],[6,7,9],[7,8,10],[8,9,11],[9,10,12],[10,11,13],[11,12,0],[12,13,1],[13,0,2]]
        super(cyclic14, self).__init__(self._line_matrix)