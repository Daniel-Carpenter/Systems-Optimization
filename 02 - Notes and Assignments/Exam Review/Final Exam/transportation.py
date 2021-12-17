"""
Practice Transportation Optimization
"""

from gurobipy import *

# CREATE MODEL
m = Model("Transportation Example")


# SETS
Plants  = [1, 2]
Centers = [1, 2, 3]


# PARAMETERS
cost = {(1, 1): 25,
        (1, 2): 85,
        (1, 3): 25,
        (2, 1): 50,
        (2, 2): 35,
        (2, 3): 95,
}

supply = {1: 350,
          2: 300}

demand = {1: 100,
          2: 350,
          3: 200}

# VARIABLES
flowOfBits = m.addVars(cost.keys(), name = "flowOfBits")

# OBJECTIVE FUNCTION
obj = sum(flowOfBits[i] * cost[i] for i in cost)

# CONSTRAINTS

## Supply
for p in Plants:
    m.addConstr(sum(flowOfBits[(p, c)] for c in Centers) == supply[p])

## Demand
for c in Centers:
    m.addConstr(sum(flowOfBits[(p, c)] for p in Plants) == demand[c])

# OPTIMIZE
m.setObjective(obj, GRB.MINIMIZE)
m.update()
m.optimize()

if m.STATUS == GRB.OPTIMAL:
    m.printAttr("X")
