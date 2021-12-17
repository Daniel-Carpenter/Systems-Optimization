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














