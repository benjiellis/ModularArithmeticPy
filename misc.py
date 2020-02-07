from mod_int import *
from combo_testing import *
from bingroup import *
from configurations import *
import json
#import time
import numpy as np
from spanningset import indspan_set_test
import group_gen
import collineations
import solution_saver

config = Pappus()
groups = solution_saver.group_gen_modified(9)


for group in groups:
    print group.mod_tuple
    list = solution_saver.get_magic_solutions(group, config)
    print list
