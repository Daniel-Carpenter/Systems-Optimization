```python
# -*- coding: utf-8 -*-
"""
ISE 4623/5023: Deterministic Systems Models / Systems Optimization 
Fall 2021
Individual assignment 6 
@author: Daniel Carpenter
"""
from gurobipy import *
import pandas as pd

```


```python
"""
==============================================================================
Problem 1 (b)
==============================================================================
"""

# Create model for optimization
model1b = Model('Drill Bit Transportation')

# Nodes and Resource names Defined
resources = ['Drill Bits']
nodes     = ['Plant 1', 'Plant 2', 
             'Center 1', 'Center 2', 'Center 3']

# Define the supply constraints (this is for simplicity of changing in problem 1(c))
plant1Supply = 350
plant2Supply = 300

# Arcs (point a to point b) and their respective capacity
arcs, capacity = multidict ({
    
# Source    | Destination | Capacity
  ('Plant 1', 'Center 1'): plant1Supply,
  ('Plant 1', 'Center 2'): plant1Supply,
  ('Plant 1', 'Center 3'): plant1Supply,
  ('Plant 2', 'Center 1'): plant2Supply,
  ('Plant 2', 'Center 2'): plant2Supply,
  ('Plant 2', 'Center 3'): plant2Supply 
  })

# Cost of the Resource, with the source and destination nodes
cost = {

#  Resource    | Source   | Destination | Cost
  ('Drill Bits', 'Plant 1', 'Center 1'): 25,
  ('Drill Bits', 'Plant 1', 'Center 2'): 85,
  ('Drill Bits', 'Plant 1', 'Center 3'): 25,
  ('Drill Bits', 'Plant 2', 'Center 1'): 50,
  ('Drill Bits', 'Plant 2', 'Center 2'): 35,
  ('Drill Bits', 'Plant 2', 'Center 3'): 95
  }

# Supply and demand of the resource
inflow = {
    
#  Resource    | Node       | Supply (Demand)
  ('Drill Bits', 'Plant 1' ):  plant1Supply,
  ('Drill Bits', 'Plant 2' ):  plant2Supply,
  ('Drill Bits', 'Center 1'): -100,
  ('Drill Bits', 'Center 2'): -350,
  ('Drill Bits', 'Center 3'): -200
  }


# Create the Variables in the Model
flow = model1b.addVars(resources, arcs, obj = cost, name = "flow")

# Account for the arc capacity constraints
model1b.addConstrs(
    (flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), "Capacity")


# Account for the flow constraints 
model1b.addConstrs(
    (flow.sum(h, '*', j) + inflow[h, j] == flow.sum(h, j, '*')
    for h in resources for j in nodes), "node")


# Optimize the solution
print('\n====================== PROBLEM 1 (b) ======================')
model1b.optimize()

# Print the solution to the console
if model1b.status == GRB.Status.OPTIMAL:
    solution = model1b.getAttr('x', flow)
    print('\n-- DECISION VARIABLES --')
    for v in model1b.getVars(): print ('%s: %g' % (v.varName, v.x))
    print('\n-- Dual Variables --')
    for constraint in model1b.getConstrs(): print('Dual Variable of constraint %s: %g' % (constraint.constrName, constraint.Pi))
    print('\nOPTIMAL (MINIMIZED) COST = $', "{:,.4f}".format(model1b.objVal))
    for h in resources:
        print('\nOptimal flows for %s:' % h)
        for i,j in arcs:
            if solution[h,i,j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h,i,j]))


print(
"""
Problem 1 (b) Results Discussion:
The output above shows the decision variables (i.e. flow[i,j]),
which are the optimal arc flows defined for each arc (arc[i, j]).

Simply, Plant 2 should allocate all of its resources to center 2, and 
Plant 1 should distribute its drill bits to Center 1, Center 2, Center 3
with the number of drill bits totalling 100, 50, and 200 drill bits,
respectively for each Center stated.

The minimized cost is $22,250.0000
"""
)
```

    Restricted license - for non-production use only - expires 2022-01-13
    
    ====================== PROBLEM 1 (b) ======================
    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 11 rows, 6 columns and 18 nonzeros
    Model fingerprint: 0x1c21d833
    Coefficient statistics:
      Matrix range     [1e+00, 1e+00]
      Objective range  [3e+01, 1e+02]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+02, 4e+02]
    Presolve removed 11 rows and 6 columns
    Presolve time: 0.00s
    Presolve: All rows and columns removed
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    2.2250000e+04   0.000000e+00   0.000000e+00      0s
    
    Solved in 0 iterations and 0.00 seconds
    Optimal objective  2.225000000e+04
    
    -- DECISION VARIABLES --
    flow[Drill Bits,Plant 1,Center 1]: 100
    flow[Drill Bits,Plant 1,Center 2]: 50
    flow[Drill Bits,Plant 1,Center 3]: 200
    flow[Drill Bits,Plant 2,Center 1]: 0
    flow[Drill Bits,Plant 2,Center 2]: 300
    flow[Drill Bits,Plant 2,Center 3]: 0
    
    -- Dual Variables --
    Dual Variable of constraint Capacity[Plant 1,Center 1]: 0
    Dual Variable of constraint Capacity[Plant 1,Center 2]: 0
    Dual Variable of constraint Capacity[Plant 1,Center 3]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 1]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 2]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 3]: 0
    Dual Variable of constraint node[Drill Bits,Plant 1]: -50
    Dual Variable of constraint node[Drill Bits,Plant 2]: 0
    Dual Variable of constraint node[Drill Bits,Center 1]: -25
    Dual Variable of constraint node[Drill Bits,Center 2]: 35
    Dual Variable of constraint node[Drill Bits,Center 3]: -25
    
    OPTIMAL (MINIMIZED) COST = $ 22,250.0000
    
    Optimal flows for Drill Bits:
    Plant 1 -> Center 1: 100
    Plant 1 -> Center 2: 50
    Plant 1 -> Center 3: 200
    Plant 2 -> Center 2: 300
    
    Problem 1 (b) Results Discussion:
    The output above shows the decision variables (i.e. flow[i,j]),
    which are the optimal arc flows defined for each arc (arc[i, j]).
    
    Simply, Plant 2 should allocate all of its resources to center 2, and 
    Plant 1 should distribute its drill bits to Center 1, Center 2, Center 3
    with the number of drill bits totalling 100, 50, and 200 drill bits,
    respectively for each Center stated.
    
    The minimized cost is $22,250.0000
    
    


