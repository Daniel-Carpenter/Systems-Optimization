```python
"""
@author: Daniel Carpenter
@date: 2021-12-15
Systems Optimization 
Final Exam
"""

# Import Gurobi
from gurobipy import *

# Import excel reading package
import openpyxl as opxl

# Create the model
m = Model('Knapsack - Packing for Vacation')
m.setParam(GRB.Param.OutputFlag, 0)

```


```python
"""
=== Problem 1: Knapsack ===
"""
```




    '\n=== Problem 1: Knapsack ===\n'




```python
# Create print function for Knapsack
def printOptimalSolution(model, isPacked, weight, value, Items, Bags):
    if model.status == GRB.Status.OPTIMAL:
        print('Optimizing your vacation: maximize value of packed items while not packing too much')
        
        # Print the optimal intrinsic value
        print("\n*Optimal value of packed items: " 
              + "{:,.4f}".format(model.objVal) + " total intrinsic value")
        
        for bag in Bags:
            
            print('\n\n======== ' + bag + " ========")
        
            # GEt the total weight of the bag
            totalWeight = sum(weight[item] * isPacked[bag, item].x 
                              for item in Items)
            
            # print the total amount packed in lbs
            print('\nTotal Weight of bag: ' + str(totalWeight) + ' lbs.')
            
            # Print the items packed with weight and value
            print("\nItems that you should pack in " + bag + ":")
            print("Item | isPacked \t| lbs. \t| Intrinsic Value")
            for item in Items:
                if isPacked[bag, item].x > 0.5:
                    print(str(item) + ": " 
                          + "\t"    + str(isPacked[bag, item].x)
                          + "\t |\t" + str(  weight[item])
                          + "\t |\t" + str(   value[item]))
        
            # Print the items NOT packed with weight and value
            print("\nItems that you should NOT pack in " + bag + ":")
            print("Item | isPacked \t| lbs. \t| Intrinsic Value")
            for item in Items:
                if isPacked[bag, item].x < 0.5:
                    print(str(item) + ": " 
                          + "\t "    + str(isPacked[bag, item].x)
                          + "\t|\t" + str(  weight[item])
                          + "\t|\t" + str(   value[item]))
    
```


```python
"""
=== Problem 1: Knapsack ===
PART I:
    Imagine that you are planning your next vacations.
    For your trip, first you want to determine which items to pack. 
    To take this decision, you make a list of 30 items from which you want to 
    pick the ones to be packed. For each of these 30 items, you know 
    its weight (in pounds) and its associated intrinsic value 
    (the more you want to take the item, the higher its “value”)
"""

# SETS =======================================================================

# The item and its number that you are considering packing
Items = []
Bags  = ['Bag 1']

# PARAMETERS =================================================================

## weight (in pounds) of each item that you are considering packing
weight = {}

## Intrinsic value of each item that you are considering packing
value = {}

## Read in the values of the Items, weight, and value in the 'Data.xlxs' file
xlFileName  = 'Data'
xlSheetName = 'Data'

xlFile = opxl.load_workbook(xlFileName + ".xlsx")

### First Row to read in minus 1
row = 5 - 1

## Loop through each row and col and insert data into sets and parameters
while xlFile[xlSheetName].cell(row = row + 1, column = 2).value:
    
    #### Read in item name
    newItem = xlFile[xlSheetName].cell(row = row + 1, column = 2).value
    Items.append(newItem)
    
    #### Read in weight col
    weight[newItem] = xlFile[xlSheetName].cell(row = row + 1, column = 3).value
    
    #### read in value col
    value[newItem] = xlFile[xlSheetName].cell(row = row + 1, column = 4).value
    
    #### Increment row
    row += 1


## Capacity of one bag = 15 lbs
bagCapacities = {'Bag 1':15}

# DESCISION VARIABLES ========================================================
isPacked = m.addVars(Bags, Items, vtype = GRB.BINARY)


# OPTIMIZATION ===============================================================

## Add the new constraint for two bags capacity
m.addConstrs(quicksum(weight[item] * isPacked[bag, item] for item in Items) 
                     <= bagCapacities[bag] for bag in Bags)

## Maximize the intrinsic value of the packed items for each bag
objFun = quicksum(quicksum(value[item] * isPacked[bag, item] 
                           for item in Items) 
                  for bag in Bags)

## Set objective, update the model, and Optimize
m.setObjective(objFun, GRB.MAXIMIZE)
m.update()
m.optimize()


# OUTPUT =====================================================================
            
# Print the solution to the console
print('\nPART I: ONLY ONE BAG')
printOptimalSolution(m, isPacked, weight, value, Items, Bags)
            
```

    
    PART I: ONLY ONE BAG
    Optimizing your vacation: maximize value of packed items while not packing too much
    
    *Optimal value of packed items: 34.0000 total intrinsic value
    
    
    ======== Bag 1 ========
    
    Total Weight of bag: 13.0 lbs.
    
    Items that you should pack in Bag 1:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 10: 	1.0	 |	3	 |	9
    Item 13: 	1.0	 |	3	 |	8
    Item 25: 	1.0	 |	3	 |	7
    Item 28: 	1.0	 |	4	 |	10
    
    Items that you should NOT pack in Bag 1:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	3
    Item 2: 	 0.0	|	5	|	2
    Item 3: 	 0.0	|	5	|	5
    Item 4: 	 0.0	|	9	|	4
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 0.0	|	4	|	4
    Item 7: 	 0.0	|	7	|	4
    Item 8: 	 0.0	|	7	|	9
    Item 9: 	 0.0	|	6	|	7
    Item 11: 	 0.0	|	7	|	8
    Item 12: 	 0.0	|	8	|	9
    Item 14: 	 0.0	|	8	|	3
    Item 15: 	 0.0	|	4	|	6
    Item 16: 	 0.0	|	3	|	5
    Item 17: 	 0.0	|	7	|	7
    Item 18: 	 0.0	|	9	|	8
    Item 19: 	 0.0	|	6	|	2
    Item 20: 	 0.0	|	7	|	2
    Item 21: 	 0.0	|	6	|	7
    Item 22: 	 0.0	|	8	|	2
    Item 23: 	 0.0	|	7	|	5
    Item 24: 	 0.0	|	9	|	3
    Item 26: 	 0.0	|	4	|	4
    Item 27: 	 0.0	|	5	|	7
    Item 29: 	 0.0	|	3	|	4
    Item 30: 	 0.0	|	8	|	6
    


