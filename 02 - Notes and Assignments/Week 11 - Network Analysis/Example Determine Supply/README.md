# Determining the Supply in a Network with `Gurobi`

## Conceptual Overview:
 Suppose that you are about to open a company that produces paint. You have built two production plants `(P1 and P2)` to supply the demands of three nearby cities `(C1, C2, and C3)`, but you still need to decide how much production capacity (in tons) you should assign to each plant.

The figure below indicates the expected `demand` in each city (in tons). Also, the figure indicates (in parenthesis) the unitary `flow cost `(dollars per ton) and the `maximum capacity` (in
tons) associated with each arc (respectively.

<br>

<img src ="Images\pSetup.png" height = 350>

--- 
 
## Setup of Problem

### Mathematical Formulation
<img src ="Images\mSetup.png">

--- 

## Questions to Answer:
1. Considering the information given, how much production capacity should be given to plants P1 and P2, so that the final paint distribution cost is
minimized?
2. What is the optimal distribution cost for this problem?
3. Construct and solve the associated dual problem. Create a table to indicate the values of each dual variable found and discuss their meaning
in the context of the original problem.

<br>

## Code

```python
"""
Transportation Analysis Example from Previous Final

Goal is to determine the supply of each plant
In doing so, you must minimize the cost given the demand of the city
s.t. 
    flow of goods is <= the upper bound of the path
    flow of goods is >= the lower bound of the path
"""

# Import Gurobi
from gurobipy import *

```


```python
# CREATE MODEL ================================================================
m = Model(name = 'Transportation - Previous Final Exam')


# SETS ========================================================================
Plants = ['Plant 1', 'Plant 2']
Cities = ['City 1', 'City 2', 'City 3']

```

    Restricted license - for non-production use only - expires 2022-01-13
    


```python
# PARAMETERS ==================================================================

## The demand of the city
demand = {'City 1': 50, 
          'City 2': 100, 
          'City 3': 75}

## Define the cost, lowerBound, and upperBound:
### cost: the cost of the path from a plant ∈ Plants to a city ∈ Cities
### lowerBound: the lower bound of each path from a plant ∈ Plants to a city ∈ Cities
### upperBound: the upper bound (capacity limit) of each path from a plant ∈ Plants to a city ∈ Cities
Arcs, cost, lowerBound, upperBound = multidict({
        ('Plant 1', 'City 1'): [10, 0, 60],
        ('Plant 1', 'City 2'): [10, 0, 90],
        ('Plant 1', 'City 3'): [ 7, 0, 80],
        ('Plant 2', 'City 1'): [ 5, 0, 20],
        ('Plant 2', 'City 2'): [ 1, 0, 30],
        ('Plant 2', 'City 3'): [ 3, 0, 80],
    })

```


```python
# DECISION VARIABLES AND OBJECTIVE FUNCTION ==================================

## The flow of goods from a plant ∈ Plants to a city ∈ Cities
flow = m.addVars(Arcs, name = 'flow',
                 
## Objective = cost, minimized by default
                 obj = cost)

```


```python
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

```




    {('Plant 1', 'City 1'): <gurobi.Constr *Awaiting Model Update*>,
     ('Plant 1', 'City 2'): <gurobi.Constr *Awaiting Model Update*>,
     ('Plant 1', 'City 3'): <gurobi.Constr *Awaiting Model Update*>,
     ('Plant 2', 'City 1'): <gurobi.Constr *Awaiting Model Update*>,
     ('Plant 2', 'City 2'): <gurobi.Constr *Awaiting Model Update*>,
     ('Plant 2', 'City 3'): <gurobi.Constr *Awaiting Model Update*>}




```python
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
    
    print('\nDual Variables:')
    for constr in m.getConstrs(): print('Dual:\t%s:\t%g' % (constr.constrName, constr.Pi))

```

    
    ========= OPTIMIZED MODEL =========
    
    Optimized cost: 1355 (in USD)
    
    Optimal Supply of the Plants
    Plant 1:	100.0
    Plant 2:	125.0
    
    Decision Variables (flow from plant to city): 
    Plant 1	->	City 1:	30.0
    Plant 1	->	City 2:	70.0
    Plant 1	->	City 3:	0.0
    Plant 2	->	City 1:	20.0
    Plant 2	->	City 2:	30.0
    Plant 2	->	City 3:	75.0
    
    Dual Variables:
    Dual:	demand[City 1]:	10
    Dual:	demand[City 2]:	10
    Dual:	demand[City 3]:	3
    Dual:	lowerFlow[Plant 1,City 1]:	0
    Dual:	lowerFlow[Plant 1,City 2]:	0
    Dual:	lowerFlow[Plant 1,City 3]:	0
    Dual:	lowerFlow[Plant 2,City 1]:	0
    Dual:	lowerFlow[Plant 2,City 2]:	0
    Dual:	lowerFlow[Plant 2,City 3]:	0
    Dual:	upperFlow[Plant 1,City 1]:	0
    Dual:	upperFlow[Plant 1,City 2]:	0
    Dual:	upperFlow[Plant 1,City 3]:	0
    Dual:	upperFlow[Plant 2,City 1]:	-5
    Dual:	upperFlow[Plant 2,City 2]:	-9
    Dual:	upperFlow[Plant 2,City 3]:	0
    


```python

```
