# Traveling Salesman with `Gurobi`

## Conceptual Overview:
* Goal is to go on a trip and minimzie the distance traveled while visiting both St. Louis and Charlottsville once
* We will start and finish the trip at Norman, OK 
 
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
Example finds the minimum distance between major US cities for a single route
"""

from gurobipy import *

# Create model for optimization
m = Model('Traveling Salesman')

```

    Restricted license - for non-production use only - expires 2022-01-13
    


```python
# Sets (KEY INPUTS) ===========================================================

## ---------------------------------------------------------------------------
## Position name (POS_NAME), Position (POS) - doesnt really matter what is in this, and Distance Matrix (DIST)
POS_NAME = ['Norman', 'St. Louis', 'Charlettsville']
POS = [[35, 97], [38, 90], [37, 78]]
DIST = [[0,    514, 1228], 
        [515,  0,   754 ], 
        [1233, 753, 0   ]]
## ---------------------------------------------------------------------------

## Create Empty Sets and Paremters to append in following block 

### Nodes
N = tuplelist([])

### Arcs
A = tuplelist([])

### Cost
c = {}

### Read distance and position lists to create set of node (N), arcs (A), and
### Distance between nodes (c)
for i, pos_i in enumerate(POS):
    N.append(i)
    for j, pos_j in enumerate(POS):
        if j!= i:
            A.append((i, j))
            c[i, j] = DIST[i][j]
            
### COunt of nodes
n = len(N)

```


```python
# OPTIMIZATION ================================================================

## Create the model
m = Model('Traveling Salesman')

## Create variables and the coefficients of the objective function
x = m.addVars(A, obj = c, name = 'x', vtype = GRB.BINARY)
u = m.addVars(N, obj = 0, name = 'u')

## Constraints ---------------------------------------------------------------

### Only can depart from a single node
m.addConstrs(
    (x.sum('*', j) == 1 for j in N),
    'departureNode')

### Only can arrive at a single node
m.addConstrs(
    (x.sum(i, '*') == 1 for i in N),
    'arrivalNode')

### Time labels?
m.addConstrs(
    (n*(1 - x[i, j]) >= u[i]-u[j]+1 for (i,j) in A if (j!=0)),
    'timeLabels')

## Optimize the Minimum Distance Traveled
m.modelSense = GRB.MINIMIZE
m.setParam('OutputFlag', 0)
m.optimize()

# Print the solution
if m.status == GRB.Status.OPTIMAL:
    solution_OF = m.objVal
    solution_x  = m.getAttr('x', x) 
    solution_u  = m.getAttr('x', u)
    print('\nTotal (Optimized) Distance: %g' % solution_OF)
    print('\nOptimal Path:')
    for i, j in A:
        if solution_x[i,j] > 0:
            print('%s\t->\t%s' % (POS_NAME[i], POS_NAME[j]))
            
```

    
    Total (Optimized) Distance: 2496
    
    Optimal Path:
    Norman	->	Charlettsville
    St. Louis	->	Norman
    Charlettsville	->	St. Louis
    
