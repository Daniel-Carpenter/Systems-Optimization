# General Knapsack Function and Ouput

```python
"""
@author: Daniel Carpenter

Knapsack Function with Multiple Bags
Given a number of bags and weight capcity of each bag, what is the optimal 
way to pack these bags?
"""
```




    '\n@author: Daniel Carpenter\n\nKnapsack Function with Multiple Bags\nGiven a number of bags and weight capcity of each bag, what is the optimal \nway to pack these bags?\n'




```python
# Inputs 

## The bags you want to pack
Bags = ['Bag 1', 'Bag 2', 'Bag 3']

## Capacity of each bags
bagCapacities = {'Bag 1':15, 'Bag 2':50, 'Bag 3':20}

## Names of the Excel file and sheet
xlFileName  = 'Data'
xlSheetName = 'Data'

```


```python
# Import Gurobi
from gurobipy import *

# Import excel reading package
import openpyxl as opxl

```


```python
# Create the knapsack model, given inputs defined above
def knapsackOptMultipleBags(Bags, bagCapacities, xlFileName, xlSheetName):
    
    # Create the model
    m = Model('General Knapsack - Packing Multiple Bags given weight constraint')
    m.setParam(GRB.Param.OutputFlag, 0)
    
    # SETS =======================================================================
    
    # The item and its number that you are considering packing
    Items = []
    
    # PARAMETERS =================================================================
    
    ## weight (in pounds) of each item that you are considering packing
    weight = {}
    
    ## Intrinsic value of each item that you are considering packing
    value = {}
    
    ## Read in the values of the Items, weight, and value in the 'Data.xlxs' file
    
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
        
    print('\nOptimization with multiple bags')
    printOptimalSolution(m, isPacked, weight, value, Items, Bags)
    
```


```python
# Call function and return optimal results
knapsackOptMultipleBags(Bags, bagCapacities, xlFileName, xlSheetName)
```

    
    Optimization with multiple bags
    Optimizing your vacation: maximize value of packed items while not packing too much
    
    *Optimal value of packed items: 110.0000 total intrinsic value
    
    
    ======== Bag 1 ========
    
    Total Weight of bag: 15.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 6: 	1.0	 |	4	 |	4
    Item 17: 	1.0	 |	7	 |	7
    Item 28: 	1.0	 |	4	 |	10
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	4
    Item 2: 	 0.0	|	5	|	10
    Item 3: 	 0.0	|	5	|	6
    Item 4: 	 0.0	|	9	|	1
    Item 5: 	 0.0	|	9	|	4
    Item 7: 	 0.0	|	7	|	8
    Item 8: 	 0.0	|	7	|	6
    Item 9: 	 0.0	|	6	|	5
    Item 10: 	 0.0	|	3	|	1
    Item 11: 	 0.0	|	7	|	9
    Item 12: 	 0.0	|	8	|	4
    Item 13: 	 0.0	|	3	|	4
    Item 14: 	 0.0	|	8	|	5
    Item 15: 	 0.0	|	4	|	7
    Item 16: 	 0.0	|	3	|	1
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
    
    
    ======== Bag 2 ========
    
    Total Weight of bag: 50.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 2: 	1.0	 |	5	 |	10
    Item 3: 	1.0	 |	5	 |	6
    Item 7: 	1.0	 |	7	 |	8
    Item 13: 	1.0	 |	3	 |	4
    Item 15: 	1.0	 |	4	 |	7
    Item 20: 	1.0	 |	7	 |	9
    Item 22: 	1.0	 |	8	 |	10
    Item 29: 	1.0	 |	3	 |	3
    Item 30: 	1.0	 |	8	 |	9
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	4
    Item 4: 	 0.0	|	9	|	1
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 0.0	|	4	|	4
    Item 8: 	 0.0	|	7	|	6
    Item 9: 	 0.0	|	6	|	5
    Item 10: 	 0.0	|	3	|	1
    Item 11: 	 0.0	|	7	|	9
    Item 12: 	 0.0	|	8	|	4
    Item 14: 	 0.0	|	8	|	5
    Item 16: 	 0.0	|	3	|	1
    Item 17: 	 0.0	|	7	|	7
    Item 18: 	 0.0	|	9	|	9
    Item 19: 	 0.0	|	6	|	3
    Item 21: 	 0.0	|	6	|	3
    Item 23: 	 0.0	|	7	|	2
    Item 24: 	 0.0	|	9	|	5
    Item 25: 	 0.0	|	3	|	2
    Item 26: 	 0.0	|	4	|	5
    Item 27: 	 0.0	|	5	|	5
    Item 28: 	 0.0	|	4	|	10
    
    
    ======== Bag 3 ========
    
    Total Weight of bag: 20.0 lbs.
    
    Items that you should pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 11: 	1.0	 |	7	 |	9
    Item 18: 	1.0	 |	9	 |	9
    Item 26: 	1.0	 |	4	 |	5
    
    Items that you should NOT pack:
    Item | isPacked 	| lbs. 	| Intrinsic Value
    Item 1: 	 0.0	|	4	|	4
    Item 2: 	 0.0	|	5	|	10
    Item 3: 	 0.0	|	5	|	6
    Item 4: 	 0.0	|	9	|	1
    Item 5: 	 0.0	|	9	|	4
    Item 6: 	 0.0	|	4	|	4
    Item 7: 	 0.0	|	7	|	8
    Item 8: 	 0.0	|	7	|	6
    Item 9: 	 0.0	|	6	|	5
    Item 10: 	 0.0	|	3	|	1
    Item 12: 	 0.0	|	8	|	4
    Item 13: 	 0.0	|	3	|	4
    Item 14: 	 0.0	|	8	|	5
    Item 15: 	 0.0	|	4	|	7
    Item 16: 	 0.0	|	3	|	1
    Item 17: 	 0.0	|	7	|	7
    Item 19: 	 0.0	|	6	|	3
    Item 20: 	 0.0	|	7	|	9
    Item 21: 	 0.0	|	6	|	3
    Item 22: 	 0.0	|	8	|	10
    Item 23: 	 0.0	|	7	|	2
    Item 24: 	 0.0	|	9	|	5
    Item 25: 	 0.0	|	3	|	2
    Item 27: 	 0.0	|	5	|	5
    Item 28: 	 0.0	|	4	|	10
    Item 29: 	 0.0	|	3	|	3
    Item 30: 	 0.0	|	8	|	9
    