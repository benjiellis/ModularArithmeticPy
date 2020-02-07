from mod_int import *
from copy import deepcopy
small_primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
from numpy import linalg
from charpoly import *

class ModularMatrix(object):
    def __init__(self, matrix, modulus):
        try:
            if modulus not in small_primes:
                raise ValueError("Modulus must be a small prime (m < 47)")

            self.matrix = [[ModularInt(value, modulus) for value in row] for row in matrix]
            self._modulus = modulus

        except ValueError as err:
            print err.message

    def __len__(self):
        return len(self.matrix)

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __str__(self):
        string = ""
        for row in self:
            string += (str(row) + "\n")
        return string

    def __add__(self, other):
        try:
            if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
                raise ValueError("Matrices must be same size to add")

            new_matrix = ModularMatrix([[0 for x in row] for row in self.matrix], self._modulus)

            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    new_matrix[i][j] = self.matrix[i][j] + other.matrix[i][j]

            return new_matrix

        except ValueError as err:
            print err.message
            raise

    def __mul__(self, other):
        try:
            if len(self.matrix[0]) != len(other.matrix):
                raise ValueError("Incorrect dimensions for matrix multiplication")

            new_matrix = ModularMatrix([[0 for x in range(len(other.matrix[0]))] for x in range(len(self.matrix))], self._modulus)

            for i in range(len(new_matrix.matrix)):
                for j in range(len(new_matrix.matrix[0])):
                    vector1 = self.matrix[i]
                    vector2 = [row[j] for row in other.matrix]
                    new_matrix[i][j] = sum(a*b for a,b in zip(vector1, vector2))

            return new_matrix

        except ValueError as err:
            print err.message
            raise

    def set_modulus(self, modulus):
        try:
            if modulus not in small_primes:
                raise ValueError("Modulus must be a small prime (m < 47)")

            self._modulus = modulus

            self.matrix = [[ModularInt(modint.residue, modulus) for modint in row] for row in self.matrix]

        except ValueError as err:
            print err.message
            raise

    def get_modulus(self):
        return self._modulus

    def get_determinant(self):
        new_matrix = [[entry.residue for entry in row] for row in self.matrix]
        det = linalg.det(new_matrix)
        if abs(det) < .0000001:
            return 0.0
        else:
            return (det % self._modulus)

    def switch_rows(self, row1, row2):
        if row1 == row2:
            return
        self.matrix[row1], self.matrix[row2] = self.matrix[row2], self.matrix[row1]

        # print "Switching rows {0} and {1}".format(row1, row2)

    def place_leading_value(self, row_num, col_num): # place_number will be row and column cause the matrix will be a diagonal
        if self.matrix[row_num][col_num] != 0: # end if everything gucci
            return [0, 0]

        else: # if zero in desired place, find next row without zero
            leading_value_not_found = True
            i = row_num + 1
            while leading_value_not_found == True and i < len(self.matrix):
                if self.matrix[i][col_num] != 0:
                    leading_value_not_found = False

                else:
                    i += 1

            if i != len(self.matrix):
                self.switch_rows(i, row_num)
                return [i, row_num]
            else:
                return None

    def add_row(self, add_from, add_to, multiple=1):
        try:
            new_row = []
            for i in range(len(add_from)):
                new_row.append((add_from[i] * multiple) + self[add_to][i])

            # print "Adding row {0} to row {1}".format(add_from, add_to)
            self[add_to] = new_row

        except TypeError:
            # print "Adding as row index"
            new_row = []
            for i in range(len(self[add_from])):
                new_row.append((self[add_from][i] * multiple) + self[add_to][i])

            # print "Adding row {0} to row {1}".format(add_from, add_to)
            self[add_to] = new_row

    def get_eigenvalues(self, input_poly=None):
        # this will be a doozie

        # step 1: get characteristic polynomial as a list of lists, with coefficients and powers in tuples (or lists)
            # step 1a: create polynomial class that correctly multiplies polynomials as lists of coefficients and powers

            # step 1b: reduce matrix through laplacian reduction (this will use a LOT of memory)

            # step 1c: return polynomial object

        # step 2: reduce characteristic polynomial in correct modulus
        if input_poly is not None:
            char_poly = input_poly
            for term in char_poly:
                term[0] = ModularInt(term[0], self._modulus)
        else:
            char_poly = self.get_char_poly()

        # step 3: run through values of Z_p to see which fit polynomial
            # step 3a: give zeros back if no constant term, with correct multiplicity
                # find minimum power and "factor it out" by subtracting from the others

            # step 3b: figure out how to get algebraic multiplicity of all other eigenvalues
        evals = []
        for i in range(self._modulus):
            if char_poly.evaluate(ModularInt(i, self._modulus)) == 0:
                evals.append(i)

        # step 4: check correct number of eigenvalues
        return evals

    def get_char_poly(self):
        non_mod_matrix = [[value.residue for value in row] for row in self.matrix]
        char_poly = characteristic_polynomial(non_mod_matrix)
        for term in char_poly:
            term[0] = ModularInt(term[0], self._modulus)
        return char_poly


    def diagonalize(self):
        col_num = 0
        row_num = 0

        while col_num < len(self[0]):
            if self.place_leading_value(row_num, col_num) is not None:
                # if place switch successful, go through all lower rows in column and reduce to zero
                for i in range(row_num + 1, len(self)):
                    if self[i][col_num] == 0:
                        pass # if zero, go down a column
                    else:
                        # if not zero, then reduce row to zero
                        while self[i][col_num] != 0: # find better way to find out exact multiple to add
                            self.add_row(row_num, i)

                # then go down a row and over a column
                row_num += 1
                col_num += 1
            else:
                # if place switch unsuccessful, then go to next column
                col_num += 1

        return self

    def get_diagonalization(self):
        mod_matrix = deepcopy(self)

        col_num = 0
        row_num = 0

        while col_num < len(mod_matrix[0]):
            if mod_matrix.place_leading_value(row_num, col_num) is not None:
                # if place switch successful, go through all lower rows in column and reduce to zero
                for i in range(row_num + 1, len(mod_matrix)):
                    if mod_matrix[i][col_num] == 0:
                        pass # if zero, go down a column
                    else:
                        # if not zero, then reduce row to zero
                        while mod_matrix[i][col_num] != 0: # find better way to find out exact multiple to add
                            mod_matrix.add_row(row_num, i)

                # then go down a row and over a column
                row_num += 1
                col_num += 1
            else:
                # if place switch unsuccessful, then go to next column
                col_num += 1

        return mod_matrix

    def get_rank(self):

        mod_matrix = self.get_diagonalization()

        # for row in mod_matrix:
            # print row
        # return the number of rows minus number of rows with all zeros
        num_zero_rows = 0

        for row in mod_matrix:
            all_zeros = True
            for value in row:
                if value != 0:
                    all_zeros = False
                    break

            if all_zeros == True:
                num_zero_rows += 1

        # print mod_matrix
        return len(mod_matrix) - num_zero_rows

    def invert(self):
        self.matrix = self.get_inverse().matrix
        return self

    def get_inverse(self):
        try:
            if len(self.matrix) != len(self.matrix[0]):
                raise ValueError("Matrix must be square to find an inverse.")

            if self._modulus not in small_primes:
                raise ValueError("Modulus must be a small prime to find inverse")

            if self.get_rank() != len(self.matrix):
                raise ValueError("Matrix must not be singular in given modulus")

            identity = ModularIdentity(len(self.matrix), self._modulus)

            mod_matrix = deepcopy(self)

            place_num = 0

            while place_num < len(mod_matrix):
                rows = mod_matrix.place_leading_value(place_num, place_num)
                if rows is None:
                    raise RuntimeError("Unable to find leading value")

                identity.switch_rows(rows[0], rows[1])

                for i in range(len(mod_matrix)):
                    if i == place_num:
                        if mod_matrix[i][place_num] == 1:
                            pass # if one, go down a column
                        else:
                            # if not one, then reduce row to one
                            add_from = deepcopy(mod_matrix[i])
                            add_from_i = deepcopy(identity[i])
                            while mod_matrix[i][place_num] != 1: # find better way to find out exact multiple to add
                                mod_matrix.add_row(add_from, i)
                                identity.add_row(add_from_i, i)
                    else:
                        if mod_matrix[i][place_num] == 0:
                            pass # if zero, go down a column
                        else:
                            # if not zero, then reduce row to zero
                            add_from = deepcopy(mod_matrix[place_num])
                            add_from_i = deepcopy(identity[place_num])
                            while mod_matrix[i][place_num] != 0: # find better way to find out exact multiple to add
                                mod_matrix.add_row(add_from, i)
                                identity.add_row(add_from_i, i)

                # then go down a row and over a column
                place_num += 1

            return identity

        except ValueError as err:
            print err.message
            raise
        except RuntimeError as err:
            print err.message
            raise

