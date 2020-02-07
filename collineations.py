from copy import copy, deepcopy

def get_collineation_count(config):
    point_queue = [point.id for point in config.get_points()]
    point_set = set(point_queue)
    line_set = set()
    for line in config.get_lines():
        line_to_add = set()
        for point in line:
            line_to_add.add(point.id)
        frozen_to_add = frozenset(line_to_add)
        line_set.add(frozen_to_add)
    collineation_count = [0]
    automorphism = dict()
    collineation_list = []

    assign_point(point_queue, point_set, line_set, automorphism, collineation_count, collineation_list)

    return [collineation_count[0], collineation_list]

def assign_point(point_queue, point_set, line_set, automorphism, collineation_count, collineation_list):
    unassigned_points = {point for point in point_set if point not in automorphism}

    if len(unassigned_points) == 0:
        collineation_count[0] += 1
        new_dict = deepcopy(automorphism)
        collineation_list.append(new_dict)
        return

    mapped_points = {automorphism[key] for key in automorphism}
    unmapped_points = point_set.difference(mapped_points)

    to_assign = point_queue[0]
    for to_map in unmapped_points:
        new_automorphism = deepcopy(automorphism)
        new_automorphism[to_assign] = to_map

        if do_lines_work_out(line_set, new_automorphism):
            new_point_queue = point_queue[1:]
            assign_point(new_point_queue, point_set, line_set, new_automorphism, collineation_count, collineation_list)

    return


def do_lines_work_out(line_set, automorphism):
    all_lines_work_so_far = True
    for line in line_set:
        entire_line_in_automorphism = True
        for point in line:
            if point not in automorphism:
                entire_line_in_automorphism = False

        if entire_line_in_automorphism == True:
            new_line = set()
            for point in line:
                new_line.add(automorphism[point])
            if new_line not in line_set:
                all_lines_work_so_far = False

    return all_lines_work_so_far