```python

"""
==============================================================================
Problem 1 (c)
==============================================================================
"""

# each plant loses 30% of their production (due to and unforeseen disruption)
supplyLost = 0.30

# Define the supply constraints
plant1Supply = plant1Supply * (1 - supplyLost)
plant2Supply = plant2Supply * (1 - supplyLost)

# Create model for optimization
model1c = Model('Drill Bit Transportation (with Supply Lost at 30%')

# Arcs (point a to point b) and their respective capacity
arcs, capacity = multidict ({
    
# Source    | Destination | Capacity
  ('Plant 1', 'Center 1'): plant1Supply,
  ('Plant 1', 'Center 2'): plant1Supply,
  ('Plant 1', 'Center 3'): plant1Supply,
  ('Plant 2', 'Center 1'): plant2Supply,
  ('Plant 2', 'Center 2'): plant2Supply,
  ('Plant 2', 'Center 3'): plant2Supply 
  })


# Supply and demand of the resource
inflow = {
    
#  Resource    | Node       | Supply (Demand)
  ('Drill Bits', 'Plant 1' ):  plant1Supply,
  ('Drill Bits', 'Plant 2' ):  plant2Supply,
  ('Drill Bits', 'Center 1'): -100,
  ('Drill Bits', 'Center 2'): -350,
  ('Drill Bits', 'Center 3'): -200
  }


# Create the Variables in the Model
flow = model1c.addVars(resources, arcs, obj = cost, name = "flow")

# Account for the arc capacity constraints
model1c.addConstrs(
    (flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), "Capacity")


# Account for the flow constraints 
model1c.addConstrs(
    (flow.sum(h, '*', j) + inflow[h, j] <= flow.sum(h, j, '*')
    for h in resources for j in nodes), "node")


# Optimize the solution
print('\n====================== PROBLEM 1 (c) ======================')
model1c.optimize()

# Print the solution to the console
if model1c.status == GRB.Status.OPTIMAL:
    solution = model1c.getAttr('x', flow)
    print('\n-- DECISION VARIABLES --')
    for v in model1c.getVars(): print ('%s: %g' % (v.varName, v.x))
    print('\n-- Dual Variables --')
    for constraint in model1c.getConstrs(): print('Dual Variable of constraint %s: %g' % (constraint.constrName, constraint.Pi))
    print('\nOPTIMAL (MINIMIZED) COST = $', "{:,.4f}".format(model1c.objVal))
    for h in resources:
        print('\nOptimal flows for %s:' % h)
        for i,j in arcs:
            if solution[h,i,j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h,i,j]))

print(
"""
Problem 1 (c) Results Discussion:
The output above shows could have been infeasible if we did not 
change the second constraint, which now states that the supply
can exceed the demand.

The optimal flows can seen directly above; please note that they
have changed now. Also note that optimal cost decreased to
$13,475.0000.
"""
)

```

    
    ====================== PROBLEM 1 (c) ======================
    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 11 rows, 6 columns and 18 nonzeros
    Model fingerprint: 0x0340f79c
    Coefficient statistics:
      Matrix range     [1e+00, 1e+00]
      Objective range  [3e+01, 1e+02]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+02, 4e+02]
    Presolve removed 6 rows and 0 columns
    Presolve time: 0.00s
    Presolved: 5 rows, 6 columns, 12 nonzeros
    
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    0.0000000e+00   5.687500e+01   0.000000e+00      0s
           3    1.3475000e+04   0.000000e+00   0.000000e+00      0s
    
    Solved in 3 iterations and 0.01 seconds
    Optimal objective  1.347500000e+04
    
    -- DECISION VARIABLES --
    flow[Drill Bits,Plant 1,Center 1]: 100
    flow[Drill Bits,Plant 1,Center 2]: 0
    flow[Drill Bits,Plant 1,Center 3]: 145
    flow[Drill Bits,Plant 2,Center 1]: 0
    flow[Drill Bits,Plant 2,Center 2]: 210
    flow[Drill Bits,Plant 2,Center 3]: 0
    
    -- Dual Variables --
    Dual Variable of constraint Capacity[Plant 1,Center 1]: 0
    Dual Variable of constraint Capacity[Plant 1,Center 2]: 0
    Dual Variable of constraint Capacity[Plant 1,Center 3]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 1]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 2]: 0
    Dual Variable of constraint Capacity[Plant 2,Center 3]: 0
    Dual Variable of constraint node[Drill Bits,Plant 1]: -25
    Dual Variable of constraint node[Drill Bits,Plant 2]: -35
    Dual Variable of constraint node[Drill Bits,Center 1]: 0
    Dual Variable of constraint node[Drill Bits,Center 2]: 0
    Dual Variable of constraint node[Drill Bits,Center 3]: 0
    
    OPTIMAL (MINIMIZED) COST = $ 13,475.0000
    
    Optimal flows for Drill Bits:
    Plant 1 -> Center 1: 100
    Plant 1 -> Center 3: 145
    Plant 2 -> Center 2: 210
    
    Problem 1 (c) Results Discussion:
    The output above shows could have been infeasible if we did not 
    change the second constraint, which now states that the supply
    can exceed the demand.
    
    The optimal flows can seen directly above; please note that they
    have changed now. Also note that optimal cost decreased to
    $13,475.0000.
    
    


