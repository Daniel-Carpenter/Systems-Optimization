```python
"""
DEA Analysis - Testing Efficiencies releative to peer group
"""

from gurobipy import *
m = Model("DEA Example")
```


```python
# CREATE SETS ================================================================

#  Note List [], Tuple (Cannot modify) (), Dictionary {}
I = [1, 2]
O = [1]
S = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]

# Select the desired Student to compare
p = 49
```


```python
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
```


```python

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
```


```python
# SET OBJECTIVE TO PHI =======================================================

## Maximize phi
z = phi
m.setObjective(z, GRB.MAXIMIZE)
```


```python
# CONSTRAINTS ================================================================
m.addConstrs(sum(x[i, j] * lambdas[j] for j in S) <= x[i, p] for i in I)
m.addConstrs(sum(y[o, j] * lambdas[j] for j in S) >= y[o, p] * phi for o in O)
m.addConstr( sum(lambdas[j] for j in S) == 1)

m.update()
```


```python
# Optimize the model!!!!

m.optimize()

## Print the objective, phi (Proportional change of the output needed to achieve efficiency), 
## and lambdas (percentage / weight given to a person (set)
if m.status == GRB.OPTIMAL:
    print("\n Optimal Found:",
          "\n\n Objective (phi): %g" % m.objVal,
          "\n\n Decision Variables:")
    for var in m.getVars():
        print('%s %g' % (var.varName, var.x))
```

    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 4 rows, 11 columns and 39 nonzeros
    Model fingerprint: 0xc0e9d706
    Coefficient statistics:
      Matrix range     [1e+00, 1e+02]
      Objective range  [1e+00, 1e+00]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+00, 2e+01]
    Presolve removed 1 rows and 1 columns
    Presolve time: 0.00s
    Presolved: 3 rows, 10 columns, 28 nonzeros
    
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    1.7962963e+00   6.460000e-01   0.000000e+00      0s
           3    1.6455026e+00   0.000000e+00   0.000000e+00      0s
    
    Solved in 3 iterations and 0.01 seconds
    Optimal objective  1.645502646e+00
    
     Optimal Found: 
    
     Objective (phi): 1.6455 
    
     Decision Variables:
    phi 1.6455
    lambda[40] 0
    lambda[41] 0.428571
    lambda[42] 0
    lambda[43] 0
    lambda[44] 0
    lambda[45] 0.571429
    lambda[46] 0
    lambda[47] 0
    lambda[48] 0
    lambda[49] 0
    
