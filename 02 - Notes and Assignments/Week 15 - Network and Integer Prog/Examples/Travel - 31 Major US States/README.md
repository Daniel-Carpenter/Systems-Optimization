# Traveling Salesman with `Gurobi` - Visit 31 major Cities in US and minimize distance traveled

## Conceptual Overview:
* Goal is to go on a trip to 31 major US cities and minimize the distance traveled
* We will start and finish in Alabama
 
--- 
 
## Setup
<img src ="Images\setup.png">

--- 

## Optimal Solution (Visually)
<img src ="Images\opt.png">


<br>

## Code
```python
"""
Traveling Salesmen (Minimize distance traveled through sources and destinations)
"""

# Import Gurobi
from gurobipy import *

```


```python
# Function to minimize travel measure
def getMinRoute(POS_NAME, POS, OBJ_MAT, objMeasureName, minHours):
    # Create model for optimization
    m = Model('Traveling Salesman')
    
    ## Create Empty Sets and Paremters to append in following block 
    
    ### Nodes
    Nodes = tuplelist([])
    
    ### Arcs
    Arcs = tuplelist([])
    
    ### Distance
    objCost = {}
    
    ### Actual Cost
    #supportCost = {}
    
    ### Read distance and position lists to create set of node (Nodes), arcs (Arcs), and
    ### Distance between nodes (objCost)
    for i, pos_i in enumerate(POS):
        Nodes.append(i)
        for j, pos_j in enumerate(POS):
            if j!= i:
                Arcs.append((i, j))
                objCost[i, j] = OBJ_MAT[i][j]
                #supportCost[i, j]   = SUPPORT_MAT[i][j]
                
    ### COunt of nodes
    numNodes = len(Nodes)
    
    # OPTIMIZATION ================================================================
    
    ## Create the model
    m = Model('Traveling Salesman')
    
    ## Create variables and the coefficients of the objective function
    isVisited    = m.addVars(Arcs,  obj = objCost, name = 'isVisited', vtype = GRB.BINARY)
    m.update()
    orderOfVisit = m.addVars(Nodes, obj = 0, name = 'orderOfVisit')
    m.update()
    
    ## Constraints ---------------------------------------------------------------
    
    ### Only can depart from a single node
    m.addConstrs(
        (isVisited.sum('*', j) == 1 for j in Nodes),
        'departureNode')
    m.update()
    
    ### Only can arrive at a single node
    m.addConstrs(
        (isVisited.sum(i, '*') == 1 for i in Nodes),
        'arrivalNode')
    m.update()
    
    ### Time labels?
    m.addConstrs(
        (numNodes*(1 - isVisited[i, j]) >= orderOfVisit[i]-orderOfVisit[j]+1 for (i,j) in Arcs if (j!=0)),
        'timeLabels')
    m.update()
    
    ### Total number of Hours traveled must be less than the minHours that you define
    #m.addConstr(sum(supportCost[node] * isVisited[node] for node in isVisited) <= minHours)
    
    ## Optimize the Minimum Distance Traveled
    m.modelSense = GRB.MINIMIZE
    m.setParam('OutputFlag', 0)
    m.update()
    m.optimize()
    
    ## Get the total cost
    #totalSupportCost = sum(supportCost[node] * isVisited[node].x for node in isVisited) 
    
    # Print the solution
    if m.status == GRB.Status.OPTIMAL:
        print('\n======== Optimized ' + objMeasureName + ' ========')
        solution_OF = m.objVal
        solution_x  = m.getAttr('x', isVisited) 
        solution_u  = m.getAttr('x', orderOfVisit)
        print('Total Optimized ' + objMeasureName + ': \t%g' % solution_OF)
        #print('Total Associated '  + suportMeasureName + ': \t%g' % totalSupportCost)
        print('\nOptimal Path:')
        for i, j in Arcs:
            if solution_x[i,j] > 0:
                print('%s\t->\t%s' % (POS_NAME[i], POS_NAME[j]))
```