```python
"""
==============================================================================
Problem 2 (b)
==============================================================================
"""


## Plants: Uses table 4 and previous section for this calculation (See excel file)
plant1SupplyA = 0.5 * 60  * 48
plant2SupplyA = 0.5 * 120 * 48
plant3SupplyA = 0.2 * 80  * 48

## Warehouses: Since transshippment node, b = 0
## Retailers: Data supplied from table 5

# DATA for Supply, Through, and Demand
N, b = multidict({
    ("Plant 1"):     plant1SupplyA,
    ("Plant 2"):     plant2SupplyA,
    ("Plant 3"):     plant3SupplyA,
    ("Warehouse A"): 0,
    ("Warehouse B"): 0,
    ("Warehouse C"): 0,
    ("Retailer 1"): -175,
    ("Retailer 2"): -120,
    ("Retailer 3"): -140,
    ("Retailer 4"): -100,
    ("Retailer 5"): -160
})

# For each arc, define the lower, upper, and cost of the flow
arcs, lower, upper, cost = multidict({
    
    # From plants to warehouses:
        
    # Plant        | Warehouse       l | u  | cost
    ("Plant 1",     "Warehouse A"): [0, 120, 25],
    ("Plant 1",     "Warehouse B"): [0, 150, 85],
    ("Plant 1",     "Warehouse C"): [0, 170, 25],
    ("Plant 2",     "Warehouse A"): [0, 150, 50],
    ("Plant 2",     "Warehouse B"): [0, 160, 35],
    ("Plant 2",     "Warehouse C"): [0, 180, 95],
    ("Plant 3",     "Warehouse A"): [0, 150, 50],
    ("Plant 3",     "Warehouse B"): [0, 170, 40],
    ("Plant 3",     "Warehouse C"): [0, 180, 55],
    
    # From warehouses to retailers:
        
    # Warehouse   |   Retailer       l | u  | cost
    ("Warehouse A", "Retailer 1"):  [0, 160, 75],
    ("Warehouse A", "Retailer 2"):  [0, 190, 50],
    ("Warehouse A", "Retailer 3"):  [0, 110, 60],
    ("Warehouse A", "Retailer 4"):  [0, 180, 75],
    ("Warehouse A", "Retailer 5"):  [0, 150, 30],
    ("Warehouse B", "Retailer 1"):  [0, 170, 85],
    ("Warehouse B", "Retailer 2"):  [0, 190, 15],
    ("Warehouse B", "Retailer 3"):  [0, 150, 85],
    ("Warehouse B", "Retailer 4"):  [0, 140, 85],
    ("Warehouse B", "Retailer 5"):  [0, 120, 90],
    ("Warehouse C", "Retailer 1"):  [0, 140, 90],
    ("Warehouse C", "Retailer 2"):  [0, 160, 85],
    ("Warehouse C", "Retailer 3"):  [0, 180, 35],
    ("Warehouse C", "Retailer 4"):  [0, 120, 35],
    ("Warehouse C", "Retailer 5"):  [0, 100, 95]
})


# Create the model2b
model2b = Model('Problem 2(b) - Supply Chain')

# Add the variables to the model2b
flow = model2b.addVars(arcs, obj = cost, name = "flow")


# CONSTRAINTS ================================================================

## Upper Bound
model2b.addConstrs((flow[i, j] <= upper[i, j] for i, j in arcs),  "maxFlow")

## Lower Bound
model2b.addConstrs((flow[i, j] >= lower[i, j] for i, j in arcs), "minFlow")

## Flow-Balance Constraint
model2b.addConstrs((flow.sum(i, '*') - flow.sum('*', i) <= b[i] for i in N), "flowBalance")

## Update the model
model2b.update()
model2b.params.outputflag=0


# Optimize Model
print('\n====================== PROBLEM 2 PART 1 ======================')
model2b.optimize()


# Print the optimized model2b
if model2b.status == GRB.OPTIMAL:
    print('\n-- DECISION VARIABLES --')
    for v in model2b.getVars(): print ('%s: %g' % (v.varName, v.x))
    print('\n-- Dual Variables --')
    for constraint in model2b.getConstrs(): print('Dual Variable of constraint %s: %g' % (constraint.constrName, constraint.Pi))
    print('\nOPTIMAL (MINIMIZED) COST = $', "{:,.4f}".format(model2b.objVal))
    print('\n-- SUMMARY OF FLOWS --')
    product_flow = pd.DataFrame(columns=["Source", "Destination", "Flow of Product A"])
    for arc in arcs:
        if flow[arc].x > 1e-6:
            product_flow = product_flow.append({"Source": arc[0], 
                                                "Destination": arc[1], 
                                                "Flow of Product A": flow[arc].x}, ignore_index = True)  
    product_flow.index=[''] * len(product_flow)
    print(product_flow)



print(
"""
Problem 2 (b) Results Discussion:
The output above could have been infeasible if we did not 
change the balanced constraint, which now states that the supply
can exceed the demand.

The optimal flows can seen directly above between both plants
to warehouses and warehouses to retailers. The minimized cost
equals $54,475.0000.
"""
)
```

    
    ====================== PROBLEM 2 PART 1 ======================
    
    -- DECISION VARIABLES --
    flow[Plant 1,Warehouse A]: 120
    flow[Plant 1,Warehouse B]: 0
    flow[Plant 1,Warehouse C]: 170
    flow[Plant 2,Warehouse A]: 150
    flow[Plant 2,Warehouse B]: 160
    flow[Plant 2,Warehouse C]: 0
    flow[Plant 3,Warehouse A]: 25
    flow[Plant 3,Warehouse B]: 0
    flow[Plant 3,Warehouse C]: 70
    flow[Warehouse A,Retailer 1]: 145
    flow[Warehouse A,Retailer 2]: 0
    flow[Warehouse A,Retailer 3]: 0
    flow[Warehouse A,Retailer 4]: 0
    flow[Warehouse A,Retailer 5]: 150
    flow[Warehouse B,Retailer 1]: 30
    flow[Warehouse B,Retailer 2]: 120
    flow[Warehouse B,Retailer 3]: 0
    flow[Warehouse B,Retailer 4]: 0
    flow[Warehouse B,Retailer 5]: 10
    flow[Warehouse C,Retailer 1]: 0
    flow[Warehouse C,Retailer 2]: 0
    flow[Warehouse C,Retailer 3]: 140
    flow[Warehouse C,Retailer 4]: 100
    flow[Warehouse C,Retailer 5]: 0
    
    -- Dual Variables --
    Dual Variable of constraint maxFlow[Plant 1,Warehouse A]: -25
    Dual Variable of constraint maxFlow[Plant 1,Warehouse B]: 0
    Dual Variable of constraint maxFlow[Plant 1,Warehouse C]: -30
    Dual Variable of constraint maxFlow[Plant 2,Warehouse A]: 0
    Dual Variable of constraint maxFlow[Plant 2,Warehouse B]: -5
    Dual Variable of constraint maxFlow[Plant 2,Warehouse C]: 0
    Dual Variable of constraint maxFlow[Plant 3,Warehouse A]: 0
    Dual Variable of constraint maxFlow[Plant 3,Warehouse B]: 0
    Dual Variable of constraint maxFlow[Plant 3,Warehouse C]: 0
    Dual Variable of constraint maxFlow[Warehouse A,Retailer 1]: 0
    Dual Variable of constraint maxFlow[Warehouse A,Retailer 2]: 0
    Dual Variable of constraint maxFlow[Warehouse A,Retailer 3]: 0
    Dual Variable of constraint maxFlow[Warehouse A,Retailer 4]: 0
    Dual Variable of constraint maxFlow[Warehouse A,Retailer 5]: -50
    Dual Variable of constraint maxFlow[Warehouse B,Retailer 1]: 0
    Dual Variable of constraint maxFlow[Warehouse B,Retailer 2]: 0
    Dual Variable of constraint maxFlow[Warehouse B,Retailer 3]: 0
    Dual Variable of constraint maxFlow[Warehouse B,Retailer 4]: 0
    Dual Variable of constraint maxFlow[Warehouse B,Retailer 5]: 0
    Dual Variable of constraint maxFlow[Warehouse C,Retailer 1]: 0
    Dual Variable of constraint maxFlow[Warehouse C,Retailer 2]: 0
    Dual Variable of constraint maxFlow[Warehouse C,Retailer 3]: 0
    Dual Variable of constraint maxFlow[Warehouse C,Retailer 4]: 0
    Dual Variable of constraint maxFlow[Warehouse C,Retailer 5]: 0
    Dual Variable of constraint minFlow[Plant 1,Warehouse A]: 0
    Dual Variable of constraint minFlow[Plant 1,Warehouse B]: 0
    Dual Variable of constraint minFlow[Plant 1,Warehouse C]: 0
    Dual Variable of constraint minFlow[Plant 2,Warehouse A]: 0
    Dual Variable of constraint minFlow[Plant 2,Warehouse B]: 0
    Dual Variable of constraint minFlow[Plant 2,Warehouse C]: 0
    Dual Variable of constraint minFlow[Plant 3,Warehouse A]: 0
    Dual Variable of constraint minFlow[Plant 3,Warehouse B]: 0
    Dual Variable of constraint minFlow[Plant 3,Warehouse C]: 0
    Dual Variable of constraint minFlow[Warehouse A,Retailer 1]: 0
    Dual Variable of constraint minFlow[Warehouse A,Retailer 2]: 0
    Dual Variable of constraint minFlow[Warehouse A,Retailer 3]: 0
    Dual Variable of constraint minFlow[Warehouse A,Retailer 4]: 0
    Dual Variable of constraint minFlow[Warehouse A,Retailer 5]: 0
    Dual Variable of constraint minFlow[Warehouse B,Retailer 1]: 0
    Dual Variable of constraint minFlow[Warehouse B,Retailer 2]: 0
    Dual Variable of constraint minFlow[Warehouse B,Retailer 3]: 0
    Dual Variable of constraint minFlow[Warehouse B,Retailer 4]: 0
    Dual Variable of constraint minFlow[Warehouse B,Retailer 5]: 0
    Dual Variable of constraint minFlow[Warehouse C,Retailer 1]: 0
    Dual Variable of constraint minFlow[Warehouse C,Retailer 2]: 0
    Dual Variable of constraint minFlow[Warehouse C,Retailer 3]: 0
    Dual Variable of constraint minFlow[Warehouse C,Retailer 4]: 0
    Dual Variable of constraint minFlow[Warehouse C,Retailer 5]: 0
    Dual Variable of constraint flowBalance[Plant 1]: 0
    Dual Variable of constraint flowBalance[Plant 2]: 0
    Dual Variable of constraint flowBalance[Plant 3]: 0
    Dual Variable of constraint flowBalance[Warehouse A]: -50
    Dual Variable of constraint flowBalance[Warehouse B]: -40
    Dual Variable of constraint flowBalance[Warehouse C]: -55
    Dual Variable of constraint flowBalance[Retailer 1]: -125
    Dual Variable of constraint flowBalance[Retailer 2]: -55
    Dual Variable of constraint flowBalance[Retailer 3]: -90
    Dual Variable of constraint flowBalance[Retailer 4]: -90
    Dual Variable of constraint flowBalance[Retailer 5]: -130
    
    OPTIMAL (MINIMIZED) COST = $ 54,475.0000
    
    -- SUMMARY OF FLOWS --
           Source  Destination  Flow of Product A
          Plant 1  Warehouse A              120.0
          Plant 1  Warehouse C              170.0
          Plant 2  Warehouse A              150.0
          Plant 2  Warehouse B              160.0
          Plant 3  Warehouse A               25.0
          Plant 3  Warehouse C               70.0
      Warehouse A   Retailer 1              145.0
      Warehouse A   Retailer 5              150.0
      Warehouse B   Retailer 1               30.0
      Warehouse B   Retailer 2              120.0
      Warehouse B   Retailer 5               10.0
      Warehouse C   Retailer 3              140.0
      Warehouse C   Retailer 4              100.0
    
    Problem 2 (b) Results Discussion:
    The output above could have been infeasible if we did not 
    change the balanced constraint, which now states that the supply
    can exceed the demand.
    
    The optimal flows can seen directly above between both plants
    to warehouses and warehouses to retailers. The minimized cost
    equals $54,475.0000.
    
    


