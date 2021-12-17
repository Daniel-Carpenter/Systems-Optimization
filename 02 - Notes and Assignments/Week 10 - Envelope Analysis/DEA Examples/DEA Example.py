"""
DEA Analysis - Testing Efficiencies releative to peer group
"""

from gurobipy import *
m = Model("DEA Example")

# CREATE SETS ================================================================

#  Note List [], Tuple (Cannot modify) (), Dictionary {}
I = [1, 2]
O = [1]
S = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]

# Select the desired Student to compare
p = 49


# CREATE PARAMETERS ==========================================================

x = {
        # Input 1 
        (1, 40): 2,
        (1, 41): 19,
        (1, 42): 18,
        (1, 43): 5,
        (1, 44): 18,
        (1, 45): 0,
        (1, 46): 15,
        (1, 47): 4,
        (1, 48): 0,
        (1, 49): 15,
        
        # Input 2
        (2, 40): 15,
        (2, 41): 4,
        (2, 42): 10,
        (2, 43): 5,
        (2, 44): 11,
        (2, 45): 11,
        (2, 46): 6,
        (2, 47): 15,
        (2, 48): 14,
        (2, 49): 8
}

y = {
        (1, 40): 63,
        (1, 41): 78,
        (1, 42): 86,
        (1, 43): 52,
        (1, 44): 80,
        (1, 45): 97,
        (1, 46): 65,
        (1, 47): 51,
        (1, 48): 72,
        (1, 49): 54
}


# CREATE VARIABLES ===========================================================

## Phi (maximize this later)
phi = m.addVar(lb    = -GRB.INFINITY,
               ub    =  GRB.INFINITY,
               vtype =  GRB.CONTINUOUS,
               name  = 'phi')

## Lambda Variables
lambdas = m.addVars(S, name = "lambda")

## Update the model
m.update()

# SET OBJECTIVE TO PHI =======================================================

## Maximize phi
z = phi
m.setObjective(z, GRB.MAXIMIZE)


# CONSTRAINTS ================================================================
m.addConstrs(sum(x[i, j] * lambdas[j] for j in S) <= x[i, p] for i in I)
m.addConstrs(sum(y[o, j] * lambdas[j] for j in S) >= y[o, p] * phi for o in O)
m.addConstr( sum(lambdas[j] for j in S) == 1)

m.update()

# Optimize the model!!!!

m.optimize()

if m.status == GRB.OPTIMAL:
    print("\n Optimal Found:",
          "\n\n Objective (phi): %g" % m.objVal,
          "\n\n Decision Variables:")
    for var in m.getVars():
        print('%s %g' % (var.varName, var.x))