```python
"""
=== Problem 1: Knapsack ===
PART II:
    Now, assume that for your trip you can use two bags. 
    The first  bag has a maximum capacity of 15 pounds and 
    the second one has a maximum capacity of 50 pounds.
"""

# SETS =======================================================================

## New SET defining the bags
Bags.append('Bag 2')

## Second Bag Capacity = 50 lbs
bagCapacities = {'Bag 1':15, 'Bag 2':50}


# DESCISION VARIABLES ========================================================
isPacked = m.addVars(Bags, Items, vtype = GRB.BINARY)


# OPTIMIZATION ===============================================================

## Add the new constraint for two bags capacity
m.addConstrs(quicksum(weight[item] * isPacked[bag, item] for item in Items) 
                     <= bagCapacities[bag] for bag in Bags)

## C2: The item cannot be packed in multiple bags
PACKED = 1

### The sum of the binary var `item` (over all bags '*') cannot exceed a count of 1
for item in Items:
        m.addConstr(isPacked.sum('*', item) <= PACKED)

## Maximize the intrinsic value of the packed items for each bag
objFun = quicksum(quicksum(value[item] * isPacked[bag, item] 
                           for item in Items) 
                  for bag in Bags)

## Set objective, update the model, and Optimize
m.setObjective(objFun, GRB.MAXIMIZE)
m.update()
m.optimize()

print('\n\nPART II: MULTIPLE BAGS')
printOptimalSolution(m, isPacked, weight, value, Items, Bags)

```

    
    
    PART II: MULTIPLE BAGS
    Optimizing your vacation: maximize value of packed items while not packing too much
    
    *Optimal value of packed items: 98.0000 total intrinsic value
    
    
    ======== Bag 1 ========
    
    Total Weight of bag: 15.0 lbs.
    
    Items that you should pack in Bag 1:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 9: 	1.0	 |	6	 |	7
    Item 26: 	1.0	 |	4	 |	4
    Item 27: 	1.0	 |	5	 |	7
    
    Items that you should NOT pack in Bag 1:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	3
    Item 2: 	 0.0	|	5	|	2
    Item 3: 	 -0.0	|	5	|	5
    Item 4: 	 0.0	|	9	|	4
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 -0.0	|	4	|	4
    Item 7: 	 0.0	|	7	|	4
    Item 8: 	 -0.0	|	7	|	9
    Item 10: 	 -0.0	|	3	|	9
    Item 11: 	 0.0	|	7	|	8
    Item 12: 	 -0.0	|	8	|	9
    Item 13: 	 -0.0	|	3	|	8
    Item 14: 	 0.0	|	8	|	3
    Item 15: 	 -0.0	|	4	|	6
    Item 16: 	 -0.0	|	3	|	5
    Item 17: 	 -0.0	|	7	|	7
    Item 18: 	 0.0	|	9	|	8
    Item 19: 	 0.0	|	6	|	2
    Item 20: 	 0.0	|	7	|	2
    Item 21: 	 -0.0	|	6	|	7
    Item 22: 	 0.0	|	8	|	2
    Item 23: 	 0.0	|	7	|	5
    Item 24: 	 0.0	|	9	|	3
    Item 25: 	 0.0	|	3	|	7
    Item 28: 	 0.0	|	4	|	10
    Item 29: 	 -0.0	|	3	|	4
    Item 30: 	 0.0	|	8	|	6
    
    
    ======== Bag 2 ========
    
    Total Weight of bag: 50.0 lbs.
    
    Items that you should pack in Bag 2:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 8: 	1.0	 |	7	 |	9
    Item 10: 	1.0	 |	3	 |	9
    Item 11: 	1.0	 |	7	 |	8
    Item 13: 	1.0	 |	3	 |	8
    Item 15: 	1.0	 |	4	 |	6
    Item 16: 	1.0	 |	3	 |	5
    Item 17: 	1.0	 |	7	 |	7
    Item 21: 	1.0	 |	6	 |	7
    Item 25: 	1.0	 |	3	 |	7
    Item 28: 	1.0	 |	4	 |	10
    Item 29: 	1.0	 |	3	 |	4
    
    Items that you should NOT pack in Bag 2:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	3
    Item 2: 	 0.0	|	5	|	2
    Item 3: 	 0.0	|	5	|	5
    Item 4: 	 0.0	|	9	|	4
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 0.0	|	4	|	4
    Item 7: 	 0.0	|	7	|	4
    Item 9: 	 -0.0	|	6	|	7
    Item 12: 	 0.0	|	8	|	9
    Item 14: 	 0.0	|	8	|	3
    Item 18: 	 0.0	|	9	|	8
    Item 19: 	 0.0	|	6	|	2
    Item 20: 	 0.0	|	7	|	2
    Item 22: 	 0.0	|	8	|	2
    Item 23: 	 0.0	|	7	|	5
    Item 24: 	 0.0	|	9	|	3
    Item 26: 	 -0.0	|	4	|	4
    Item 27: 	 0.0	|	5	|	7
    Item 30: 	 0.0	|	8	|	6
    


