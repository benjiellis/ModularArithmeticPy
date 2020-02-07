from group_gen import *
from copy import deepcopy

class GroupElement(object):
    def __init__(self, mod_tuple, value_list):
        try:
            if len(mod_tuple) != len(value_list):
                raise ValueError("mod_tuple must be same length as value_list")
            self.mod_tuple = mod_tuple
            self.value_list = value_list

        except ValueError as err:
            print err.message
            raise

    def __neg__(self):
        new_value_list = [self.value_list[i] % self.mod_tuple[i] for i in range(len(self.value_list))]
        return GroupElement(self.mod_tuple, new_value_list)

    def __add__(self, other):
        try:
            if self.mod_tuple != other.mod_tuple:
                raise ValueError("can only add group_element with same mod_tuple")

            new_value_list = [(self.value_list[i]+other.value_list[i]) % self.mod_tuple[i] for i in range(len(self.value_list))]
            return GroupElement(self.mod_tuple, new_value_list)

        except ValueError as err:
            print err.message
            raise
        except AttributeError:
            if (other == 0) or (other is None):
                return GroupElement(self.mod_tuple, self.value_list)

    def __radd__(self, other):
        try:
            if (other == 0):
                return deepcopy(self)
            else:
                raise ValueError("cannot sum ints!=0 to group elements")

        except ValueError as err:
            print err.message
            raise


    def __eq__(self, other):
        cond1 = (self.value_list == other.value_list)
        cond2 = (self.mod_tuple == other.mod_tuple)
        if cond1 and cond2:
            return True
        else:
            return False

    def __str__(self):
        return str(self.value_list)

    __repr__ = __str__

    def get_group_elements(self):
        element_list = []
        list_of_factor_values = []
        for factor in self.mod_tuple:
            new_list = [i for i in range(factor)]
            list_of_factor_values.append(new_list)
        unprocessed_element_list = product(*list_of_factor_values)
        for element in unprocessed_element_list:
            element_list.append(GroupElement(self.mod_tuple, element))

        return element_list

def group_gen_modified(order):
    group_factors = get_combinations(order)

    group_list = []

    for factor_set in group_factors:
        group_list.append(GroupElement(tuple(factor_set), [0 for i in range(len(factor_set))]))

    return group_list

def get_magic_solutions(group_representative, config):
    try:
        point_queue = extract_point_ids(config)
        point_set = set(point_queue)
        line_set = extract_line_sets(config)

        mapping_function = dict()
        solution_list = []

        group_elements = set(group_representative.get_group_elements())

        assign_point(point_set, point_queue, line_set, group_elements, mapping_function, solution_list)

        return solution_list

    except ValueError as err:
        print "The group has less elements than the configurations has points."
        return None

def extract_point_ids(config):
    return [point.id for point in config.get_points()]

def extract_line_sets(config):
    to_return = set()
    for line in config.get_lines():
        line_to_add = set()
        for point in line:
            line_to_add.add(point.id)
        frozen_to_add = frozenset(line_to_add)
        to_return.add(frozen_to_add)
    return to_return

def do_lines_work_out(line_set, mapping_function):
    valid_lines = []
    for line in line_set:
        entire_line_in_mapping_function = True
        for point in line:
            if point not in mapping_function:
                entire_line_in_mapping_function = False
        if entire_line_in_mapping_function:
            valid_lines.append(line)

    if valid_lines:
        image = [mapping_function[point] for point in valid_lines[0]]
        total = sum(image)

        for line in valid_lines[1:]:
            image1 = [mapping_function[point] for point in line]
            total1 = sum(image1)
            if (total1 != total):
                return False

        return True
    else:
        return True

def assign_point(point_set, point_queue, line_set, group_elements, mapping_function, solution_list):
    # check to see if free points
        # if none, add to solution_list and return

    if len(point_queue) == 0:
        solution_list.append(deepcopy(mapping_function))
        print mapping_function
        return

    mapped_values = [mapping_function[key] for key in mapping_function]

    to_assign = point_queue[0]
    for value in group_elements:
        if value in mapped_values:
            continue

        new_mapping_function = deepcopy(mapping_function)
        new_mapping_function[to_assign] = value

        if do_lines_work_out(line_set, new_mapping_function):
            new_point_queue = point_queue[1:]
            assign_point(point_set, new_point_queue, line_set, group_elements, new_mapping_function, solution_list)

    return