```python
print(
"""
Minimize the total Distance for a 50 states trip in the US
"""
)


## Name of the positions
POS_NAME = ['Montgomery, Alabama', 'Juneau, Alaska', 'Phoenix, Arizona', 'Little Rock, Arkansas', 'Sacramento, California', 'Denver, Colorado', 'Hartford, Connecticut', 'Dover, Delaware', 'Tallahassee, Florida', 'Atlanta, Georgia', 'Honolulu, Hawaii', 'Boise, Idaho', 'Springfield, Illinois', 'Indianapolis, Indiana', 'Des Moines, Iowa', 'Topeka, Kansas', 'Frankfort, Kentucky', 'Baton Rouge, Louisiana', 'Augusta, Maine', 'Annapolis, Maryland', 'Boston, Massachusetts', 'Lansing, Michigan', 'Saint Paul, Minnesota', 'Jackson, Mississippi', 'Jefferson City, Missouri', 'Helena, Montana', 'Lincoln, Nebraska', 'Carson City, Nevada', 'Concord, New Hampshire', 'Trenton, New Jersey', 'Santa Fe, New Mexico', 'Albany, New York', 'Raleigh, North Carolina', 'Bismarck, North Dakota', 'Columbus, Ohio', 'Oklahoma City, Oklahoma', 'Salem, Oregon', 'Harrisburg, Pennsylvania', 'Providence, Rhode Island', 'Columbia, South Carolina', 'Pierre, South Dakota', 'Nashville, Tennessee', 'Austin, Texas', 'Salt Lake City, Utah', 'Montpelier, Vermont', 'Richmond, Virginia', 'Olympia, Washington', 'Charleston, West Virginia', 'Madison, Wisconsin', 'Cheyenne, Wyoming']

# Positions
POS =  [[-5961.51, 2236.04], 
        [-9287.82, 4028.41], 
        [-7743.82, 2311.14], 
        [-6379.68, 2400.11], 
        [-8392.98, 2664.03], 
        [-7253.95, 2745.8], 
        [-5021.67, 2885.92], 
        [-5218.57, 2705.92], 
        [-5822.88, 2104.09], 
        [-5830.98, 2332.67], 
        [-10905.11, 1472.36], 
        [-8031.52, 3013.52], 
        [-6194.45, 2748.85], 
        [-5952.43, 2749.38], 
        [-6468.8, 2873.75], 
        [-6611.76, 2697.49], 
        [-5863.67, 2639.27], 
        [-6297.39, 2104.52], 
        [-4820.48, 3062.56], 
        [-5285.9, 2692.86], 
        [-4907.69, 2918.27], 
        [-5841.81, 2952.7], 
        [-6432.39, 3105.85], 
        [-6232.91, 2233.17], 
        [-6369.88, 2665.22], 
        [-7740.58, 3219.57], 
        [-6679.85, 2819.78], 
        [-8274.47, 2705.85], 
        [-4943.73, 2986.32], 
        [-5165.33, 2779.15], 
        [-7321.69, 2464.45]]


# Distances between all positions
DIST = [[0, 3778, 1784, 449, 2469, 1389, 1143, 879, 191, 162, 5002, 2211, 563, 513, 815, 797, 415, 361, 1409, 816, 1255, 727, 989, 271, 592, 2033, 926, 2360, 1264, 964, 1379, 1119, 578, 1515, 572, 807, 2684, 849, 1217, 380, 1277, 265, 806, 1862, 1254, 707, 2726, 524, 771, 1416], 
        [3778, 0, 2309, 3333, 1632, 2405, 4416, 4279, 3963, 3850, 3025, 1615, 3348, 3572, 3046, 2989, 3695, 3556, 4571, 4219, 4519, 3610, 3001, 3543, 3221, 1746, 2874, 1666, 4467, 4308, 2512, 4327, 4157, 2415, 3772, 2997, 1214, 4167, 4499, 4053, 2544, 3629, 3189, 1973, 4382, 4189, 1113, 3899, 3285, 2365], 
        [1784, 2309, 0, 1367, 739, 655, 2782, 2556, 1932, 1913, 3271, 759, 1610, 1844, 1394, 1196, 1909, 1461, 3018, 2487, 2900, 2007, 1533, 1513, 1419, 908, 1179, 661, 2880, 2621, 449, 2721, 2316, 1318, 2059, 1014, 1097, 2477, 2868, 2145, 1108, 1757, 1014, 505, 2830, 2408, 1200, 2130, 1703, 732], 
        [449, 3333, 1367, 0, 2031, 940, 1442, 1201, 631, 553, 4620, 1762, 395, 552, 482, 377, 569, 307, 1694, 1132, 1561, 771, 708, 222, 265, 1589, 516, 1919, 1551, 1272, 944, 1394, 949, 1134, 739, 363, 2235, 1134, 1525, 782, 865, 396, 485, 1414, 1516, 1046, 2276, 780, 611, 969], 
        [2469, 1632, 739, 2031, 0, 1142, 3379, 3175, 2630, 2583, 2780, 503, 2200, 2442, 1936, 1782, 2529, 2169, 3595, 3107, 3495, 2567, 2010, 2203, 2023, 857, 1720, 126, 3464, 3230, 1090, 3307, 2966, 1596, 2660, 1667, 454, 3083, 3465, 2811, 1514, 2402, 1736, 679, 3402, 3042, 595, 2753, 2239, 1165], 
        [1389, 2405, 655, 940, 1142, 0, 2237, 2036, 1568, 1482, 3867, 822, 1060, 1302, 796, 644, 1394, 1152, 2454, 1969, 2353, 1427, 897, 1143, 888, 679, 579, 1021, 2323, 2089, 289, 2165, 1841, 691, 1519, 593, 1297, 1943, 2323, 1702, 453, 1282, 824, 482, 2261, 1908, 1336, 1616, 1102, 98], 
        [1143, 4416, 2782, 1442, 3379, 2237, 0, 267, 1119, 980, 6051, 3013, 1181, 941, 1447, 1601, 877, 1496, 268, 327, 118, 823, 1428, 1376, 1366, 2739, 1659, 3258, 127, 179, 2338, 98, 584, 2002, 724, 1772, 3486, 308, 87, 788, 1920, 1049, 1906, 2711, 173, 441, 3489, 662, 1158, 2220], 
        [879, 4279, 2556, 1201, 3175, 2036, 267, 0, 853, 717, 5819, 2830, 977, 735, 1261, 1393, 649, 1235, 534, 69, 376, 670, 1278, 1119, 1152, 2574, 1466, 3056, 393, 91, 2117, 270, 318, 1868, 519, 1542, 3306, 121, 338, 522, 1752, 805, 1654, 2515, 408, 174, 3318, 426, 995, 2027], 
        [191, 3963, 1932, 631, 2630, 1568, 1119, 853, 0, 229, 5121, 2389, 744, 658, 1005, 987, 537, 475, 1387, 797, 1225, 849, 1173, 430, 784, 2219, 1117, 2524, 1245, 942, 1542, 1112, 535, 1706, 663, 980, 2859, 849, 1186, 332, 1469, 431, 931, 2037, 1251, 679, 2904, 575, 941, 1599], 
        [162, 3850, 1913, 553, 2583, 1482, 980, 717, 229, 0, 5147, 2303, 553, 434, 836, 862, 308, 519, 1247, 653, 1093, 620, 980, 414, 633, 2106, 979, 2472, 1102, 802, 1497, 957, 421, 1538, 439, 916, 2779, 687, 1055, 232, 1323, 234, 954, 1961, 1093, 545, 2814, 370, 730, 1500], 
        [5002, 3025, 3271, 4620, 2780, 3867, 6051, 5819, 5121, 5147, 0, 3261, 4881, 5115, 4652, 4465, 5175, 4651, 6289, 5750, 6169, 5275, 4762, 4734, 4689, 3615, 4435, 2905, 6151, 5887, 3718, 5992, 5562, 4376, 5328, 4279, 2906, 5745, 6136, 5378, 4280, 5015, 4197, 3447, 6101, 5665, 2998, 5395, 4962, 3912], 
        [2211, 1615, 759, 1762, 503, 822, 3013, 2830, 2389, 2303, 3261, 0, 1856, 2096, 1569, 1455, 2200, 1958, 3211, 2764, 3125, 2191, 1602, 1961, 1698, 357, 1365, 392, 3088, 2876, 897, 2934, 2654, 1127, 2310, 1409, 478, 2730, 3099, 2521, 1100, 2099, 1576, 359, 3017, 2712, 517, 2419, 1856, 808], 
        [563, 3348, 1610, 395, 2200, 1060, 1181, 977, 744, 553, 4881, 1856, 0, 242, 301, 420, 348, 652, 1409, 910, 1298, 407, 429, 517, 194, 1616, 491, 2080, 1273, 1030, 1163, 1114, 810, 990, 460, 621, 2334, 883, 1267, 717, 803, 319, 863, 1538, 1220, 856, 2351, 563, 228, 1051], 
        [513, 3572, 1844, 552, 2442, 1302, 941, 735, 658, 434, 5115, 2096, 242, 0, 531, 661, 141, 731, 1174, 669, 1058, 231, 598, 587, 426, 1849, 731, 2322, 1036, 788, 1399, 877, 589, 1188, 218, 841, 2573, 642, 1027, 534, 1030, 254, 1037, 1780, 988, 620, 2588, 327, 319, 1292], 
        [815, 3046, 1394, 482, 1936, 796, 1447, 1261, 1005, 836, 4652, 1569, 301, 531, 0, 227, 649, 788, 1659, 1197, 1562, 632, 235, 683, 231, 1318, 218, 1813, 1529, 1307, 946, 1373, 1111, 703, 742, 501, 2045, 1161, 1534, 1016, 502, 603, 833, 1264, 1466, 1151, 2057, 858, 310, 773], 
        [797, 2989, 1196, 377, 1782, 644, 1601, 1393, 987, 862, 4465, 1455, 420, 661, 227, 0, 750, 671, 1828, 1326, 1718, 811, 446, 599, 244, 1244, 140, 1663, 1693, 1449, 747, 1534, 1200, 761, 879, 277, 1932, 1303, 1688, 1071, 488, 647, 623, 1126, 1638, 1264, 1959, 972, 517, 646], 
        [415, 3695, 1909, 569, 2529, 1394, 877, 649, 537, 308, 5175, 2200, 348, 141, 649, 750, 0, 689, 1126, 580, 996, 314, 736, 549, 507, 1965, 836, 2412, 983, 712, 1468, 825, 462, 1322, 177, 895, 2678, 570, 962, 393, 1151, 193, 1046, 1876, 947, 514, 2698, 223, 460, 1393], 
        [361, 3556, 1461, 307, 2169, 1152, 1496, 1235, 475, 519, 4651, 1958, 652, 731, 788, 671, 689, 0, 1760, 1170, 1610, 963, 1010, 144, 565, 1824, 811, 2067, 1616, 1318, 1086, 1466, 939, 1433, 865, 562, 2420, 1196, 1573, 740, 1152, 496, 457, 1601, 1599, 1064, 2475, 854, 880, 1198], 
        [1409, 4571, 3018, 1694, 3595, 2454, 268, 534, 1387, 1247, 6289, 3211, 1409, 1174, 1659, 1828, 1126, 1760, 0, 594, 169, 1027, 1612, 1638, 1600, 2924, 1875, 3472, 145, 446, 2572, 300, 852, 2165, 963, 2014, 3681, 566, 207, 1056, 2112, 1304, 2164, 2921, 194, 709, 3676, 918, 1358, 2431], 
        [816, 4219, 2487, 1132, 3107, 1969, 327, 69, 797, 653, 5750, 2764, 910, 669, 1197, 1326, 580, 1170, 594, 0, 440, 614, 1219, 1053, 1084, 2511, 1400, 2989, 451, 148, 2049, 317, 266, 1810, 454, 1473, 3241, 93, 402, 465, 1689, 737, 1587, 2448, 456, 119, 3254, 357, 934, 1961], 
        [1255, 4519, 2900, 1561, 3495, 2353, 118, 376, 1225, 1093, 6169, 3125, 1298, 1058, 1562, 1718, 996, 1610, 169, 440, 0, 935, 1536, 1492, 1484, 2849, 1775, 3373, 77, 293, 2456, 193, 690, 2105, 842, 1890, 3598, 426, 39, 895, 2030, 1167, 2023, 2825, 176, 550, 3599, 780, 1270, 2335], 
        [727, 3610, 2007, 771, 2567, 1427, 823, 670, 849, 620, 5275, 2191, 407, 231, 632, 811, 314, 963, 1027, 614, 935, 0, 610, 819, 601, 1917, 849, 2445, 899, 698, 1558, 744, 631, 1198, 219, 1028, 2663, 557, 909, 650, 1097, 479, 1255, 1894, 834, 607, 2666, 364, 335, 1404], 
        [989, 3001, 1533, 708, 2010, 897, 1428, 1278, 1173, 980, 4762, 1602, 429, 598, 235, 446, 736, 1010, 1612, 1219, 1536, 610, 0, 895, 445, 1313, 378, 1885, 1493, 1309, 1096, 1344, 1183, 594, 778, 723, 2068, 1166, 1513, 1125, 502, 747, 1064, 1331, 1419, 1195, 2064, 914, 287, 851], 
        [271, 3543, 1513, 222, 2203, 1143, 1376, 1119, 430, 414, 4734, 1961, 517, 587, 683, 599, 549, 144, 1638, 1053, 1492, 819, 895, 0, 453, 1802, 737, 2096, 1493, 1199, 1113, 1341, 834, 1354, 726, 551, 2430, 1072, 1455, 644, 1088, 356, 540, 1608, 1472, 952, 2477, 724, 745, 1178], 
        [592, 3221, 1419, 265, 2023, 888, 1366, 1152, 784, 633, 4689, 1698, 194, 426, 231, 244, 507, 565, 1600, 1084, 1484, 601, 445, 453, 0, 1479, 346, 1905, 1462, 1210, 973, 1303, 956, 924, 642, 427, 2176, 1065, 1452, 833, 691, 409, 691, 1370, 1411, 1020, 2201, 730, 366, 889], 
        [2033, 1746, 908, 1589, 857, 679, 2739, 2574, 2219, 2106, 3615, 357, 1616, 1849, 1318, 1244, 1965, 1824, 2924, 2511, 2849, 1917, 1313, 1802, 1479, 0, 1134, 741, 2807, 2613, 864, 2657, 2425, 792, 2057, 1262, 769, 2468, 2825, 2312, 822, 1887, 1499, 404, 2731, 2469, 751, 2176, 1583, 625], 
        [926, 2874, 1179, 516, 1720, 579, 1659, 1466, 1117, 979, 4435, 1365, 491, 731, 218, 140, 836, 811, 1875, 1400, 1775, 849, 378, 737, 346, 1134, 0, 1599, 1744, 1515, 734, 1587, 1294, 621, 947, 373, 1843, 1369, 1746, 1179, 353, 755, 732, 1051, 1682, 1347, 1862, 1053, 528, 562], 
        [2360, 1666, 661, 1919, 126, 1021, 3258, 3056, 2524, 2472, 2905, 392, 2080, 2322, 1813, 1663, 2412, 2067, 3472, 2989, 3373, 2445, 1885, 2096, 1905, 741, 1599, 0, 3343, 3110, 983, 3186, 2851, 1471, 2540, 1556, 458, 2964, 3345, 2699, 1389, 2287, 1640, 554, 3279, 2924, 586, 2635, 2116, 1042], 
        [1264, 4467, 2880, 1551, 3464, 2323, 127, 393, 1245, 1102, 6151, 3088, 1273, 1036, 1529, 1693, 983, 1616, 145, 451, 77, 899, 1493, 1493, 1462, 2807, 1744, 3343, 0, 303, 2435, 159, 711, 2056, 823, 1873, 3559, 421, 97, 914, 1991, 1160, 2020, 2793, 101, 566, 3557, 774, 1232, 2302], 
        [964, 4308, 2621, 1272, 3230, 2089, 179, 91, 942, 802, 5887, 2876, 1030, 788, 1307, 1449, 712, 1318, 446, 148, 293, 698, 1309, 1199, 1210, 2613, 1515, 3110, 303, 0, 2179, 181, 408, 1894, 570, 1608, 3351, 146, 256, 611, 1791, 877, 1731, 2566, 318, 263, 3359, 492, 1030, 2077], 
        [1379, 2512, 449, 944, 1090, 289, 2338, 2117, 1542, 1497, 3718, 897, 1163, 1399, 946, 747, 1468, 1086, 2572, 2049, 2456, 1558, 1096, 1113, 973, 864, 734, 983, 2435, 2179, 0, 2276, 1888, 976, 1614, 583, 1342, 2035, 2424, 1726, 716, 1326, 679, 540, 2383, 1974, 1409, 1691, 1255, 387]]


# Call function to minimize distance
getMinRoute(POS_NAME, POS, 
            OBJ_MAT=DIST, objMeasureName='Raw Distance between Cities - "As the crow flies"', 
            minHours=GRB.INFINITY)
```

    
    Minimize the total Distance for a 50 states trip in the US
    
    Restricted license - for non-production use only - expires 2022-01-13
    
    ======== Optimized Raw Distance between Cities - "As the crow flies" ========
    Total Optimized Raw Distance between Cities - "As the crow flies": 	16533
    
    Optimal Path:
    Montgomery, Alabama	->	Jackson, Mississippi
    Juneau, Alaska	->	Boise, Idaho
    Phoenix, Arizona	->	Carson City, Nevada
    Little Rock, Arkansas	->	Topeka, Kansas
    Sacramento, California	->	Honolulu, Hawaii
    Denver, Colorado	->	Santa Fe, New Mexico
    Hartford, Connecticut	->	Trenton, New Jersey
    Dover, Delaware	->	Annapolis, Maryland
    Tallahassee, Florida	->	Montgomery, Alabama
    Atlanta, Georgia	->	Tallahassee, Florida
    Honolulu, Hawaii	->	Juneau, Alaska
    Boise, Idaho	->	Helena, Montana
    Springfield, Illinois	->	Indianapolis, Indiana
    Indianapolis, Indiana	->	Frankfort, Kentucky
    Des Moines, Iowa	->	Jefferson City, Missouri
    Topeka, Kansas	->	Lincoln, Nebraska
    Frankfort, Kentucky	->	Lansing, Michigan
    Baton Rouge, Louisiana	->	Little Rock, Arkansas
    Augusta, Maine	->	Boston, Massachusetts
    Annapolis, Maryland	->	Atlanta, Georgia
    Boston, Massachusetts	->	Hartford, Connecticut
    Lansing, Michigan	->	Concord, New Hampshire
    Saint Paul, Minnesota	->	Des Moines, Iowa
    Jackson, Mississippi	->	Baton Rouge, Louisiana
    Jefferson City, Missouri	->	Springfield, Illinois
    Helena, Montana	->	Saint Paul, Minnesota
    Lincoln, Nebraska	->	Denver, Colorado
    Carson City, Nevada	->	Sacramento, California
    Concord, New Hampshire	->	Augusta, Maine
    Trenton, New Jersey	->	Dover, Delaware
    Santa Fe, New Mexico	->	Phoenix, Arizona
    