```python
"""
=== Problem 2: Minimizing Travel Metrics ===
"""
```




    '\n=== Problem 2: Minimizing Travel Metrics ===\n'




```python
# Function to resuse for problem 2 and minimize travel measure
def getMinRoute(POS_NAME, POS, OBJ_MAT, SUPPORT_MAT, objMeasureName, suportMeasureName, minHours):
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
    supportCost = {}
    
    ### Read distance and position lists to create set of node (Nodes), arcs (Arcs), and
    ### Distance between nodes (objCost)
    for i, pos_i in enumerate(POS):
        Nodes.append(i)
        for j, pos_j in enumerate(POS):
            if j!= i:
                Arcs.append((i, j))
                objCost[i, j] = OBJ_MAT[i][j]
                supportCost[i, j]   = SUPPORT_MAT[i][j]
                
    ### COunt of nodes
    numNodes = len(Nodes)
    
    # OPTIMIZATION ================================================================
    
    ## Create the model
    m = Model('Traveling Salesman')
    
    ## Create variables and the coefficients of the objective function
    isVisited    = m.addVars(Arcs,  obj = objCost, name = 'isVisited', vtype = GRB.BINARY)
    orderOfVisit = m.addVars(Nodes, obj = 0, name = 'orderOfVisit')
    m.update()
    
    ## Constraints ---------------------------------------------------------------
    
    ### Only can depart from a single node
    m.addConstrs(
        (isVisited.sum('*', j) == 1 for j in Nodes),
        'departureNode')
    
    ### Only can arrive at a single node
    m.addConstrs(
        (isVisited.sum(i, '*') == 1 for i in Nodes),
        'arrivalNode')
    
    ### Time labels
    m.addConstrs(
        (numNodes*(1 - isVisited[i, j]) >= orderOfVisit[i]-orderOfVisit[j]+1 for (i,j) in Arcs if (j!=0)),
        'timeLabels')
    
    ### Total number of Hours traveled must be less than the minHours that you define
    m.addConstr(sum(supportCost[node] * isVisited[node] for node in isVisited) <= minHours)
    
    ## Optimize the Minimum Distance Traveled
    m.update()
    m.modelSense = GRB.MINIMIZE
    m.setParam('OutputFlag', 0)
    m.optimize()
    
    ## Get the total cost
    totalSupportCost = sum(supportCost[node] * isVisited[node].x for node in isVisited) 
    
    # Print the solution
    if m.status == GRB.Status.OPTIMAL:
        print('\n======== Optimized ' + objMeasureName + ' & Associated '  + suportMeasureName + ' ========')
        solution_OF = m.objVal
        solution_x  = m.getAttr('x', isVisited) 
        solution_u  = m.getAttr('x', orderOfVisit)
        print('Total Optimized ' + objMeasureName + ': \t%g' % solution_OF)
        print('Total Associated '  + suportMeasureName + ': \t%g' % totalSupportCost)
        print('\nOptimal Path:')
        for i, j in Arcs:
            if solution_x[i,j] > 0:
                print('%s\t->\t%s' % (POS_NAME[i], POS_NAME[j]))
                
```


