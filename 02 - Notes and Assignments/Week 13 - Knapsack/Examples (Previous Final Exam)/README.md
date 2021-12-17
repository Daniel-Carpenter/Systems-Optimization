```python
"""
Knapsack Example
Daniel Carpenter

Problem from previous final exam
"""

# Import Gurobi
from gurobipy import *

# Import excel reading package
import openpyxl as opxl

# Create the model
m = Model('Knapsack Previous Final Exam - Packing for Vacation')
m.setParam(GRB.Param.OutputFlag, 0)

```

    Restricted license - for non-production use only - expires 2022-01-13
    


```python
# Create print function
def printOptimalSolution(model, isPacked, weight, value, Items, Bags):
    if model.status == GRB.Status.OPTIMAL:
        print('Optimizing your vacation: maximize value of packed items while not packing too much')
        
        # Print the optimal intrinsic value
        print("\n*Optimal value of packed items: " 
              + "{:,.4f}".format(model.objVal) + " total intrinsic value")
        
        for bag in Bags:
            
            print('\n\n======== ' + bag + " ========")
        
            # GEt the total weight of the bag
            totalWeight = sum(weight[item] * isPacked[bag, item].x 
                              for item in Items)
            
            # print the total amount packed in lbs
            print('\nTotal Weight of bag: ' + str(totalWeight) + ' lbs.')
            
            # Print the items packed with weight and value
            print("\nItems that you should pack:")
            print("Item | isPacked \t| lbs. \t| Intrinsic Value")
            for item in Items:
                if isPacked[bag, item].x > 0.5:
                    print(str(item) + ": " 
                          + "\t"    + str(isPacked[bag, item].x)
                          + "\t |\t" + str(  weight[item])
                          + "\t |\t" + str(   value[item]))
        
            # Print the items NOT packed with weight and value
            print("\nItems that you should NOT pack:")
            print("Item | isPacked \t| lbs. \t| Intrinsic Value")
            for item in Items:
                if isPacked[bag, item].x < 0.5:
                    print(str(item) + ": " 
                          + "\t "    + str(isPacked[bag, item].x)
                          + "\t|\t" + str(  weight[item])
                          + "\t|\t" + str(   value[item]))
    
```


```python
"""
PART I:
    Imagine that you are planning your next vacations.
    For your trip, first you want to determine which items to pack. 
    To take this decision, you make a list of 30 items from which you want to 
    pick the ones to be packed. For each of these 30 items, you know 
    its weight (in pounds) and its associated intrinsic value 
    (the more you want to take the item, the higher its “value”)
"""

# SETS =======================================================================

# The item and its number that you are considering packing
Items = []
Bags  = ['Bag 1']

# PARAMETERS =================================================================

## weight (in pounds) of each item that you are considering packing
weight = {}

## Intrinsic value of each item that you are considering packing
value = {}

## Read in the values of the Items, weight, and value in the 'Data.xlxs' file
xlFileName  = 'Data'
xlSheetName = 'Data'

xlFile = opxl.load_workbook(xlFileName + ".xlsx")

### First Row to read in minus 1
row = 5 - 1

## Loop through each row and col and insert data into sets and parameters
while xlFile[xlSheetName].cell(row = row + 1, column = 2).value:
    
    #### Read in item name
    newItem = xlFile[xlSheetName].cell(row = row + 1, column = 2).value
    Items.append(newItem)
    
    #### Read in weight col
    weight[newItem] = xlFile[xlSheetName].cell(row = row + 1, column = 3).value
    
    #### read in value col
    value[newItem] = xlFile[xlSheetName].cell(row = row + 1, column = 4).value
    
    #### Increment row
    row += 1


## Capacity of one bag = 15 lbs
bagCapacities = {'Bag 1':15}

# DESCISION VARIABLES ========================================================
isPacked = m.addVars(Bags, Items, vtype = GRB.BINARY)


# OPTIMIZATION ===============================================================

## Add the new constraint for two bags capacity
m.addConstrs(quicksum(weight[item] * isPacked[bag, item] for item in Items) 
                     <= bagCapacities[bag] for bag in Bags)

## Maximize the intrinsic value of the packed items for each bag
objFun = quicksum(quicksum(value[item] * isPacked[bag, item] 
                           for item in Items) 
                  for bag in Bags)

## Set objective, update the model, and Optimize
m.setObjective(objFun, GRB.MAXIMIZE)
m.update()
m.optimize()


# OUTPUT =====================================================================
            
# Print the solution to the console
print('\nPART I: ONLY ONE BAG')
printOptimalSolution(m, isPacked, weight, value, Items, Bags)
            
```

    
    PART I: ONLY ONE BAG
    Optimizing your vacation: maximize value of packed items while not packing too much
    
    *Optimal value of packed items: 27.0000 total intrinsic value
    
    
    ======== Bag 1 ========
    
    Total Weight of bag: 13.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 2: 	1.0	 |	5	 |	10
    Item 15: 	1.0	 |	4	 |	7
    Item 28: 	1.0	 |	4	 |	10
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	4
    Item 3: 	 0.0	|	5	|	6
    Item 4: 	 0.0	|	9	|	1
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 0.0	|	4	|	4
    Item 7: 	 0.0	|	7	|	8
    Item 8: 	 0.0	|	7	|	6
    Item 9: 	 0.0	|	6	|	5
    Item 10: 	 0.0	|	3	|	1
    Item 11: 	 0.0	|	7	|	9
    Item 12: 	 0.0	|	8	|	4
    Item 13: 	 0.0	|	3	|	4
    Item 14: 	 0.0	|	8	|	5
    Item 16: 	 0.0	|	3	|	1
    Item 17: 	 0.0	|	7	|	7
    Item 18: 	 0.0	|	9	|	9
    Item 19: 	 0.0	|	6	|	3
    Item 20: 	 0.0	|	7	|	9
    Item 21: 	 0.0	|	6	|	3
    Item 22: 	 0.0	|	8	|	10
    Item 23: 	 0.0	|	7	|	2
    Item 24: 	 0.0	|	9	|	5
    Item 25: 	 0.0	|	3	|	2
    Item 26: 	 0.0	|	4	|	5
    Item 27: 	 0.0	|	5	|	5
    Item 29: 	 0.0	|	3	|	3
    Item 30: 	 0.0	|	8	|	9
    


