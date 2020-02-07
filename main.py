from mod_int import *
from combo_testing import *
from bingroup import *
from configurations import *
import json
#import time
import numpy as np
from spanningset import indspan_set_test
import group_gen
from mod_linalg import *
import copy
from charpoly import *

groups = group_gen.get_all_groups_in_range(12,24)
config = Desargues()
det = 0

for group in groups:
    print det % group.get_size()