```python
print(
"""

=== Problem 2: Minimizing Travel Metrics ===
PART I: Minimize the total Travel Time using Airplanes 
"""
)

## Input Sets
AIRPLANE_POS_NAME = ['Airplane 1', 'Airplane 2', 'Airplane 3', 'Airplane 4', 'Airplane 5', 'Airplane 6', 'Airplane 7']
AIRPLANE_POS = [['Airplane 1', 'Airplane 1'], 
                ['Airplane 2', 'Airplane 2'], 
                ['Airplane 3', 'Airplane 3'], 
                ['Airplane 4', 'Airplane 4'], 
                ['Airplane 5', 'Airplane 5'], 
                ['Airplane 6', 'Airplane 6'], 
                ['Airplane 7', 'Airplane 7']]

## Airplane Distance Matrix
AIRPLANE_DIST =    [[0, 0.9, 1.1, 1, 2.8, 1.8, 2.5], 
                    [0.8, 0, 1.7, 1.8, 3.1, 1.8, 2.4], 
                    [1.1, 1.6, 0, 1.4, 1.7, 1.7, 1.7], 
                    [0.9, 1.9, 1.3, 0, 2.7, 2.8, 2.9], 
                    [2.8, 3, 1.6, 2.8, 0, 2, 1.3], 
                    [1.9, 1.7, 1.8, 2.8, 2.2, 0, 1.2], 
                    [2.6, 2.5, 1.7, 2.9, 1.3, 1.2, 0]]


## Airplane Cost Matrix
AIRPLANE_COST =    [[0, 85, 160, 99, 280, 194, 302], 
                    [123, 0, 223, 232, 385, 234, 312], 
                    [162, 240, 0, 202, 175, 213, 209], 
                    [150, 248, 197, 0, 291, 295, 349], 
                    [344, 327, 193, 314, 0, 258, 132], 
                    [202, 176, 201, 281, 246, 0, 181], 
                    [326, 271, 230, 318, 130, 174, 0]]



## Call Function defined above
getMinRoute(AIRPLANE_POS_NAME, AIRPLANE_POS, 
            OBJ_MAT=AIRPLANE_DIST,    SUPPORT_MAT=AIRPLANE_COST, 
            objMeasureName = 'Time (Hours)', suportMeasureName = 'Cost (USD)',
            minHours=GRB.INFINITY) # no restriction on min hours

```

    
    
    === Problem 2: Minimizing Travel Metrics ===
    PART I: Minimize the total Travel Time using Airplanes 
    
    
    ======== Optimized Time (Hours) & Associated Cost (USD) ========
    Total Optimized Time (Hours): 	9
    Total Associated Cost (USD): 	1076
    
    Optimal Path:
    Airplane 1	->	Airplane 4
    Airplane 2	->	Airplane 1
    Airplane 3	->	Airplane 5
    Airplane 4	->	Airplane 3
    Airplane 5	->	Airplane 7
    Airplane 6	->	Airplane 2
    Airplane 7	->	Airplane 6
    


