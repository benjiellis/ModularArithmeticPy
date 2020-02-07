class BinGroup(object):
    def __init__(self, value, group_dim):
        self.bits = value & ((2 ** group_dim) - 1)
        self.group_dim = group_dim

    def __add__(self, other):
        return BinGroup(self.bits ^ other.bits, self.group_dim)

    def __radd__(self, other):
        return self.bits ^ other

    def __eq__(self, other):
        if self.bits == other.bits:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.bits != other.bits:
            return True
        else:
            return False

    def __str__(self):
        return "{0:b}".format(self.bits)

    def get_elements(self):
        elements_array = []
        for i in range(2 ** self.group_dim):
            elements_array.append(BinGroup(i, self.group_dim))
        return elements_array

    __repr__ = __str__

class BinGroup8(BinGroup):
    group_count = 8
    def __init__(self, value):
        super(BinGroup8, self).__init__(value, 3)

class BinGroup16(BinGroup):
    group_count = 16
    def __init__(self, value):
        super(BinGroup16, self).__init__(value, 4)