```python
"""
PART II:
    Now, assume that for your trip you can use two bags. 
    The first  bag has a maximum capacity of 15 pounds and 
    the second one has a maximum capacity of 50 pounds.
"""

# SETS =======================================================================

## New SET defining the bags
Bags.append('Bag 2')

## Second Bag Capacity = 50 lbs
bagCapacities = {'Bag 1':15, 'Bag 2':50}


# DESCISION VARIABLES ========================================================
isPacked = m.addVars(Bags, Items, vtype = GRB.BINARY)


# OPTIMIZATION ===============================================================

## Add the new constraint for two bags capacity
m.addConstrs(quicksum(weight[item] * isPacked[bag, item] for item in Items) 
                     <= bagCapacities[bag] for bag in Bags)

## C2: The item cannot be packed in multiple bags
PACKED = 1

### The sum of the binary var `item` (over all bags '*') cannot exceed a count of 1
for item in Items:
        m.addConstr(isPacked.sum('*', item) <= PACKED)

## Maximize the intrinsic value of the packed items for each bag
objFun = quicksum(quicksum(value[item] * isPacked[bag, item] 
                           for item in Items) 
                  for bag in Bags)

## Set objective, update the model, and Optimize
m.setObjective(objFun, GRB.MAXIMIZE)
m.update()
m.optimize()

print('\n\nPART II: MULTIPLE BAGS')
printOptimalSolution(m, isPacked, weight, value, Items, Bags)

```

    
    
    PART II: MULTIPLE BAGS
    Optimizing your vacation: maximize value of packed items while not packing too much
    
    *Optimal value of packed items: 90.0000 total intrinsic value
    
    
    ======== Bag 1 ========
    
    Total Weight of bag: 15.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 13: 	1.0	 |	3	 |	4
    Item 22: 	1.0	 |	8	 |	10
    Item 26: 	1.0	 |	4	 |	5
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 -0.0	|	4	|	4
    Item 2: 	 -0.0	|	5	|	10
    Item 3: 	 -0.0	|	5	|	6
    Item 4: 	 -0.0	|	9	|	1
    Item 5: 	 -0.0	|	9	|	4
    Item 6: 	 -0.0	|	4	|	4
    Item 7: 	 -0.0	|	7	|	8
    Item 8: 	 -0.0	|	7	|	6
    Item 9: 	 -0.0	|	6	|	5
    Item 10: 	 -0.0	|	3	|	1
    Item 11: 	 -0.0	|	7	|	9
    Item 12: 	 -0.0	|	8	|	4
    Item 14: 	 -0.0	|	8	|	5
    Item 15: 	 -0.0	|	4	|	7
    Item 16: 	 -0.0	|	3	|	1
    Item 17: 	 -0.0	|	7	|	7
    Item 18: 	 -0.0	|	9	|	9
    Item 19: 	 -0.0	|	6	|	3
    Item 20: 	 -0.0	|	7	|	9
    Item 21: 	 -0.0	|	6	|	3
    Item 23: 	 -0.0	|	7	|	2
    Item 24: 	 -0.0	|	9	|	5
    Item 25: 	 -0.0	|	3	|	2
    Item 27: 	 -0.0	|	5	|	5
    Item 28: 	 -0.0	|	4	|	10
    Item 29: 	 -0.0	|	3	|	3
    Item 30: 	 -0.0	|	8	|	9
    
    
    ======== Bag 2 ========
    
    Total Weight of bag: 50.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 2: 	1.0	 |	5	 |	10
    Item 3: 	1.0	 |	5	 |	6
    Item 7: 	1.0	 |	7	 |	8
    Item 11: 	1.0	 |	7	 |	9
    Item 15: 	1.0	 |	4	 |	7
    Item 20: 	1.0	 |	7	 |	9
    Item 28: 	1.0	 |	4	 |	10
    Item 29: 	1.0	 |	3	 |	3
    Item 30: 	1.0	 |	8	 |	9
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 -0.0	|	4	|	4
    Item 4: 	 -0.0	|	9	|	1
    Item 5: 	 -0.0	|	9	|	4
    Item 6: 	 -0.0	|	4	|	4
    Item 8: 	 -0.0	|	7	|	6
    Item 9: 	 -0.0	|	6	|	5
    Item 10: 	 -0.0	|	3	|	1
    Item 12: 	 -0.0	|	8	|	4
    Item 13: 	 -0.0	|	3	|	4
    Item 14: 	 -0.0	|	8	|	5
    Item 16: 	 -0.0	|	3	|	1
    Item 17: 	 -0.0	|	7	|	7
    Item 18: 	 -0.0	|	9	|	9
    Item 19: 	 -0.0	|	6	|	3
    Item 21: 	 -0.0	|	6	|	3
    Item 22: 	 -0.0	|	8	|	10
    Item 23: 	 -0.0	|	7	|	2
    Item 24: 	 -0.0	|	9	|	5
    Item 25: 	 -0.0	|	3	|	2
    Item 26: 	 -0.0	|	4	|	5
    Item 27: 	 -0.0	|	5	|	5
    