```python
print(
"""

=== Problem 2: Minimizing Travel Metrics ===
PART II: Minimize the total Travel Cost using Buses
"""
)

## Input Sets
BUS_POS_NAME = ['Bus 1', 'Bus 2', 'Bus 3', 'Bus 4', 'Bus 5', 'Bus 6', 'Bus 7']
BUS_POS = [['Bus 1', 'Bus 1'], 
            ['Bus 2', 'Bus 2'], 
            ['Bus 3', 'Bus 3'], 
            ['Bus 4', 'Bus 4'], 
            ['Bus 5', 'Bus 5'], 
            ['Bus 6', 'Bus 6'], 
            ['Bus 7', 'Bus 7']]

## Bus Distance Matrix
BUS_DIST = [[0, 4.7, 5.4, 4.5, 10.1, 7, 9.4], 
            [4.5, 0, 7.1, 6.7, 10.8, 6.9, 10.2], 
            [3.5, 6.1, 0, 5.1, 6.4, 7.4, 7.6], 
            [2.8, 6.6, 5.9, 0, 10.7, 10.7, 10.7], 
            [9.3, 11.4, 7.6, 10.5, 0, 7.4, 5], 
            [6.9, 7, 7.6, 9.5, 9, 0, 5.4], 
            [8.9, 9.3, 6.7, 11.3, 6.2, 4.2, 0]]


## Bus Cost Matrix
BUS_COST = [[0, 21, 21, 25, 38, 27, 25], 
            [13, 0, 30, 32, 31, 17, 25], 
            [24, 16, 0, 12, 19, 32, 21], 
            [25, 24, 19, 0, 21, 36, 38], 
            [22, 42, 16, 39, 0, 17, 11], 
            [23, 27, 16, 34, 25, 0, 13], 
            [19, 19, 25, 37, 28, 19, 0]]


## Call Function
getMinRoute(BUS_POS_NAME, BUS_POS, 
            OBJ_MAT=BUS_COST,       SUPPORT_MAT=BUS_DIST, 
            objMeasureName = 'Cost (USD)', suportMeasureName = 'Time (Hours)',
            minHours=GRB.INFINITY)

```

    
    
    === Problem 2: Minimizing Travel Metrics ===
    PART II: Minimize the total Travel Cost using Buses
    
    
    ======== Optimized Cost (USD) & Associated Time (Hours) ========
    Total Optimized Cost (USD): 	116
    Total Associated Time (Hours): 	47.8
    
    Optimal Path:
    Bus 1	->	Bus 3
    Bus 2	->	Bus 1
    Bus 3	->	Bus 4
    Bus 4	->	Bus 5
    Bus 5	->	Bus 6
    Bus 6	->	Bus 7
    Bus 7	->	Bus 2
    


```python
print(
"""

=== Problem 2: Minimizing Travel Metrics ===
PART III: 
    Minimize the total Travel Cost with Bus and Airports
    s.t. total travel time <= 20 hours 
"""
)
    
import numpy as np
    
## Combine the bus and airplane position names
COMB_POS_NAME = np.hstack((BUS_POS_NAME, AIRPLANE_POS_NAME))

## Combine the bus and airplane positions
COMB_POS = np.vstack((BUS_POS, AIRPLANE_POS))

# * Assume that it takes the same amount of distance from a bus station 1 
# to bus station 2 as it takes to get from bus station 1 to airplane 2, etc.

# Append the Bus and Airplane distance matrices by row
COMB_DIST = np.vstack((BUS_DIST, AIRPLANE_DIST))

# Duplicate the data - create a copy and append by col
COMB_DIST = np.hstack((COMB_DIST, COMB_DIST))

# Append the Bus and Airplane cost matrices by row
COMB_COST = np.vstack((BUS_COST, AIRPLANE_COST))

# Duplicate the data - create a copy and append by col
COMB_COST = np.hstack((COMB_COST, COMB_COST))

# CAll function which get the minimum cost route using buses or airplanes, s.t. you travel less than 20 hours total
getMinRoute(COMB_POS_NAME, COMB_POS, 
            OBJ_MAT=COMB_COST,       SUPPORT_MAT=COMB_DIST, 
            objMeasureName = 'Cost (USD)', suportMeasureName = 'Time (Hours)',
            minHours = 20)

```

    
    
    === Problem 2: Minimizing Travel Metrics ===
    PART III: 
        Minimize the total Travel Cost with Bus and Airports
        s.t. total travel time <= 20 hours 
    
    
    ======== Optimized Cost (USD) & Associated Time (Hours) ========
    Total Optimized Cost (USD): 	643
    Total Associated Time (Hours): 	19.8
    
    Optimal Path:
    Bus 1	->	Airplane 1
    Bus 2	->	Bus 6
    Bus 3	->	Airplane 4
    Bus 4	->	Bus 1
    Bus 5	->	Airplane 5
    Bus 6	->	Airplane 6
    Bus 7	->	Airplane 7
    Airplane 1	->	Airplane 2
    Airplane 2	->	Bus 2
    Airplane 3	->	Bus 3
    Airplane 4	->	Bus 4
    Airplane 5	->	Airplane 3
    Airplane 6	->	Bus 7
    Airplane 7	->	Bus 5
    


