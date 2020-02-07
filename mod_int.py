from itertools import product
from operator import mul
small_primes = [2,3,5,7,11,13,17,19,23,27,29,31,37,41,43,47]

class ModularInt(object):
    def __init__(self, residue=0, modulus=None):
        self.residue = residue % modulus
        self._modulus = modulus
        self.group_count = modulus

    def __neg__(self):
        return ModularInt(-self.residue % self._modulus, self._modulus)

    def inverse(self):
        try:
            if self._modulus not in small_primes:
                raise ValueError("Modular integer must have prime moduli to find inverse")

            inverse = None
            for i in range(self._modulus):
                if ((self.residue * i) % self._modulus) == 1:
                    inverse = i

            return ModularInt(inverse, self._modulus)

        except ValueError as err:
            print err.message
            raise

    def __add__(self, other):
        try:
            if self._modulus != other._modulus:
                raise ModulusComputationError
            sum = self.residue + other.residue
            sum_mod = sum % self._modulus
            return ModularInt(sum_mod, self._modulus)
        except ModulusComputationError as err:
            print err.message
        except AttributeError:
            return ModularInt((self.residue + other) % self._modulus, self._modulus)

    def __radd__(self, other):
        return (self.residue + other) % self._modulus

    def __mul__(self, other):
        try:
            if other._modulus != self._modulus:
                raise ValueError("Cannot multiply modular integers with different moduli")

            return ModularInt((other.residue * self.residue) % self._modulus, self._modulus)

        except ValueError as err:
            print err.message
            raise
        except AttributeError:
            return ModularInt((other * self.residue) % self._modulus, self._modulus)

    def __rmul__(self, other):
        return ModularInt((other * self.residue) % self._modulus, self._modulus)

    def __div__(self, other):
        try:
            if self._modulus != other._modulus:
                raise ValueError("Cannot divide modular integers with different moduli")
            if self._modulus not in small_primes:
                raise ValueError("Can only divide modular integers in rings with prime order")

            return (self * other.inverse())

        except ValueError as err:
            print err.message
            raise

    def __pow__(self, power):
        return ModularInt((self.residue ** power) % self._modulus, self._modulus)

    def __eq__(self, other):
        try:
            if other is None:
                return False
            if hasattr(other, '_modulus'):
                if self._modulus != other._modulus:
                    raise ModulusComparisonError
                if self.residue == other.residue:
                    return True
            else:
                if self.residue == other:
                    return True
                else:
                    return False

        except ModulusComparisonError as err:
            print err.message

    def __ne__(self, other):
        try:
            if hasattr(other, '_modulus'):
                if self._modulus != other._modulus:
                    raise ModulusComparisonError
                if self.residue != other.residue:
                    return True
            else:
                if self.residue != other:
                    return True
                else:
                    return False
        except ModulusComparisonError as err:
            print err.message

    def __str__(self):
        return str(self.residue)

    def get_elements(self):
        element_array = []
        for i in range(self._modulus):
            element_array.append(ModularInt(i, self._modulus))
        return element_array

    __repr__ = __str__


class MultiModInt(ModularInt):
    def __init__(self, residue, modulus):
        super(MultiModInt, self).__init__(residue, modulus)

    def __add__(self, other):
        try:
            if self._modulus != other._modulus:
                raise ModulusComputationError
            return ModularInt((self.residue * other.residue) % self._modulus, self._modulus)
        except ModulusComputationError as err:
            print err.message


class ModulusComputationError(Exception):
    def __init__(self):
        self.message = "Two ModInts with different moduli computed together."


class ModulusComparisonError(Exception):
    def __init__(self):
        self.message = "Two ModInts with different moduli were compared."


class Mod3(ModularInt):
    group_count = 3
    def __init__(self, value=0):
        super(Mod3, self).__init__(value, 3)


class Mod8(ModularInt):
    group_count = 8
    def __init__(self, value=0):
        super(Mod8, self).__init__(value, 8)


class Mod9(ModularInt):
    group_count = 9
    def __init__(self, value=0):
        super(Mod9, self).__init__(value, 9)


class Mod10(ModularInt):
    group_count = 10
    def __init__(self, value=0):
        super(Mod10, self).__init__(value, 10)


class Mod11(ModularInt):
    group_count = 11
    def __init__(self, value=0):
        super(Mod11, self).__init__(value, 11)


class Mod12(ModularInt):
    group_count = 12
    def __init__(self, value=0):
        super(Mod12, self).__init__(value, 12)


class Mod13(ModularInt):
    group_count = 13
    def __init__(self, value=0):
        super(Mod13, self).__init__(value, 13)


class Mod14(ModularInt):
    group_count = 14
    def __init__(self, value=0):
        super(Mod14, self).__init__(value, 14)


class Mod15(ModularInt):
    group_count = 15
    def __init__(self, value=0):
        super(Mod15, self).__init__(value, 15)


class Mod18(ModularInt):
    group_count = 18
    def __init__(self, value=0):
        super(Mod18, self).__init__(value, 18)


class Mod20(ModularInt):
    group_count = 20
    def __init__(self, value=0):
        super(Mod20, self).__init__(value, 20)


class Mod25(ModularInt):
    group_count = 25
    def __init__(self, value=0):
        super(Mod25, self).__init__(value, 25)


class Mod30(ModularInt):
    group_count = 30
    def __init__(self, value=0):
        super(Mod30, self).__init__(value, 30)


class Mod35(ModularInt):
    group_count = 35
    def __init__(self, value=0):
        super(Mod35, self).__init__(value, 35)


class Mod60(ModularInt):
    group_count = 60
    def __init__(self, value=0):
        super(Mod60, self).__init__(value, 60)


class ComposedGroup(object):
    def __init__(self, *values):
        self.values_list = list(values)
        self.group_count = reduce(mul, [i.group_count for i in self.values_list])

    def __add__(self, other):
        try:
            if len(self.values_list) != len(other.values_list):
                raise ValueError("Composed Group objects have different lengths")

            new_values = [a + b for a,b in zip(self.values_list, other.values_list)]
            return ComposedGroup(*new_values)

        except ValueError as err:
            print err.message
            raise

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            raise ValueError("Something besides a ComposedGroup tried to add to a ComposedGroup.")

    def __eq__(self, other):
        if other is None:
            return False
        if self.values_list == other.values_list:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.values_list != other.values_list:
            return True
        else:
            return False

    def __str__(self):
        return str(self.values_list)

    def get_elements(self):
        group_element_array = []
        for value in self.values_list:
            group_element_array.append(value.get_elements())

        values = [ComposedGroup(*values) for values in product(*group_element_array)]

        return values

    def get_composition(self):
        return [value._modulus for value in self.values_list]

    def get_size(self):
        return self.group_count

    __repr__ = __str__

class Mod3x3(ComposedGroup):
    group_count = 9
    def __init__(self, val1=0, val2=0):
        super(Mod3x3, self).__init__(Mod3(val1), Mod3(val2))