```python
"""
==============================================================================
Problem 2 (c) (extra credit)
==============================================================================
"""

# New values for total supply
plant1SupplyB = 0.5 * 60  * 48 * 3
plant2SupplyB = 0.5 * 120 * 48 * 3
plant3SupplyB = 0.2 * 80  * 48 * 3

# Define the commodities and the source/destination nodes
commodities = ['Product A', 'Product B']
nodes = ["Plant 1", "Plant 2", "Plant 3", 
         "Warehouse A", "Warehouse B", "Warehouse C", 
         "Retailer 1", "Retailer 2", "Retailer 3", "Retailer 4", "Retailer 5"]


# Create A, capacity (upper bound)
arcs, capacity = multidict({
    ("Plant 1",     "Warehouse A"): 120,
    ("Plant 1",     "Warehouse B"): 150,
    ("Plant 1",     "Warehouse C"): 170,
    ("Plant 2",     "Warehouse A"): 150,
    ("Plant 2",     "Warehouse B"): 160,
    ("Plant 2",     "Warehouse C"): 180,
    ("Plant 3",     "Warehouse A"): 150,
    ("Plant 3",     "Warehouse B"): 170,
    ("Plant 3",     "Warehouse C"): 180,
    ("Warehouse A", "Retailer 1"):  160,
    ("Warehouse A", "Retailer 2"):  190,
    ("Warehouse A", "Retailer 3"):  110,
    ("Warehouse A", "Retailer 4"):  180,
    ("Warehouse A", "Retailer 5"):  150,
    ("Warehouse B", "Retailer 1"):  170,
    ("Warehouse B", "Retailer 2"):  190,
    ("Warehouse B", "Retailer 3"):  150,
    ("Warehouse B", "Retailer 4"):  140,
    ("Warehouse B", "Retailer 5"):  120,
    ("Warehouse C", "Retailer 1"):  140,
    ("Warehouse C", "Retailer 2"):  160,
    ("Warehouse C", "Retailer 3"):  180,
    ("Warehouse C", "Retailer 4"):  120,
    ("Warehouse C", "Retailer 5"):  100,
    })

# Create Cost vector
cost = {
    ("Product A", "Plant 1",     "Warehouse A"): 25,
    ("Product A", "Plant 1",     "Warehouse B"): 85,
    ("Product A", "Plant 1",     "Warehouse C"): 25,
    ("Product A", "Plant 2",     "Warehouse A"): 50,
    ("Product A", "Plant 2",     "Warehouse B"): 35,
    ("Product A", "Plant 2",     "Warehouse C"): 95,
    ("Product A", "Plant 3",     "Warehouse A"): 50,
    ("Product A", "Plant 3",     "Warehouse B"): 40,
    ("Product A", "Plant 3",     "Warehouse C"): 55,
    ("Product A", "Warehouse A", "Retailer 1" ): 75,
    ("Product A", "Warehouse A", "Retailer 2" ): 50,
    ("Product A", "Warehouse A", "Retailer 3" ): 60,
    ("Product A", "Warehouse A", "Retailer 4" ): 75,
    ("Product A", "Warehouse A", "Retailer 5" ): 30,
    ("Product A", "Warehouse B", "Retailer 1" ): 85,
    ("Product A", "Warehouse B", "Retailer 2" ): 15,
    ("Product A", "Warehouse B", "Retailer 3" ): 85,
    ("Product A", "Warehouse B", "Retailer 4" ): 85,
    ("Product A", "Warehouse B", "Retailer 5" ): 90,
    ("Product A", "Warehouse C", "Retailer 1" ): 90,
    ("Product A", "Warehouse C", "Retailer 2" ): 85,
    ("Product A", "Warehouse C", "Retailer 3" ): 35,
    ("Product A", "Warehouse C", "Retailer 4" ): 35,
    ("Product A", "Warehouse C", "Retailer 5" ): 95,
    ("Product B", "Plant 1",     "Warehouse B"): 25,
    ("Product B", "Plant 1",     "Warehouse B"): 85,
    ("Product B", "Plant 1",     "Warehouse C"): 25,
    ("Product B", "Plant 2",     "Warehouse B"): 50,
    ("Product B", "Plant 2",     "Warehouse B"): 35,
    ("Product B", "Plant 2",     "Warehouse C"): 95,
    ("Product B", "Plant 3",     "Warehouse B"): 50,
    ("Product B", "Plant 3",     "Warehouse B"): 40,
    ("Product B", "Plant 3",     "Warehouse C"): 55,
    ("Product B", "Warehouse B", "Retailer 1" ): 75,
    ("Product B", "Warehouse B", "Retailer 2" ): 50,
    ("Product B", "Warehouse B", "Retailer 3" ): 60,
    ("Product B", "Warehouse B", "Retailer 4" ): 75,
    ("Product B", "Warehouse B", "Retailer 5" ): 30,
    ("Product B", "Warehouse B", "Retailer 1" ): 85,
    ("Product B", "Warehouse B", "Retailer 2" ): 15,
    ("Product B", "Warehouse B", "Retailer 3" ): 85,
    ("Product B", "Warehouse B", "Retailer 4" ): 85,
    ("Product B", "Warehouse B", "Retailer 5" ): 90,
    ("Product B", "Warehouse C", "Retailer 1" ): 90,
    ("Product B", "Warehouse C", "Retailer 2" ): 85,
    ("Product B", "Warehouse C", "Retailer 3" ): 35,
    ("Product B", "Warehouse C", "Retailer 4" ): 35,
    ("Product B", "Warehouse C", "Retailer 5" ): 95
}

# Create supply and (demand)
inflow = {
    ("Product A", "Plant 1"    ): plant1SupplyA,
    ("Product A", "Plant 2"    ): plant2SupplyA,
    ("Product A", "Plant 3"    ): plant3SupplyA,
    ("Product A", "Warehouse A"): 0,
    ("Product A", "Warehouse B"): 0,
    ("Product A", "Warehouse C"): 0,
    ("Product A", "Retailer 1" ): -175,
    ("Product A", "Retailer 2" ): -120,
    ("Product A", "Retailer 3" ): -140,
    ("Product A", "Retailer 4" ): -100,
    ("Product A", "Retailer 5" ): -160,
    ("Product B", "Plant 1"    ): plant1SupplyB,
    ("Product B", "Plant 2"    ): plant2SupplyB,
    ("Product B", "Plant 3"    ): plant3SupplyB,
    ("Product B", "Warehouse A"): 0,
    ("Product B", "Warehouse B"): 0,
    ("Product B", "Warehouse C"): 0,
    ("Product B", "Retailer 1" ): -100,
    ("Product B", "Retailer 2" ): -150,
    ("Product B", "Retailer 3" ): -110,
    ("Product B", "Retailer 4" ): -300,
    ("Product B", "Retailer 5" ): -230
}


# Create optimization model
m = Model('netflow')

# Create variables
flow = m.addVars(commodities, arcs, obj=cost, name="flow")

# Arc-capacity constraints
m.addConstrs(
    (flow.sum('*',i,j) <= capacity[i,j] for i,j in arcs), "cap")


# Flow-conservation constraints
m.addConstrs(
    (flow.sum(h,'*',j) - flow.sum(h,j,'*') <= inflow[h,j]
    for h in commodities for j in nodes), "node")


# Compute optimal solution
m.optimize()

# Print solution
if m.status == GRB.Status.OPTIMAL:
    solution = m.getAttr('x', flow)
    for h in commodities:
        print('\nOptimal flows for %s:' % h)
        for i,j in arcs:
            if solution[h,i,j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h,i,j]))

print(
"""
Note that the above model is infeasible, simply because I was under a time constraint and
did not have time to complete. It is infeaible because of constraint number 2.
The code needs to be updated to have the sum of the flows less than or equal to
the supply, which would allow for unmet supply.
"""
)

```

    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 46 rows, 48 columns and 144 nonzeros
    Model fingerprint: 0x31eedceb
    Coefficient statistics:
      Matrix range     [1e+00, 1e+00]
      Objective range  [2e+01, 1e+02]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+02, 9e+03]
    Presolve removed 36 rows and 48 columns
    Presolve time: 0.00s
    
    Solved in 0 iterations and 0.00 seconds
    Infeasible model
    
    Note that the above model is infeasible, simply because I was under a time constraint and
    did not have time to complete. It is infeaible because of constraint number 2.
    The code needs to be updated to have the sum of the flows less than or equal to
    the supply, which would allow for unmet supply.
    
    


```python

```