```python
"""
=== Problem 3: Determine supply / Production capcity and distribution ===
"""
```




    '\n=== Problem 3: Determine supply / Production capcity and distribution ===\n'




```python
"""
Problem 3:
Production capcity and distribution

Goal is to determine the supply of each plant
In doing so, you must minimize the cost given the demand of the city
s.t. 
    flow of goods is <= the upper bound of the path
    flow of goods is >= the lower bound of the path
"""

# CREATE MODEL ================================================================
m = Model(name = 'Production capcity and distribution')


# SETS ========================================================================
Plants = ['Plant 1', 'Plant 2']
Cities = ['City 1', 'City 2', 'City 3']


# PARAMETERS ==================================================================

## The demand of the city
demand = {'City 1': 25, 
          'City 2': 15, 
          'City 3': 40}

## Define the cost, lowerBound, and upperBound:
### cost: the cost of the path from a plant ∈ Plants to a city ∈ Cities
### lowerBound: the lower bound of each path from a plant ∈ Plants to a city ∈ Cities
### upperBound: the upper bound (capacity limit) of each path from a plant ∈ Plants to a city ∈ Cities
Arcs, cost, lowerBound, upperBound = multidict({
        ('Plant 1', 'City 1'): [18, 0, 15],
        ('Plant 1', 'City 2'): [17, 0, 30],
        ('Plant 1', 'City 3'): [21, 0, 20],
        ('Plant 2', 'City 1'): [13, 0, 20],
        ('Plant 2', 'City 2'): [15, 0, 25],
        ('Plant 2', 'City 3'): [10, 0, 30],
    })


# DECISION VARIABLES AND OBKJECTIVE FUNCTION ==================================

## The flow of goods from a plant ∈ Plants to a city ∈ Cities
flow = m.addVars(Arcs, name = 'flow',
                 
## Objective = cost, minimized by default
                 obj = cost)


# CONSTRAINTS =================================================================

# Flow from a plant ∈ Plants to a city ∈ Cities must be less than the demand in a city ∈ Cities 
m.addConstrs((flow.sum('*', city) == demand[city] 
             for city in Cities), 'demand')

# Flow from a plant ∈ Plants to a city ∈ Cities must be greater than the lowerBound 
m.addConstrs((flow[plant, city] >= lowerBound[plant, city] 
             for plant, city in Arcs),'lowerFlow')

# Flow from a plant ∈ Plants to a city ∈ Cities must be less than the upperBound 
m.addConstrs((flow[plant, city] <= upperBound[plant, city] 
             for plant, city in Arcs), 'upperFlow')


# OPTIMIZE AND PRINT ==========================================================

## Update the model
m.update()

## Optimize the model
m.modelSense = GRB.MINIMIZE
m.setParam('OutputFlag', 0)
m.optimize()

## Get the supply of each plant
plantSupply = {'Plant 1':0,
               'Plant 2':0}

for plant in Plants:
    for city in Cities:
        plantSupply[plant] += flow[plant, city].x

## Print the output
if m.status == GRB.Status.OPTIMAL:
    print('\n========= OPTIMIZED MODEL =========')
    
    print('\nOptimized cost: %g' % m.objVal + ' (in USD)')
    
    print('\nOptimal Supply of the Plants')
    for plant in Plants: print(plant + ':\t' + str(plantSupply[plant]))

    print('\nDecision Variables (flow from plant to city): ')
    for plant, city in Arcs:
        print('%s\t->\t%s' % (plant, city) + ':\t' + str(flow[plant, city].x))
        
```

    
    ========= OPTIMIZED MODEL =========
    
    Optimized cost: 1085 (in USD)
    
    Optimal Supply of the Plants
    Plant 1:	15.0
    Plant 2:	65.0
    
    Decision Variables (flow from plant to city): 
    Plant 1	->	City 1:	5.0
    Plant 1	->	City 2:	0.0
    Plant 1	->	City 3:	10.0
    Plant 2	->	City 1:	20.0
    Plant 2	->	City 2:	15.0
    Plant 2	->	City 3:	30.0
    
