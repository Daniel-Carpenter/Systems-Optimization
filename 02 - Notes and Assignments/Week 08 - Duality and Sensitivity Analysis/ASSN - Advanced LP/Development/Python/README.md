```python
"""
Daniel Carpenter - ID: 113009743

==============================================================================
Problem 1. (b)
==============================================================================
"""


from gurobipy import *
model1b = Model("Reddy_Mikks_Company")


# DECISION VARIABLES ==========================================================

w1 = {}
w1 = model1b.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)
    
w2 = {}
w2 = model1b.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)

w3 = {}
w3 = model1b.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)


# OBJECTIVE FUNCTION ==========================================================

z = (810.50*w1) + (655.80*w2) + (520.75*w3)

# Set objective function to z
model1b.setObjective(z)       

# Define whether to minimize or mawimize
model1b.modelSense = GRB.MINIMIZE

model1b.update()

# ADD CONSTRAINTS =============================================================

model1b.addConstr(100.05*w1 +	 5.50*w2 + 75.30*w3 >= 275.75)
model1b.addConstr( 60.75*w1 + 10.25*w2 + 24.84*w3	>= 120.50)


# SOLVE MODEL =================================================================

# Optimize
print("\nSOLUTION TO PROBLEM 1 ------------------------------\n")
model1b.optimize()

# Print Output
if (model1b.status == GRB.OPTIMAL):
        print("\nOptimal value (profit in USD Thousands:", model1b.objVal)
        print("--- Production Variables ---")
        print("w1: ", w1.x)
        print("w2: ", w2.x)
        print("w3: ", w3.x)
```

    Restricted license - for non-production use only - expires 2022-01-13
    
    SOLUTION TO PROBLEM 1 ------------------------------
    
    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 2 rows, 3 columns and 6 nonzeros
    Model fingerprint: 0xb44da65c
    Coefficient statistics:
      Matrix range     [6e+00, 1e+02]
      Objective range  [5e+02, 8e+02]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+02, 3e+02]
    Presolve removed 0 rows and 1 columns
    Presolve time: 0.00s
    Presolved: 2 rows, 2 columns, 4 nonzeros
    
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    0.0000000e+00   6.459375e+01   0.000000e+00      0s
           2    2.0332340e+03   0.000000e+00   0.000000e+00      0s
    
    Solved in 2 iterations and 0.00 seconds
    Optimal objective  2.033233991e+03
    
    Optimal value (profit in USD Thousands: 2033.2339909550537
    --- Production Variables ---
    w1:  1.064515063662119
    w2:  0.0
    w3:  2.2476131192643427
    


```python
"""
==============================================================================
Problem 1. (d)
==============================================================================
"""

# Likely not the right standard from estimate. Watch videos or see slides

model1d = Model("Reddy_Mikks_Company")

# DECISION VARIABLES ==========================================================

w1 = {}
w1 = model1d.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)
    
w2 = {}
w2 = model1d.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)

w3 = {}
w3 = model1d.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)


# OBJECTIVE FUNCTION ==========================================================

z = (810.50*w1) + (655.80*w2) + (520.75*w3)

# Set objective function to z
model1d.setObjective(z)       

# Define whether to minimize or mawimize
model1d.modelSense = GRB.MINIMIZE

model1d.update()

# ADD CONSTRAINTS =============================================================

model1d.addConstr(100.05*w1 +  5.50*w2 + 75.30*w3 >= 275.75)
model1d.addConstr( 60.75*w1 + 10.25*w2 + 24.84*w3	>= 120.50)
model1d.addConstr(w1 >= 0)
model1d.addConstr(w2 >= 0)
model1d.addConstr(w3 >= 0)


# SOLVE MODEL =================================================================

# Optimize
print("\nSOLUTION TO PROBLEM 2 ------------------------------\n")
model1d.optimize()

# Print Output
if (model1d.status == GRB.OPTIMAL):
        print("\nOptimal value (profit in USD Thousands:", model1d.objVal)
        print("--- Production Variables ---")
        print("w1: ", w1.x)
        print("w2: ", w2.x)
        print("w3: ", w3.x)
```

    
    SOLUTION TO PROBLEM 2 ------------------------------
    
    Gurobi Optimizer version 9.1.2 build v9.1.2rc0 (win64)
    Thread count: 10 physical cores, 20 logical processors, using up to 20 threads
    Optimize a model with 5 rows, 3 columns and 9 nonzeros
    Model fingerprint: 0xd23bf9a5
    Coefficient statistics:
      Matrix range     [1e+00, 1e+02]
      Objective range  [5e+02, 8e+02]
      Bounds range     [0e+00, 0e+00]
      RHS range        [1e+02, 3e+02]
    Presolve removed 3 rows and 1 columns
    Presolve time: 0.00s
    Presolved: 2 rows, 2 columns, 4 nonzeros
    
    Iteration    Objective       Primal Inf.    Dual Inf.      Time
           0    0.0000000e+00   6.459375e+01   0.000000e+00      0s
           2    2.0332340e+03   0.000000e+00   0.000000e+00      0s
    
    Solved in 2 iterations and 0.01 seconds
    Optimal objective  2.033233991e+03
    
    Optimal value (profit in USD Thousands: 2033.2339909550537
    --- Production Variables ---
    w1:  1.064515063662119
    w2:  0.0
    w3:  2.2476131192643427
    
