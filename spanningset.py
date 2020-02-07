from configurations import *

def indspan_set_test(configuration):
    lines = configuration.get_lines()

    set_found = False
    pt_list = []
    used_lines = []
    step = 1

    if choose_next_pt(configuration, lines, pt_list, used_lines, step):
        return [point.id for point in pt_list]
    else:
        return None

def choose_next_pt(configuration, lines, pt_list, used_lines, step):
    try:
        i = 0
        set_found_bool = False
        under_point_limit = step <= len(lines) / 3
        while set_found_bool == False and i < len(lines[0]) and under_point_limit:
            remaining_lines = [line for line in lines if line not in used_lines]

            if not remaining_lines:
                raise IndexError("Error at step {0} at count {1}.".format(step, i))

            next_pt = remaining_lines[0][i]
            pt_list.append(next_pt)

            if configuration.test_adjacency(next_pt, *pt_list[:-1]) and step != 1:
                pass

            else:
                next_used_lines = used_lines + configuration.get_lines_with_point(next_pt)
                if len(next_used_lines) == len(lines) and step == len(lines) / 3:
                    set_found_bool = True
                else:
                    next_step = step + 1
                    if choose_next_pt(configuration, lines, pt_list, next_used_lines, next_step):
                        set_found_bool = True

            if set_found_bool == False:
                i += 1
                pt_list.pop()

        return set_found_bool

    except IndexError as err:
        print err.message


