from copy import deepcopy

class PolyError(Exception):
    def __init__(self, code, message):
        self.code = code
        super(PolyError, self).__init__(message)

class Polynomial(object):
    def __init__(self, constant=0, *coefficients):
        inputs = [constant] + list(coefficients)
        self.terms = []
        for i in range(len(inputs)):
            self.terms.append([inputs[i], i])

        self._order = len(inputs) - 1

    def __neg__(self):
        return Polynomial(*[-term[0] for term in self.terms])

    def __str__(self):
        string = ""
        string += str(self.terms[0][0])
        for term in self.terms[1:]:
            string += (" + " + str(term[0]) + "x^" + str(term[1]))

        return string

    def __add__(self, other):
        new_poly_l = []
        if self._order > other._order:
            for i in range(len(other.terms)):
                new_poly_l.append(self.terms[i][0] + other.terms[i][0])

            for term in self.terms[(other._order + 1):]:
                new_poly_l.append(term[0])

        elif self._order < other._order:
            for i in range(len(self.terms)):
                new_poly_l.append(self.terms[i][0] + other.terms[i][0])

            for term in other.terms[(self._order + 1):]:
                new_poly_l.append(term[0])

        else:
            for i in range(len(self.terms)):
                new_poly_l.append(self.terms[i][0] + other.terms[i][0])

        return Polynomial(*new_poly_l)

    def __div__(self, other):
        # implement polynomial division
        try:
            if self.terms[0]._modulus != other.terms[0]._modulus:
                raise TypeError("Polynomials with modular integers must have the same moduli")
        except AttributeError as err:
            pass
        except TypeError as err:
            print err.message
            raise

        try:
            if self._order < other._order:
                raise PolyError(0, "Divisor has higher order than dividend")

            new_poly_l = poly_division(self, other)
            return Polynomial(new_poly_l)

        except PolyError as err:
            if err.code == 0:
                print err.message
                raise
            elif err.code == 1:
                print err.message
                raise

    def __sub__(self, other):
        neg_l = [(term[0] * -1) for term in other.terms]
        neg_poly = Polynomial(*neg_l)
        return (self + neg_poly)

    def __len__(self):
        return self._order

    __repr__ = __str__

    def __getitem__(self, index):
        return self.terms[index]

    def __setitem__(self, key, value):
        self.terms[key] = value

    def mul_by_term(self, term):
        new_poly_l = [0 for i in range(term[1])]

        for item in self.terms:
            new_poly_l.append(item[0] * term[0])

        return Polynomial(*new_poly_l)

    def __mul__(self, other):
        try:
            new_poly = Polynomial()

            for term in self.terms:
                term_poly = other.mul_by_term(term)
                new_poly += term_poly

            return new_poly

        except AttributeError:
            new_poly = deepcopy(self)

            for term in new_poly.terms:
                term[0] = other * term[0]

            return new_poly

    def __rmul__(self, other):
        new_poly = deepcopy(self)

        for term in new_poly.terms:
            term[0] = other * term[0]

        return new_poly

    def evaluate(self, value):
        list = [term[0] * (value ** term[1]) for term in self]
        return sum(list)

    def bump_order(self, inc):
        return Polynomial(*([0]*inc + [term[0] for term in self.terms]))

    def pop_highest(self):
        list = [term[0] for term in self.terms]
        list.pop()
        return Polynomial(*list)

def poly_division(dividend, divisor):
    try:
        if dividend._order == divisor._order:
            does_divide = True
            multiple = dividend.terms[dividend._order][0] / divisor.terms[divisor._order][0]
            for (dividend_term, divisor_term) in zip(dividend.terms, divisor.terms):
                if divisor_term[0] * multiple != dividend_term[0]:
                    does_divide = False

            if does_divide == True:
                return [multiple]
            else:
                raise PolyError(1, "does not divide")

        multiple = dividend.terms[dividend._order][0] / divisor.terms[divisor._order][0]
        new_dividend = deepcopy(dividend) - (multiple * divisor.bump_order(dividend._order - divisor._order))
        new_dividend.pop_highest()
        return poly_division(new_dividend, divisor) + [multiple]

    except PolyError as err:
        if err.code == 1:
            raise



def get_cofactor(matrix, row_num, col_num):
    new_matrix = deepcopy(matrix)
    new_matrix.pop(row_num)
    for row in new_matrix:
        row.pop(col_num)

    return new_matrix

def laplace_expand(matrix):
    if len(matrix) == 2:
        return (matrix[0][0] * matrix[1][1]) - (matrix[0][1] * matrix[1][0])

    new_poly = Polynomial()

    for i in range(len(matrix)):
        cofactor = get_cofactor(matrix, 0, i)
        sign = (-1 if i % 2 != 0 else 1)
        if matrix[0][i] == 0:
            pass
        else:
            new_poly += ((sign * matrix[0][i]) * laplace_expand(cofactor))

    return new_poly

def characteristic_polynomial(matrix):
    try:
        if len(matrix) != len(matrix[0]):
            raise ValueError("Matrix must be square to find characteristic polynomial")
        # step 1: get characteristic polynomial as a list of lists, with coefficients and powers in tuples (or lists)
            # step 1a: create polynomial class that correctly multiplies polynomials as lists of coefficients and powers

            # step 1b: reduce matrix through laplacian expansion (this will use a LOT of memory)

        poly_matrix = [[Polynomial(value) for value in row] for row in matrix] # turns all entries into constant polynomials

        for i in range(len(poly_matrix)): # turn diagonal into linear polynomials (constant minus lambda)
            poly_matrix[i][i] += Polynomial(*[0, -1])

        char_poly = laplace_expand(poly_matrix)

        return char_poly

            # step 1c: return polynomial object

        # step 2: reduce characteristic polynomial in correct modulus
            # easy peasy

    except ValueError as err:
        print err.message
        raise


