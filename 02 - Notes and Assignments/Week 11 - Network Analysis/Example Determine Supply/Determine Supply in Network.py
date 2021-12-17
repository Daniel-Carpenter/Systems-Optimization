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


# CREATE MODEL ================================================================
m = Model(name = 'Transportation - Previous Final Exam')


# SETS ========================================================================
Plants = ['Plant 1', 'Plant 2']
Cities = ['City 1', 'City 2', 'City 3']


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












