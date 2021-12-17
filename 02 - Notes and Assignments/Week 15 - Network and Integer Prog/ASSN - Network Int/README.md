# Traveling Salesman with `Gurobi`

## Conceptual Overview:
```
After 7 months of travel from Earth, on February 18, 2021, NASA’s rover Perseverance landed on Mars, in the Jezero crater located in the Syrtis Major square of the Martian surface. The rover is part of the Mars 2020 mission, and its purpose is to collect information on the habitability of the planet, search for possible microbial life, collect and store rock samples, among others. In the rock sample collection procedure, the mission control team divided the Syrtis Major into 15 quadrants in which the Perseverance will move to perform the respective task. The map of the region, as well as the quadrant labeling are shown in Figure
1.
```
 
--- 
 
## Setup

### Map of Mars and Quadrants
<img src ="Images\setup1.png">

<br>

### Distance between quadrants
<img src ="Images\setup2.png">

--- 
<br>

## Optimal Solution (Visually)
<img src ="Images\opt.png">


<br>

## Code

```python
"""
Traveling Salesmen (Minimize distance traveled through sources and destinations)
"""

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
    #m.addConstr(sum(supportCost[node] * isVisited[node] for node in isVisited) <= minHours)
    
    ## Optimize the Minimum Distance Traveled
    m.modelSense = GRB.MINIMIZE
    m.setParam('OutputFlag', 0)
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

    
# =============================================================================

```


```python
print(
"""
Minimize the total energy of route for Mars Rover:
"""
)

# INPUTS:

## Name of the positions
POS_NAME = ['Quadrant 1', 'Quadrant 2', 'Quadrant 3', 'Quadrant 4', 'Quadrant 5', 
            'Quadrant 6', 'Quadrant 7', 'Quadrant 8', 'Quadrant 9', 'Quadrant 10', 
            'Quadrant 11', 'Quadrant 12', 'Quadrant 13', 'Quadrant 14', 'Quadrant 15']

# Positions
POS =  [['Quadrant 1', 'Quadrant 1'], 
        ['Quadrant 2', 'Quadrant 2'], 
        ['Quadrant 3', 'Quadrant 3'], 
        ['Quadrant 4', 'Quadrant 4'], 
        ['Quadrant 5', 'Quadrant 5'], 
        ['Quadrant 6', 'Quadrant 6'], 
        ['Quadrant 7', 'Quadrant 7'], 
        ['Quadrant 8', 'Quadrant 8'], 
        ['Quadrant 9', 'Quadrant 9'], 
        ['Quadrant 10', 'Quadrant 10'], 
        ['Quadrant 11', 'Quadrant 11'], 
        ['Quadrant 12', 'Quadrant 12'], 
        ['Quadrant 13', 'Quadrant 13'], 
        ['Quadrant 14', 'Quadrant 14'], 
        ['Quadrant 15', 'Quadrant 15']]

# Distances between all positions
DIST = [[0, 15.8, 3.81, 7.54, 22.9, 6.89, 15.2, 10.4, 17.7, 9.51, 10.3, 22.1, 9.33, 19.6, 7.4], 
        [15.8, 0, 22.6, 21.4, 3.75, 3.57, 23.4, 15.2, 4.41, 7.85, 8.67, 21.8, 12.4, 5.09, 13.9], 
        [3.81, 22.6, 0, 10, 17.1, 2.95, 24, 13.3, 8.88, 17.6, 7.99, 22.8, 18.4, 17.3, 24], 
        [7.54, 21.4, 10, 0, 7.59, 3.99, 3.87, 6.29, 6.41, 15.2, 25.2, 3.33, 13.4, 6.07, 7.75], 
        [22.9, 3.75, 17.1, 7.59, 0, 7.08, 7.6, 21.6, 13.8, 8.79, 13, 4.4, 4.52, 8.55, 13.7], 
        [6.89, 3.57, 2.95, 3.99, 7.08, 0, 11.1, 4.81, 4.87, 18.8, 22.2, 5.92, 7.86, 17.4, 7.1], 
        [15.2, 23.4, 24, 3.87, 7.6, 11.1, 0, 16.2, 15.6, 25.9, 20.2, 25.9, 4.18, 7.82, 8.9], 
        [10.4, 15.2, 13.3, 6.29, 21.6, 4.81, 16.2, 0, 15.9, 19.3, 10.4, 13.3, 4.72, 16.9, 5.66], 
        [17.7, 4.41, 8.88, 6.41, 13.8, 4.87, 15.6, 15.9, 0, 6.1, 11, 9.11, 2.3, 24.1, 15.5], 
        [9.51, 7.85, 17.6, 15.2, 8.79, 18.8, 25.9, 19.3, 6.1, 0, 17.1, 21.5, 25.5, 23.2, 6.22], 
        [10.3, 8.67, 7.99, 25.2, 13, 22.2, 20.2, 10.4, 11, 17.1, 0, 14, 6.26, 22.6, 13.6], 
        [22.1, 21.8, 22.8, 3.33, 4.4, 5.92, 25.9, 13.3, 9.11, 21.5, 14, 0, 17.3, 25.3, 5.56], 
        [9.33, 12.4, 18.4, 13.4, 4.52, 7.86, 4.18, 4.72, 2.3, 25.5, 6.26, 17.3, 0, 4.02, 6.51], 
        [19.6, 5.09, 17.3, 6.07, 8.55, 17.4, 7.82, 16.9, 24.1, 23.2, 22.6, 25.3, 4.02, 0, 4.67], 
        [7.4, 13.9, 24, 7.75, 13.7, 7.1, 8.9, 5.66, 15.5, 6.22, 13.6, 5.56, 6.51, 4.67, 0]]

```

    
    Minimize the total energy of route for Mars Rover:
    
    


```python
# Call function to minimize distance
getMinRoute(POS_NAME, POS, 
            OBJ_MAT=DIST, objMeasureName='Energy Expenditure (Joules)', 
            minHours=GRB.INFINITY)

```

    Restricted license - for non-production use only - expires 2022-01-13
    
    ======== Optimized Energy Expenditure (Joules) ========
    Total Optimized Energy Expenditure (Joules): 	77.71
    
    Optimal Path:
    Quadrant 1	->	Quadrant 11
    Quadrant 2	->	Quadrant 9
    Quadrant 3	->	Quadrant 1
    Quadrant 4	->	Quadrant 12
    Quadrant 5	->	Quadrant 2
    Quadrant 6	->	Quadrant 3
    Quadrant 7	->	Quadrant 4
    Quadrant 8	->	Quadrant 6
    Quadrant 9	->	Quadrant 10
    Quadrant 10	->	Quadrant 15
    Quadrant 11	->	Quadrant 13
    Quadrant 12	->	Quadrant 5
    Quadrant 13	->	Quadrant 14
    Quadrant 14	->	Quadrant 7
    Quadrant 15	->	Quadrant 8
    
