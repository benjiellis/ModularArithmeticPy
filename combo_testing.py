from itertools import permutations

def are_lines_equal(line_array):
    line_value = line_array[0].sum()
    array_size = len(line_array)
    are_lines_equal = True
    i=1
    while are_lines_equal == True and i < array_size:
        if line_array[i].sum() != line_value:
                are_lines_equal = False
        i += 1
    return are_lines_equal

def lines_filled_out(line_array):
    filled_lines_array = []
    for line in line_array:
        if line.filled_out():
            filled_lines_array.append(line)

    return filled_lines_array

def add_point(Group, line_array, point_array, group_array, used_elements, step, success_bool):

    current = 0
    while success_bool == False and current < (Group.group_count - step):
        current_array = [i for i in group_array if i not in used_elements]
        point_array[step].value = current_array[current]
        used_elements.append(current_array[current])

        # UPDATE USED ELEMENTS WHEN PASSING TO NEXT LEVEL

        filled_out = lines_filled_out(line_array)

        if filled_out:
            if are_lines_equal(filled_out):

                if len(filled_out) == len(line_array):
                    success_bool = True
                    return success_bool

                else:
                    # REITERATE

                    next_step = step + 1

                    if add_point(Group, line_array, point_array, group_array, used_elements, next_step, success_bool):
                        success_bool = True

                    if success_bool is True:
                        return success_bool

            else:
                pass

        else:
            # REITERATE

            next_step = step + 1
            if add_point(Group, line_array, point_array, group_array, used_elements, next_step, success_bool):
                success_bool = True

            if success_bool is True:
                return success_bool

        if step != 0:
            current += 1
            used_elements.pop()
        else:
            break


    if current == (Group.group_count - step):
        point_array[step].value = None

    return


def test_combinations(Group, config): # DOES NO ALGEBRA, BUT CHECKS FOR CORRECTNESS
    try:
        point_array = config.get_points()
        line_array = config.get_lines()

        if Group.group_count < len(point_array):
            raise ValueError('There are more points than group elements')

        group_array = Group.get_elements()

        good_combo_found = False
        used_elements = []
        step = 0
        if add_point(Group, line_array, point_array, group_array, used_elements, step, good_combo_found):
            good_combo_found = True

        if good_combo_found == True:
            return point_array
        else:
            return None

    except ValueError as err:
        print "The group has less elements than the configurations has points."
        return None




def test_combinations_brute(Group, config):
    try:
        point_array = config.get_points()
        line_array = config.get_lines()

        point_count = len(point_array)
        if Group.group_count < point_count:
            raise ValueError('There are more points than group elements')

        group_array = Group().get_elements

        group_prmts = permutations(group_array, point_count)
        good_prmt = None

        for prmt in group_prmts:
            for i in range(point_count):
                point_array[i].value = prmt[i]

            sums_uniquely = are_lines_equal(line_array)

            if sums_uniquely == True:
                good_prmt = tuple(prmt)

        return good_prmt # returns as None is no patterning found

    except ValueError as err:
        print err.args[0]
        raise