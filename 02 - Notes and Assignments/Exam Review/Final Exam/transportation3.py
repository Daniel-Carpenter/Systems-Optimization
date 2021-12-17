"""
Traveling Salesmen (Minimize distance traveled through sources and destinations)
"""

from gurobipy import *

# Create model for optimization
m = Model('Drill Bit Transportation')

# Sets (KEY INPUTS) ===========================================================

## ---------------------------------------------------------------------------
## Position (POS)
POS = [[35, 97], [38, 90], [37, 78]]

## Distance Matrix (DIST)
DIST = [[0, 514, 1228], [515, 0, 754], [1233, 753, 0]]
## ---------------------------------------------------------------------------

## Create Empty Sets and Paremters to append in following block 

### Nodes
N = tuplelist([])

### Arcs
A = tuplelist([])

### Cost
c = {}

### Read distance and position lists to create set of node (N), arcs (A), and
### Distance between nodes (c)
for i, pos_i in enumerate(POS):
    N.append(i)
    for j, pos_j in enumerate(POS):
        if j!= i:
            append((i, j))
            c[i, j] = DIST[i][j]
            
### COunt of nodes
n = len(N)

# OPTIMIZATION ================================================================

## Create the model