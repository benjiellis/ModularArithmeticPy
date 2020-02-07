import json
from configurations import *
from collineations import *

with open("totalconfig13.json") as config_file:
    configs = json.load(config_file)

valid_ids = [35,38,53,62,91,108,116,131,177,179,184,213,247,249,253,260,263,317,322,323,343,346,379,383,393,432,439,448,453,465,467,
             505, 512, 522, 527, 542, 543, 553, 575, 632, 691, 766, 790, 791, 846, 847, 854, 881, 891, 898, 936, 947, 962, 970, 975,
             979, 984, 985, 986, 1000, 1051, 1052, 1059, 1064, 1067, 1075, 1078, 1087, 1110, 1111, 1126, 1132, 1152, 1156, 1189, 1198,
             1211, 1218, 1220, 1221, 1224, 1240, 1243, 1250, 1259, 1268, 1272, 1293, 1313, 1317, 1337, 1353, 1355, 1375, 1379, 1381,
             1389, 1390, 1394, 1404, 1408, 1411, 1413, 1415, 1450, 1451, 1459, 1478, 1480, 1486, 1492, 1495, 1508, 1512, 1515, 1527,
             1528, 1534, 1555, 1594, 1610, 1612, 1624, 1667, 1671, 1692, 1712, 1719, 1725, 1740, 1741, 1772, 1773, 1774, 1779, 1780,
             1790, 1793, 1795, 1801, 1803, 1807, 1816, 1827, 1828, 1836, 1837, 1843, 1851, 1866, 1870, 1877, 1879, 1883, 1889, 1893,
             1899, 1903, 1911, 1912, 1916, 1921, 1929, 1932, 1936, 1943, 1946, 1947, 1952, 1953, 1955, 1958, 1963, 1971, 1974, 1975,
             1981, 1982, 1984, 1986, 1990, 1991, 1993, 1996, 1997, 2001, 2002, 2014, 2016, 2022, 2025, 2028, 2029, 2031, 2033, 2034,
             2035, 2036]

new_configs = [[id, configs[id-1]] for id in valid_ids]

with open("collineation13_valid.txt","w") as output_file:
    for config in new_configs:
        c = Configuration(config[1])
        output_file.write("CONFIGURATION #{0}\n".format(config[0]))
        print "Configuration #{0}".format(config[0])
        result = get_collineation_count(c)
        output_file.write("Collineation count: {0}\n".format(result[0]))
        print "Collineation count: ", result[0]
        for dict in result[1]:
            json.dump(dict, output_file)
            output_file.write("\n")
        print result[1]
        output_file.write("\n\n\n")