class ModularIdentity(ModularMatrix):
    def __init__(self, size, modulus):
        matrix = [[0 for x in range(size)] for x in range(size)]
        for i in range(size):
            matrix[i][i] = 1
        super(ModularIdentity, self).__init__(matrix, modulus)

class ModularRVector(ModularMatrix):
    def __init__(self, list, modulus):
        matrix = [list]
        super(ModularRVector, self).__init__(matrix, modulus)

class ModularCVector(ModularMatrix):
    def __init__(self, list, modulus):
        matrix = [[x] for x in list]
        super(ModularCVector, self).__init__(matrix, modulus)

def modular_rank(matrix, modulus):
    try:
        if modulus not in small_primes:
            raise ValueError('Only small prime numbers are currently supported as moduli')
        # turn all entries in the matrix into mod_ints of the correct modulus

        mod_matrix = ModularMatrix(matrix, modulus)
        # perform Gaussian elimination with some rule tweaks

        col_num = 0
        row_num = 0

        while col_num < len(mod_matrix[0]):
            if mod_matrix.place_leading_value(row_num, col_num) is not None:
                # if place switch successful, go through all lower rows in column and reduce to zero
                for i in range(row_num + 1, len(mod_matrix)):
                    if mod_matrix[i][col_num] == 0:
                        pass # if zero, go down a column
                    else:
                        # if not zero, then reduce row to zero
                        while mod_matrix[i][col_num] != 0: # find better way to find out exact multiple to add
                            mod_matrix.add_row(row_num, i)

                # then go down a row and over a column
                row_num += 1
                col_num += 1
            else:
                # if place switch unsuccessful, then go to next column
                col_num += 1

        for row in mod_matrix:
            print row
        # return the number of rows minus number of rows with all zeros
        num_zero_rows = 0

        for row in mod_matrix:
            all_zeros = True
            for value in row:
                if value != 0:
                    all_zeros = False
                    break

            if all_zeros == True:
                num_zero_rows += 1

        return len(matrix) - num_zero_rows

    except ValueError as err:
        print err.message

