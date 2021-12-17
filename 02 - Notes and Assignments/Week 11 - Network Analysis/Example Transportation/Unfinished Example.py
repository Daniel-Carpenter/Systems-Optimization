# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:24:01 2021

@author: Daniel.Carpenter
"""
from gurobipy import *

# CREATE MODEL
model = Model("Model to set supply of plants equal to demand while minimizing cost")

# SETS -----------------------------------------------------------------------

## Nodes
nodes = ['P1', 'P2', 'C1', 'C2', 'C3']


# PARAMETERS -----------------------------------------------------------------

## Demand for cities
demand = {
     ('C1'): -50, 
     ('C2'): -100,
     ('C3'): -75
}

## Arcs (arcs), cost (cost), and upper bound (upperBound) of flow within an arc
arcs, cost, upperBound = multidict({
        
    ('P1', 'C1'): [10, 60],       
    ('P1', 'C2'): [10, 90],       
    ('P1', 'C3'): [ 7, 80],       
    ('P2', 'C1'): [ 5, 20],       
    ('P2', 'C2'): [ 1, 30],       
    ('P2', 'C3'): [ 3, 80],       
})

# DECISION VARIABLES ---------------------------------------------------------
tonsOfPaint = model.addVars(arcs, vtype = GRB.CONTINUOUS, name = 'Tons of Paint',
              obj = cost) # set objective

plantSupply = model.addVars(supply, vtype = GRB.CONTINUOUS, name = 'Supply from Plants') # set objective

# CONSTRAINTS ----------------------------------------------------------------

## Upper Bound
model.addConstrs((tonsOfPaint[i, j] <= upperBound[i, j] for i, j in arcs),  "Upper Bound of Arc Flow")

## Lower Bound
model.addConstrs((tonsOfPaint[i, j] >= 0 for i, j in arcs), "Lower Bound of Arc Flow")

## Flow-Balance Constraint
model.addConstrs((plantSupply.sum(i, '*') == demand[i] for i in demand), "flowBalance")
#model.addConstrs((tonsOfPaint.sum(i, '*') - tonsOfPaint.sum('*', i) == 0 for i in nodes), "flowBalance")

## Update the model
model.update()
model.params.outputflag = 0

## Run the model
model.optimize()

## Print optimized values to console
if model.status == GRB.OPTIMAL:
    print('Optimal Solition Found\n -- OBJECTIVE FUNCTION --\n %g' % model.objVal)
    print('\n-- DECISION VARIABLES --')
    for var in model.getVars(): print ('%s: %g' % (var.varName, var.x))
    print('\n-- Dual Variables --')
    for constraint in model.getConstrs(): print('Dual Variable of constraint %s: %g' % (constraint.constrName, constraint.Pi))

