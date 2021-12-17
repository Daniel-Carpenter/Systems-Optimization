"""
Transportation Analysis Example

Systems Optimization
"""

# Import Gurobi
from gurobipy import *

# CREATE MODEL ================================================================
m = Model(name = 'Min Cost Flow Model')


# SETS AND PARAMETERS =========================================================



## Set N (the capacity constraints), 
## and parameter b (the supply and demand)
N, b = multidict({
    ('plant1'):    350,
    ('plant2'):    300,
    ('center1'):  -100,
    ('center2'):  -350,
    ('center3'):  -200
})

## Set A, paramaters l, u, & c
A, l, u, c = multidict({
    ('node1', 'node2'): [2, 5, 1],
    ('node1', 'node3'): [2, 8, 4],
    ('node3', 'node2'): [2, 8, 2],
    ('node2', 'node4'): [0, 7, 3],
    ('node3', 'node5'): [1, 8, 1],
    ('node4', 'node5'): [1, 9, 5],
    ('node4', 'node6'): [1, 6, 2],
    ('node5', 'node6'): [0, 6, 3]    
})


# VARIABLES ===================================================================
x = m.addVars(A, obj = c, name = "x")

# OBJECTIVE FUNCTION ==========================================================
# Already done in above assignment

# CONSTRAINTS =================================================================

## Upper Bound
m.addConstrs((x[i, j] <= u[i, j] for i, j in A),  "maxFlow")

## Lower Bound
m.addConstrs((x[i, j] >= l[i, j] for i, j in A), "minFlow")

## Flow-Balance Constraint
m.addConstrs((x.sum(i, '*') - x.sum('*', i) == b[i] for i in N), "flowBalance")

## Update the model
m.update()
m.params.outputflag=0

## Run the model
m.optimize()

## Print optimized values to console
if m.status == GRB.OPTIMAL:
    print('Optimal Solition Found\n -- OBJECTIVE FUNCTION --\n %g' % m.objVal)
    print('\n-- DECISION VARIABLES --')
    for v in m.getVars(): print ('%s: %g' % (v.varName, v.x))
    print('\n-- Dual Variables --')
    for constraint in m.getConstrs(): print('Dual Variable of constraint %s: %g' % (constraint.constrName, constraint.Pi))












