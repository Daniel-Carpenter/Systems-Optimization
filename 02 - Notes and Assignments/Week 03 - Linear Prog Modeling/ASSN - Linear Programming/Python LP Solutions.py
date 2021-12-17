"""

Linear Programming in Python
Assignment 2, Problem 1(d)
@author: Daniel Carpenter

"""

# Import Gurobi and set problem1Model
from gurobipy import *


"""

Problem 1(d)

"""

# Create New Model to Optimize
problem1Model = Model("Reddy_Mikks_Company")


# DECISION VARIABLES ==========================================================

hardSeed = {}
hardSeed = problem1Model.addVar(vtype = GRB.CONTINUOUS,
                        lb = 0,
                        ub = GRB.INFINITY)

serratedSeed = {}
serratedSeed = problem1Model.addVar(vtype = GRB.CONTINUOUS,
                            lb = 0,
                            ub = GRB.INFINITY)


# OBJECTIVE FUNCTION ==========================================================

objectiveFun = (275.75 * hardSeed) + (120.50 * serratedSeed)

# Set objective function to objectiveFun
problem1Model.setObjective(objectiveFun)       

# Define whether to minimize or maximze the objective function
problem1Model.modelSense = GRB.MAXIMIZE

problem1Model.update()


# ADD CONSTRAINTS =============================================================

# Water Constraint
problem1Model.addConstr((100.05*hardSeed) + (60.75*serratedSeed) <= 810.50)

# Electricity Constraint
problem1Model.addConstr((5.50*hardSeed)   + (10.25*serratedSeed) <= 655.80)

# Gas Constraint
problem1Model.addConstr((75.30*hardSeed)  + (24.84*serratedSeed) <= 520.75)


# SOLVE MODEL =================================================================

# OptimiobjectiveFune
print("\n============== Problem 1 ==================\n")
problem1Model.optimize()

# Print Output
if problem1Model.status == GRB.OPTIMAL:
    print("\n-------------------------------------------")
    print("\nOptimal Profit (USD):\t", problem1Model.objVal)
    print("\nOptimal Seed Amounts (Number of Seed Bags):")
    print("Hard Seed Amount:\t", hardSeed.x)
    print("Serrated Seed Amount:\t", serratedSeed.x)



"""

Problem 2(i)

"""

# Create New Model to Optimize
problem2Model = Model("Reddy_Mikks_Company")


# DECISION VARIABLES ==========================================================

saudiBarrels = {}
saudiBarrels = problem2Model.addVar(vtype = GRB.CONTINUOUS,
                                    lb = 0,
                                    ub = GRB.INFINITY)

venezuelaBarrels = {}
venezuelaBarrels = problem2Model.addVar(vtype = GRB.CONTINUOUS,
                                        lb = 0,
                                        ub = GRB.INFINITY)


# OBJECTIVE FUNCTION ==========================================================

objectiveFun = (20 * saudiBarrels) + (15 * venezuelaBarrels)

# Set objective function to objectiveFun
problem2Model.setObjective(objectiveFun)       

# Define whether to minimize or maximze the objective function
problem2Model.modelSense = GRB.MINIMIZE

problem2Model.update()


# ADD CONSTRAINTS =============================================================

# Gasoline Constraint
problem2Model.addConstr((0.3*saudiBarrels) + (0.4*venezuelaBarrels) >= 2000)

# Diesel Constraint
problem2Model.addConstr((0.4*saudiBarrels) + (0.2*venezuelaBarrels) >= 1500)

# Luibricant Constraint
problem2Model.addConstr((0.2*saudiBarrels) + (0.3*venezuelaBarrels) >= 500)

# Max production per Day Constraint - Saudi, Venezuela (respectively)
problem2Model.addConstr(saudiBarrels     <= 9000)
problem2Model.addConstr(venezuelaBarrels <= 6000)


# SOLVE MODEL =================================================================

# OptimiobjectiveFune
print("\n\n============== Problem 2 ==================\n")
problem2Model.optimize()

# Print Output
if problem2Model.status == GRB.OPTIMAL:
    print("\n-------------------------------------------")
    print("\nOptimal Cost (USD):\t", problem2Model.objVal)
    print("\nOptimal Barrels per Day:")
    print("Saudi Arabia Barrels:\t", saudiBarrels.x)
    print("Venezuela Barrels:\t", venezuelaBarrels.x)
