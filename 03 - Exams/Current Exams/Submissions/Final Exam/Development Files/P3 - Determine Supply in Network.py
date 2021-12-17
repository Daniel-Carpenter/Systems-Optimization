"""
Problem 3:
Production capcity and distribution

Goal is to determine the supply of each plant
In doing so, you must minimize the cost given the demand of the city
s.t. 
    flow of goods is <= the upper bound of the path
    flow of goods is >= the lower bound of the path
"""

# Import Gurobi
from gurobipy import *


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
    
    print('\nDual Variables:')
    for constr in m.getConstrs(): print('Dual:\t%s:\t%g' % (constr.constrName, constr.Pi))












