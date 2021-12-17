"""
Transportation Example 2
"""
from gurobipy import *

# Create the model
m = Model("Efficient Allocation of Resources")

# Sets
Employees    = ['Daniel', 'Roman', 'Brandon',
               'Ryan', 'Spencer', 'Jonathan']
Projects     = ['Dashboards', 'Labor', 'AdHoc']

# Parameters
supplyOfHours = 120

OPPORUNITY_COST = 1.5
hourlyCost = {
    ('Daniel', 'Dashboards'): 45, 
    ('Roman', 'Dashboards'): 62.5 * OPPORUNITY_COST, 
    ('Brandon', 'Dashboards'): 50, 
    ('Ryan', 'Dashboards'): 30, 
    ('Spencer', 'Dashboards'): 37.5, 
    ('Jonathan', 'Dashboards'): 45, 
    
    ('Daniel', 'Labor'): 45, 
    ('Roman', 'Labor'): 62.5, 
    ('Brandon', 'Labor'): 50, 
    ('Ryan', 'Labor'): 30, 
    ('Spencer', 'Labor'): 37.5, 
    ('Jonathan', 'Labor'): 45, 
    
    ('Daniel', 'AdHoc'): 45, 
    ('Roman', 'AdHoc'): 62.5, 
    ('Brandon', 'AdHoc'): 50, 
    ('Ryan', 'AdHoc'): 30, 
    ('Spencer', 'AdHoc'): 37.5, 
    ('Jonathan', 'AdHoc'): 45
}
             


hoursDemandedOfProject = {'Dashboards': 500,
                          'Labor':      200,
                          'AdHoc':      220
    }


# Decision Variables
hoursDevoted = m.addVars(hourlyCost.keys(), name = "Allocation")

# Objective
obj = sum(hoursDevoted[c] * hourlyCost[c] for c in hourlyCost)
m.setObjective(obj, GRB.MINIMIZE)

# Constraints

## Supply of Hours
for e in Employees:
    m.addConstr(sum(hoursDevoted[(e, p)] for p in Projects) == supplyOfHours)

## Demand of Hours
for p in Projects:
    m.addConstr(sum(hoursDevoted[(e, p)] for e in Employees) <= hoursDemandedOfProject[p])

# Optimize
m.update()
m.optimize()

if m.STATUS == GRB.OPTIMAL:
    print('\nX = hours devoted to a project')
    m.printAttr('X')





