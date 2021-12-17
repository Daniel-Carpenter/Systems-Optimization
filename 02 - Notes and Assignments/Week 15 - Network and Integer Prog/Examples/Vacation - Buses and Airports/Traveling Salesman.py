"""
Traveling Salesmen (Minimize distance traveled through sources and destinations)
"""

from gurobipy import *


# Function to minimize travel measure
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
    
    ## Constraints ---------------------------------------------------------------
    
    ### Only can depart from a single node
    m.addConstrs(
        (isVisited.sum('*', j) == 1 for j in Nodes),
        'departureNode')
    
    ### Only can arrive at a single node
    m.addConstrs(
        (isVisited.sum(i, '*') == 1 for i in Nodes),
        'arrivalNode')
    
    ### Time labels?
    m.addConstrs(
        (numNodes*(1 - isVisited[i, j]) >= orderOfVisit[i]-orderOfVisit[j]+1 for (i,j) in Arcs if (j!=0)),
        'timeLabels')
    
    ### Total number of Hours traveled must be less than the minHours that you define
    m.addConstr(sum(supportCost[node] * isVisited[node] for node in isVisited) <= minHours)
    
    ## Optimize the Minimum Distance Traveled
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

    
# =============================================================================
print(
"""

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
AIRPLANE_DIST = [[0, 2.4, 2.6, 2.7, 3.7, 3.4, 1.9], 
                 [2.4, 0, 2, 1.3, 1.6, 1.6, 0.6], 
                 [2.6, 2, 0, 1, 1.9, 1.6, 2], 
                 [2.7, 1.3, 1, 0, 1, 0.9, 1.4], 
                 [3.7, 1.6, 1.9, 1, 0, 0.3, 2], 
                 [3.4, 1.6, 1.6, 0.9, 0.3, 0, 2], 
                 [3.9, 1.1, 2, 1.4, 2, 2, 0]]

## Airplane Cost Matrix
AIRPLANE_COST = [[0, 670, 340, 60, 390, 130, 340], 
                 [580, 0, 300, 410, 490, 540, 110], 
                 [50, 550, 0, 240, 480, 640, 650], 
                 [180, 440, 80, 0, 140, 460, 340], 
                 [700, 450, 790, 770, 0, 330, 490], 
                 [210, 50, 400, 150, 230, 0, 730], 
                 [470, 460, 460, 60, 110, 150, 0]]


## Call Function
getMinRoute(AIRPLANE_POS_NAME, AIRPLANE_POS, 
            OBJ_MAT=AIRPLANE_DIST,    SUPPORT_MAT=AIRPLANE_COST, 
            objMeasureName = 'Time (Hours)', suportMeasureName = 'Cost (USD)',
            minHours=GRB.INFINITY)

print(
"""

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
BUS_DIST = [[0, 21, 38, 15, 22, 17, 9], 
            [17, 0, 14, 9, 11, 11, 5], 
            [18, 14, 0, 7, 13, 11, 14], 
            [19, 9, 7, 0, 7, 6, 10], 
            [26, 11, 13, 7, 0, 2, 14], 
            [24, 11, 11, 6, 2, 0, 14], 
            [25, 4, 14, 10, 14, 14, 0]]

## Bus Cost Matrix
BUS_COST = [[0, 68, 90, 76, 130, 72, 39], 
            [34, 0, 28, 45, 44, 22, 12], 
            [36, 70, 0, 14, 39, 33, 56], 
            [57, 27, 35, 0, 14, 12, 30], 
            [78, 44, 52, 35, 0, 6, 42], 
            [72, 55, 22, 24, 10, 0, 56], 
            [52, 65, 42, 20, 70, 42, 0]]

## Call Function
getMinRoute(BUS_POS_NAME, BUS_POS, 
            OBJ_MAT=BUS_COST,       SUPPORT_MAT=BUS_DIST, 
            objMeasureName = 'Cost (USD)', suportMeasureName = 'Time (Hours)',
            minHours=GRB.INFINITY)

print(
"""

PART III: 
    Minimize the total Travel Cost with Bus and Airports
    s.t. total travel time <= 30 hours 
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

# Duplicate the data - create a coppy and append by col
COMB_DIST = np.hstack((COMB_DIST, COMB_DIST))

# Append the Bus and Airplane cost matrices by row
COMB_COST = np.vstack((BUS_COST, AIRPLANE_COST))

# Duplicate the data - create a copy and append by col
COMB_COST = np.hstack((COMB_COST, COMB_COST))

# CAll function which get the minimum cost route using buses or airplanes, s.t. you travel less than 30 hours total
getMinRoute(COMB_POS_NAME, COMB_POS, 
            OBJ_MAT=COMB_COST,       SUPPORT_MAT=COMB_DIST, 
            objMeasureName = 'Cost (USD)', suportMeasureName = 'Time (Hours)',
            minHours = 30)














