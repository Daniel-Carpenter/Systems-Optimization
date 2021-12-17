"""
Daniel Carpenter - ID: 113009743
Problem 1. (b)
"""


from gurobipy import *
model = Model("Reddy_Mikks_Company")


# DECISION VARIABLES ==========================================================

w1 = {}
w1 = model.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)

w2 = {}
w2 = model.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)

w3 = {}
w3 = model.addVar(vtype = GRB.CONTINUOUS,
                  lb = 0,
                  ub = GRB.INFINITY)


# OBJECTIVE FUNCTION ==========================================================

z = (810.50*w1) + (655.80*w2) + (520.75*w3)

# Set objective function to z
model.setObjective(z)       

# Define whether to minimize or mawimize
model.modelSense = GRB.MINIMIZE

model.update()

# ADD CONSTRAINTS =============================================================

model.addConstr(100.05*w1 +	 5.50*w2 + 75.30*w3 >= 275.75)
model.addConstr( 60.75*w1 + 10.25*w2 + 24.84*w3	>= 120.50)


# SOLVE MODEL =================================================================

# Optimize
model.optimize()

# Print Output
if (model.status == GRB.OPTIMAL): {
        print("Optimal value (profit in USD Thousands:", model.objVal)
        #print("--- Production Variables ---")
        #print("w1: ", w1.w)
        #print("w2: ", w2.w)
        
}


















