from mod_int import *
from combo_testing import *
from bingroup import *
from configurations import *
from fractions import gcd
import json
#import time
import numpy as np
from spanningset import indspan_set_test
import group_gen
# class_ids = [78, 80]
with open("totalconfig13.json") as config_file:
    configs = json.load(config_file)

small_primes = [5, 7, 11, 13, 17, 19, 23]

ids = [2035]

# ids = [num+1 for num in range(0,31)]

#valid_ids = [num for num in ids if num == 183 or num == 228]
groups = group_gen.get_groups(32)
new_configs = [[configs[id-1], id] for id in ids]

with open("2035_results_32", "w") as text_file:
    for config in new_configs:
        c = Configuration(config[0])
        det = c.get_determinant()

        rank_vector = c.get_rank_vector()
        text_file.write("\n\n\n\n\nCONFIGURATION #{0}\n".format(config[1]))
        print "\n\n\nCONFIGURATION #{0}\n".format(config[1])
        print "Determinant: {0}".format(det)
        print "Rank Vector: {0}".format(rank_vector)
        text_file.write("Rank Vector: {0}\n".format(rank_vector))
        text_file.write("Determinant: {0}\n\n".format(det))
        for group in groups:
             if (abs(det) % group.get_size() < .0001):
                result = test_combinations(group, Configuration(config[0]))
                print group.get_composition()
                if result is not None:
                    text_file.write(str(group.get_composition()) + "\n")
                    text_file.write("Success: \n")
                    text_file.write(str(result))
                    text_file.write("\n\n")
                    print "Success: "
                    print result
                    print "\n"
                else:
                    print "Failure\n"
