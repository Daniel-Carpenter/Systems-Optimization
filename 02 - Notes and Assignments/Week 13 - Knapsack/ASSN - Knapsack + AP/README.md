```python
"""
@author:     Daniel Carpenter
@assignment: 7
@problems:
    1: Knapsack
    2: Aggregate Planning
"""

from gurobipy import *
import openpyxl as opxl

```


```python
# SETS & PARAMETERS ==========================================================
Projects      = []
cost          = {}
jobsGenerated = {}


# Read data from Excel -------------------------------------------------------

## Make connection with the file and store in object
xlFile = opxl.load_workbook("ConstructionProjects.xlsx")
row = 1

## Loop through each row and col and insert data into sets and parameters
while xlFile["ConstructionProjects"].cell(row = row + 1, column = 2).value:
    
    ### get the project number and add to the set of Projects
    project = xlFile["ConstructionProjects"].cell(row = row + 1, column = 1).value
    Projects.append(project)
    
    ### Get the cost of the individual project and store data
    cost[project]          = xlFile["ConstructionProjects"].cell(row = row + 1, column = 2).value
    
    ### Get the number of jobs generated for the individual project and store data
    jobsGenerated[project] = xlFile["ConstructionProjects"].cell(row = row + 1, column = 3).value
    row += 1

## Validate correct Reading of Excel Data    
print("\nThe Projects")
print(Projects)

print("\nThe Costs")
print(cost)

print("\nThe Jobs Generated")
print(jobsGenerated)


## The budget for all projects: millions of USD 
budget = 200

# OPTIMIZATION MODEL =========================================================

## Model
m1 = Model('Construction Projects Optimization')
m1.setParam(GRB.Param.OutputFlag, 0)

## Variables 
isExecuted = {project : m1.addVar(vtype = GRB.BINARY, 
                                 name = "isExecuted[" + str(project) + "]") 
              for project in Projects}

## Constraints
m1.addConstr(quicksum(cost[project] * isExecuted[project] for project in Projects) <= budget)

## Objective Function
objFun = quicksum(jobsGenerated[project] * isExecuted[project] for project in Projects)

## Optimize the model and set the model sense to maximize
m1.setObjective(objFun, GRB.MAXIMIZE)
m1.update()
m1.optimize()

# PRINT RESULTS ==============================================================

# Print the solution to the console
print("MODEL 1 (Original")
if m1.status == GRB.Status.OPTIMAL:
    print("\n*Optimal number of jobs that the project generated: " 
          + "{:,.4f}".format(m1.objVal) + " thousand jobs")
    print('\n**Below shows each project that was executed, their cost, and the jobs generated.')
    print('  Note that if a project in the set of Projects does not exist here,')
    print('  Then including it does not given an optimial solution. Therefore ignored.\n')
    print("\tProject\t| Executed\t| Cost\t| Jobs Generated")
    for project in Projects:
        if isExecuted[project].x > 0.5:
            print("\tproject[" + str(project) + "] =" 
                  + "\t"     + str(   isExecuted[project].x)
                  + "\t|\t" + str(         cost[project])
                  + "\t|\t" + str(jobsGenerated[project]))

```

    
    The Projects
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249]
    
    The Costs
    {0: 2.1, 1: 2.5, 2: 0.8, 3: 1.5, 4: 2.3, 5: 2.2, 6: 0.8, 7: 2.1, 8: 2.4, 9: 2, 10: 2.2, 11: 3, 12: 2.4, 13: 2.2, 14: 0.7, 15: 0.3, 16: 1.7, 17: 2, 18: 1.4, 19: 0.6, 20: 2.4, 21: 1.5, 22: 1, 23: 2.5, 24: 2.8, 25: 2.3, 26: 1.7, 27: 2.6, 28: 0.3, 29: 1, 30: 2.8, 31: 2.6, 32: 0.3, 33: 1.3, 34: 0.1, 35: 1.7, 36: 0.5, 37: 2.3, 38: 0.4, 39: 2.8, 40: 0.1, 41: 0.3, 42: 2.9, 43: 1.4, 44: 1.3, 45: 0.1, 46: 2.8, 47: 1.3, 48: 1.2, 49: 2.8, 50: 2.4, 51: 2.2, 52: 0.8, 53: 1.7, 54: 1.1, 55: 2.3, 56: 2.9, 57: 0.9, 58: 2.6, 59: 2.7, 60: 0.3, 61: 2.7, 62: 0.2, 63: 1.1, 64: 2.2, 65: 0.5, 66: 1.4, 67: 1.8, 68: 0.6, 69: 2.7, 70: 2, 71: 1.5, 72: 0.3, 73: 0.6, 74: 2, 75: 1.9, 76: 1.8, 77: 0.2, 78: 1.2, 79: 1.5, 80: 1.9, 81: 3, 82: 0.1, 83: 0.1, 84: 2.4, 85: 2.6, 86: 0.9, 87: 0.6, 88: 1.9, 89: 2.9, 90: 1.4, 91: 0.3, 92: 0.1, 93: 1.5, 94: 0.2, 95: 0.3, 96: 1.9, 97: 2.1, 98: 1.1, 99: 1.2, 100: 1.5, 101: 2.7, 102: 0.1, 103: 2.2, 104: 1.3, 105: 2.1, 106: 2.3, 107: 1.1, 108: 2.5, 109: 1.9, 110: 2.1, 111: 2.9, 112: 2, 113: 3, 114: 0.5, 115: 2.3, 116: 1, 117: 0.8, 118: 1.7, 119: 0.4, 120: 2.5, 121: 1.8, 122: 2.1, 123: 2.1, 124: 2.3, 125: 1.4, 126: 0.9, 127: 2, 128: 2.9, 129: 0.2, 130: 2.3, 131: 3, 132: 2.5, 133: 2.2, 134: 1.8, 135: 1.1, 136: 1.9, 137: 1.3, 138: 1.2, 139: 1.4, 140: 0.4, 141: 1.3, 142: 0.6, 143: 1.1, 144: 1.5, 145: 1.6, 146: 2.1, 147: 2.7, 148: 1.3, 149: 2.7, 150: 1.8, 151: 2.5, 152: 0.7, 153: 0.5, 154: 0.4, 155: 1.8, 156: 1.2, 157: 2.4, 158: 0.9, 159: 2.2, 160: 0.3, 161: 0.4, 162: 2.2, 163: 1, 164: 0.1, 165: 1.1, 166: 1.5, 167: 3, 168: 1.8, 169: 2.1, 170: 0.3, 171: 2.8, 172: 1.4, 173: 1.5, 174: 2.7, 175: 1.5, 176: 1.3, 177: 1, 178: 1.2, 179: 1, 180: 1.5, 181: 0.3, 182: 0.1, 183: 0.2, 184: 1.9, 185: 0.2, 186: 1.4, 187: 3, 188: 2.4, 189: 1.4, 190: 0.1, 191: 2.8, 192: 1.1, 193: 1.1, 194: 0.4, 195: 2, 196: 2.6, 197: 2.4, 198: 2, 199: 1.8, 200: 1.9, 201: 1.9, 202: 1.2, 203: 0.7, 204: 1.2, 205: 2.3, 206: 0.2, 207: 2.1, 208: 1.2, 209: 1.5, 210: 1.9, 211: 0.9, 212: 1.4, 213: 1.6, 214: 2.7, 215: 0.5, 216: 1.5, 217: 2.7, 218: 1.7, 219: 1.4, 220: 2.7, 221: 1.6, 222: 3, 223: 2.6, 224: 3, 225: 2.4, 226: 0.7, 227: 2.5, 228: 2.7, 229: 1.5, 230: 0.1, 231: 1.2, 232: 2.2, 233: 0.1, 234: 3, 235: 2, 236: 0.8, 237: 0.4, 238: 0.9, 239: 2.3, 240: 2.8, 241: 1.1, 242: 0.8, 243: 2.5, 244: 0.9, 245: 2, 246: 1.6, 247: 2.3, 248: 1.6, 249: 0.1}
    
    The Jobs Generated
    {0: 1.9, 1: 2.4, 2: 1.6, 3: 1, 4: 1.3, 5: 2.7, 6: 0.2, 7: 0.1, 8: 2.3, 9: 2.8, 10: 1.1, 11: 1.1, 12: 1.7, 13: 1.3, 14: 1, 15: 0.2, 16: 1.6, 17: 2.7, 18: 1.8, 19: 2.7, 20: 0.2, 21: 0.4, 22: 1.9, 23: 1.9, 24: 1.6, 25: 2.3, 26: 1.1, 27: 1.2, 28: 2.2, 29: 1.4, 30: 0.2, 31: 2.1, 32: 1, 33: 0.8, 34: 0.4, 35: 1.6, 36: 1.5, 37: 2.5, 38: 1.2, 39: 3, 40: 0.1, 41: 2.7, 42: 0.4, 43: 1.6, 44: 0.7, 45: 2.7, 46: 1, 47: 2.3, 48: 0.6, 49: 0.3, 50: 1.7, 51: 1.5, 52: 1.7, 53: 2.9, 54: 2.5, 55: 0.2, 56: 1.7, 57: 2.3, 58: 2.5, 59: 2.7, 60: 0.1, 61: 0.9, 62: 2.1, 63: 0.8, 64: 1.1, 65: 2.4, 66: 2.5, 67: 0.4, 68: 2.5, 69: 0.7, 70: 2.7, 71: 0.1, 72: 2.9, 73: 1.4, 74: 0.3, 75: 1.7, 76: 2, 77: 0.6, 78: 1.5, 79: 0.8, 80: 2.5, 81: 1.8, 82: 1.4, 83: 1.6, 84: 0.8, 85: 0.5, 86: 1.9, 87: 3, 88: 2.5, 89: 2.6, 90: 1.6, 91: 1, 92: 0.3, 93: 2.8, 94: 2.1, 95: 2.7, 96: 1.2, 97: 0.9, 98: 2, 99: 0.6, 100: 0.3, 101: 1, 102: 2.3, 103: 2.8, 104: 1.5, 105: 1.6, 106: 0.5, 107: 2.6, 108: 0.9, 109: 1.6, 110: 0.7, 111: 1.8, 112: 0.6, 113: 0.8, 114: 0.6, 115: 2.4, 116: 1.7, 117: 1.8, 118: 2.3, 119: 1.3, 120: 1.3, 121: 0.5, 122: 2.9, 123: 2.4, 124: 0.2, 125: 1.8, 126: 1.7, 127: 2.1, 128: 1.4, 129: 2.6, 130: 1.6, 131: 0.2, 132: 0.6, 133: 2.5, 134: 2.3, 135: 0.4, 136: 2.5, 137: 2.7, 138: 2.2, 139: 0.7, 140: 1.5, 141: 1.5, 142: 0.8, 143: 0.1, 144: 1.7, 145: 0.6, 146: 2, 147: 2.4, 148: 0.2, 149: 0.5, 150: 1.9, 151: 2.7, 152: 0.1, 153: 1.7, 154: 0.5, 155: 2.5, 156: 0.9, 157: 1.5, 158: 2.9, 159: 1.6, 160: 1.7, 161: 2.7, 162: 2.9, 163: 0.1, 164: 1.6, 165: 2.8, 166: 0.8, 167: 2.6, 168: 0.4, 169: 1.3, 170: 0.2, 171: 0.5, 172: 2.8, 173: 0.6, 174: 0.9, 175: 0.9, 176: 1.9, 177: 1.1, 178: 2.8, 179: 2, 180: 1.4, 181: 2.2, 182: 0.3, 183: 3, 184: 1.5, 185: 0.5, 186: 1.2, 187: 2.4, 188: 1.6, 189: 2, 190: 2.5, 191: 1.3, 192: 1.7, 193: 1.5, 194: 0.3, 195: 1.3, 196: 1.7, 197: 2.9, 198: 1.4, 199: 0.4, 200: 1.1, 201: 2.5, 202: 0.4, 203: 0.1, 204: 2, 205: 2.4, 206: 0.5, 207: 2, 208: 1.6, 209: 1.2, 210: 0.7, 211: 2.7, 212: 2.9, 213: 3, 214: 1.1, 215: 0.3, 216: 1.1, 217: 0.4, 218: 2, 219: 0.7, 220: 2.5, 221: 1.6, 222: 1.6, 223: 1.8, 224: 0.5, 225: 0.8, 226: 2.9, 227: 0.8, 228: 2.2, 229: 2.2, 230: 0.1, 231: 1.6, 232: 1.6, 233: 0.5, 234: 1.4, 235: 1.9, 236: 0.7, 237: 1.9, 238: 1.8, 239: 1.9, 240: 1.1, 241: 0.2, 242: 3, 243: 1.9, 244: 2.1, 245: 2.8, 246: 1.7, 247: 1.2, 248: 0.6, 249: 0.2}
    MODEL 1 (Original
    
    *Optimal number of jobs that the project generated: 302.1000 thousand jobs
    
    **Below shows each project that was executed, their cost, and the jobs generated.
      Note that if a project in the set of Projects does not exist here,
      Then including it does not given an optimial solution. Therefore ignored.
    
    	Project	| Executed	| Cost	| Jobs Generated
    	project[0] =	1.0	|	2.1	|	1.9
    	project[1] =	1.0	|	2.5	|	2.4
    	project[2] =	1.0	|	0.8	|	1.6
    	project[5] =	1.0	|	2.2	|	2.7
    	project[8] =	1.0	|	2.4	|	2.3
    	project[9] =	1.0	|	2	|	2.8
    	project[14] =	1.0	|	0.7	|	1
    	project[15] =	1.0	|	0.3	|	0.2
    	project[16] =	1.0	|	1.7	|	1.6
    	project[17] =	1.0	|	2	|	2.7
    	project[18] =	1.0	|	1.4	|	1.8
    	project[19] =	1.0	|	0.6	|	2.7
    	project[22] =	1.0	|	1	|	1.9
    	project[23] =	1.0	|	2.5	|	1.9
    	project[25] =	1.0	|	2.3	|	2.3
    	project[28] =	1.0	|	0.3	|	2.2
    	project[29] =	1.0	|	1	|	1.4
    	project[31] =	1.0	|	2.6	|	2.1
    	project[32] =	1.0	|	0.3	|	1
    	project[34] =	1.0	|	0.1	|	0.4
    	project[35] =	1.0	|	1.7	|	1.6
    	project[36] =	1.0	|	0.5	|	1.5
    	project[37] =	1.0	|	2.3	|	2.5
    	project[38] =	1.0	|	0.4	|	1.2
    	project[39] =	1.0	|	2.8	|	3
    	project[40] =	1.0	|	0.1	|	0.1
    	project[41] =	1.0	|	0.3	|	2.7
    	project[43] =	1.0	|	1.4	|	1.6
    	project[45] =	1.0	|	0.1	|	2.7
    	project[47] =	1.0	|	1.3	|	2.3
    	project[52] =	1.0	|	0.8	|	1.7
    	project[53] =	1.0	|	1.7	|	2.9
    	project[54] =	1.0	|	1.1	|	2.5
    	project[57] =	1.0	|	0.9	|	2.3
    	project[58] =	1.0	|	2.6	|	2.5
    	project[59] =	1.0	|	2.7	|	2.7
    	project[62] =	1.0	|	0.2	|	2.1
    	project[63] =	1.0	|	1.1	|	0.8
    	project[65] =	1.0	|	0.5	|	2.4
    	project[66] =	1.0	|	1.4	|	2.5
    	project[68] =	1.0	|	0.6	|	2.5
    	project[70] =	1.0	|	2	|	2.7
    	project[72] =	1.0	|	0.3	|	2.9
    	project[73] =	1.0	|	0.6	|	1.4
    	project[75] =	1.0	|	1.9	|	1.7
    	project[76] =	1.0	|	1.8	|	2
    	project[77] =	1.0	|	0.2	|	0.6
    	project[78] =	1.0	|	1.2	|	1.5
    	project[80] =	1.0	|	1.9	|	2.5
    	project[82] =	1.0	|	0.1	|	1.4
    	project[83] =	1.0	|	0.1	|	1.6
    	project[86] =	1.0	|	0.9	|	1.9
    	project[87] =	1.0	|	0.6	|	3
    	project[88] =	1.0	|	1.9	|	2.5
    	project[89] =	1.0	|	2.9	|	2.6
    	project[90] =	1.0	|	1.4	|	1.6
    	project[91] =	1.0	|	0.3	|	1
    	project[92] =	1.0	|	0.1	|	0.3
    	project[93] =	1.0	|	1.5	|	2.8
    	project[94] =	1.0	|	0.2	|	2.1
    	project[95] =	1.0	|	0.3	|	2.7
    	project[98] =	1.0	|	1.1	|	2
    	project[102] =	1.0	|	0.1	|	2.3
    	project[103] =	1.0	|	2.2	|	2.8
    	project[104] =	1.0	|	1.3	|	1.5
    	project[105] =	1.0	|	2.1	|	1.6
    	project[107] =	1.0	|	1.1	|	2.6
    	project[109] =	1.0	|	1.9	|	1.6
    	project[114] =	1.0	|	0.5	|	0.6
    	project[115] =	1.0	|	2.3	|	2.4
    	project[116] =	1.0	|	1	|	1.7
    	project[117] =	1.0	|	0.8	|	1.8
    	project[118] =	1.0	|	1.7	|	2.3
    	project[119] =	1.0	|	0.4	|	1.3
    	project[122] =	1.0	|	2.1	|	2.9
    	project[123] =	1.0	|	2.1	|	2.4
    	project[125] =	1.0	|	1.4	|	1.8
    	project[126] =	1.0	|	0.9	|	1.7
    	project[127] =	1.0	|	2	|	2.1
    	project[129] =	1.0	|	0.2	|	2.6
    	project[133] =	1.0	|	2.2	|	2.5
    	project[134] =	1.0	|	1.8	|	2.3
    	project[136] =	1.0	|	1.9	|	2.5
    	project[137] =	1.0	|	1.3	|	2.7
    	project[138] =	1.0	|	1.2	|	2.2
    	project[140] =	1.0	|	0.4	|	1.5
    	project[141] =	1.0	|	1.3	|	1.5
    	project[142] =	1.0	|	0.6	|	0.8
    	project[144] =	1.0	|	1.5	|	1.7
    	project[146] =	1.0	|	2.1	|	2
    	project[147] =	1.0	|	2.7	|	2.4
    	project[150] =	1.0	|	1.8	|	1.9
    	project[151] =	1.0	|	2.5	|	2.7
    	project[153] =	1.0	|	0.5	|	1.7
    	project[154] =	1.0	|	0.4	|	0.5
    	project[155] =	1.0	|	1.8	|	2.5
    	project[156] =	1.0	|	1.2	|	0.9
    	project[158] =	1.0	|	0.9	|	2.9
    	project[159] =	1.0	|	2.2	|	1.6
    	project[160] =	1.0	|	0.3	|	1.7
    	project[161] =	1.0	|	0.4	|	2.7
    	project[162] =	1.0	|	2.2	|	2.9
    	project[164] =	1.0	|	0.1	|	1.6
    	project[165] =	1.0	|	1.1	|	2.8
    	project[167] =	1.0	|	3	|	2.6
    	project[170] =	1.0	|	0.3	|	0.2
    	project[172] =	1.0	|	1.4	|	2.8
    	project[176] =	1.0	|	1.3	|	1.9
    	project[177] =	1.0	|	1	|	1.1
    	project[178] =	1.0	|	1.2	|	2.8
    	project[179] =	1.0	|	1	|	2
    	project[180] =	1.0	|	1.5	|	1.4
    	project[181] =	1.0	|	0.3	|	2.2
    	project[182] =	1.0	|	0.1	|	0.3
    	project[183] =	1.0	|	0.2	|	3
    	project[184] =	1.0	|	1.9	|	1.5
    	project[185] =	1.0	|	0.2	|	0.5
    	project[186] =	1.0	|	1.4	|	1.2
    	project[187] =	1.0	|	3	|	2.4
    	project[189] =	1.0	|	1.4	|	2
    	project[190] =	1.0	|	0.1	|	2.5
    	project[192] =	1.0	|	1.1	|	1.7
    	project[193] =	1.0	|	1.1	|	1.5
    	project[194] =	1.0	|	0.4	|	0.3
    	project[197] =	1.0	|	2.4	|	2.9
    	project[201] =	1.0	|	1.9	|	2.5
    	project[204] =	1.0	|	1.2	|	2
    	project[205] =	1.0	|	2.3	|	2.4
    	project[206] =	1.0	|	0.2	|	0.5
    	project[207] =	1.0	|	2.1	|	2
    	project[208] =	1.0	|	1.2	|	1.6
    	project[209] =	1.0	|	1.5	|	1.2
    	project[211] =	1.0	|	0.9	|	2.7
    	project[212] =	1.0	|	1.4	|	2.9
    	project[213] =	1.0	|	1.6	|	3
    	project[216] =	1.0	|	1.5	|	1.1
    	project[218] =	1.0	|	1.7	|	2
    	project[220] =	1.0	|	2.7	|	2.5
    	project[221] =	1.0	|	1.6	|	1.6
    	project[226] =	1.0	|	0.7	|	2.9
    	project[228] =	1.0	|	2.7	|	2.2
    	project[229] =	1.0	|	1.5	|	2.2
    	project[230] =	1.0	|	0.1	|	0.1
    	project[231] =	1.0	|	1.2	|	1.6
    	project[232] =	1.0	|	2.2	|	1.6
    	project[233] =	1.0	|	0.1	|	0.5
    	project[235] =	1.0	|	2	|	1.9
    	project[236] =	1.0	|	0.8	|	0.7
    	project[237] =	1.0	|	0.4	|	1.9
    	project[238] =	1.0	|	0.9	|	1.8
    	project[239] =	1.0	|	2.3	|	1.9
    	project[242] =	1.0	|	0.8	|	3
    	project[243] =	1.0	|	2.5	|	1.9
    	project[244] =	1.0	|	0.9	|	2.1
    	project[245] =	1.0	|	2	|	2.8
    	project[246] =	1.0	|	1.6	|	1.7
    	project[249] =	1.0	|	0.1	|	0.2
    


```python
"""
Problem 1 (c)
"""

## New Constraints 

### Variables constain the effected project numbers
CONDITIONAL_PROJECT_8 = 8
CONDITIONAL_PROJECT_9 = 9
SUBJECTIVE_PROJECT_10 = 10
PROJECT_IS_EXECUTED   = 1

### Requirement to execute construction project #10 if construction projects #8 and #9 are executed 
if  isExecuted[CONDITIONAL_PROJECT_8].x > 0.5 and isExecuted[CONDITIONAL_PROJECT_9].x > 0.5:
    m1.addConstr(isExecuted[SUBJECTIVE_PROJECT_10] == PROJECT_IS_EXECUTED)

### Reoptimize model
m1.update()
m1.optimize()

## PRINT THE MODEL
print("\n---------------------------------------------------------------------------------")
print("Model with requirement that project 10 is executed if project 8 and 9 are executed")
if m1.status == GRB.Status.OPTIMAL:
    print("\n*Optimal number of jobs that the project generated: " 
          + "{:,.4f}".format(m1.objVal) + " thousand jobs")
    print('\n**Below shows each project that was executed, their cost, and the jobs generated.')
    print('  Note that if a project in the set of Projects does not exist here,')
    print('  Then including it does not given an optimial solution. Therefore ignored.\n')
    print("\tProject\t| Executed\t| Cost\t| Jobs Generated")
    for project in Projects:
        if isExecuted[project].x > 0.5:
            print("\tproject[" + str(project) + "] =" 
                  + "\t"     + str(   isExecuted[project].x)
                  + "\t|\t" + str(         cost[project])
                  + "\t|\t" + str(jobsGenerated[project]))
            
    print(                  
    """
    Clearly, you can tell that project 10 now is executed but the value of the optimal
    solution has stayed the same.
    """
    )
    
```

    
    ---------------------------------------------------------------------------------
    Model with requirement that project 10 is executed if project 8 and 9 are executed
    
    *Optimal number of jobs that the project generated: 301.6000 thousand jobs
    
    **Below shows each project that was executed, their cost, and the jobs generated.
      Note that if a project in the set of Projects does not exist here,
      Then including it does not given an optimial solution. Therefore ignored.
    
    	Project	| Executed	| Cost	| Jobs Generated
    	project[0] =	1.0	|	2.1	|	1.9
    	project[1] =	1.0	|	2.5	|	2.4
    	project[2] =	1.0	|	0.8	|	1.6
    	project[5] =	1.0	|	2.2	|	2.7
    	project[8] =	1.0	|	2.4	|	2.3
    	project[9] =	1.0	|	2	|	2.8
    	project[10] =	1.0	|	2.2	|	1.1
    	project[14] =	1.0	|	0.7	|	1
    	project[15] =	1.0	|	0.3	|	0.2
    	project[16] =	1.0	|	1.7	|	1.6
    	project[17] =	1.0	|	2	|	2.7
    	project[18] =	1.0	|	1.4	|	1.8
    	project[19] =	1.0	|	0.6	|	2.7
    	project[22] =	1.0	|	1	|	1.9
    	project[23] =	1.0	|	2.5	|	1.9
    	project[25] =	1.0	|	2.3	|	2.3
    	project[28] =	1.0	|	0.3	|	2.2
    	project[29] =	1.0	|	1	|	1.4
    	project[31] =	1.0	|	2.6	|	2.1
    	project[32] =	1.0	|	0.3	|	1
    	project[34] =	1.0	|	0.1	|	0.4
    	project[35] =	1.0	|	1.7	|	1.6
    	project[36] =	1.0	|	0.5	|	1.5
    	project[37] =	1.0	|	2.3	|	2.5
    	project[38] =	1.0	|	0.4	|	1.2
    	project[39] =	1.0	|	2.8	|	3
    	project[40] =	1.0	|	0.1	|	0.1
    	project[41] =	1.0	|	0.3	|	2.7
    	project[43] =	1.0	|	1.4	|	1.6
    	project[45] =	1.0	|	0.1	|	2.7
    	project[47] =	1.0	|	1.3	|	2.3
    	project[52] =	1.0	|	0.8	|	1.7
    	project[53] =	1.0	|	1.7	|	2.9
    	project[54] =	1.0	|	1.1	|	2.5
    	project[57] =	1.0	|	0.9	|	2.3
    	project[58] =	1.0	|	2.6	|	2.5
    	project[59] =	1.0	|	2.7	|	2.7
    	project[62] =	1.0	|	0.2	|	2.1
    	project[63] =	1.0	|	1.1	|	0.8
    	project[65] =	1.0	|	0.5	|	2.4
    	project[66] =	1.0	|	1.4	|	2.5
    	project[68] =	1.0	|	0.6	|	2.5
    	project[70] =	1.0	|	2	|	2.7
    	project[72] =	1.0	|	0.3	|	2.9
    	project[73] =	1.0	|	0.6	|	1.4
    	project[75] =	1.0	|	1.9	|	1.7
    	project[76] =	1.0	|	1.8	|	2
    	project[77] =	1.0	|	0.2	|	0.6
    	project[78] =	1.0	|	1.2	|	1.5
    	project[80] =	1.0	|	1.9	|	2.5
    	project[82] =	1.0	|	0.1	|	1.4
    	project[83] =	1.0	|	0.1	|	1.6
    	project[86] =	1.0	|	0.9	|	1.9
    	project[87] =	1.0	|	0.6	|	3
    	project[88] =	1.0	|	1.9	|	2.5
    	project[89] =	1.0	|	2.9	|	2.6
    	project[90] =	1.0	|	1.4	|	1.6
    	project[91] =	1.0	|	0.3	|	1
    	project[92] =	1.0	|	0.1	|	0.3
    	project[93] =	1.0	|	1.5	|	2.8
    	project[94] =	1.0	|	0.2	|	2.1
    	project[95] =	1.0	|	0.3	|	2.7
    	project[98] =	1.0	|	1.1	|	2
    	project[102] =	1.0	|	0.1	|	2.3
    	project[103] =	1.0	|	2.2	|	2.8
    	project[104] =	1.0	|	1.3	|	1.5
    	project[105] =	1.0	|	2.1	|	1.6
    	project[107] =	1.0	|	1.1	|	2.6
    	project[109] =	1.0	|	1.9	|	1.6
    	project[114] =	1.0	|	0.5	|	0.6
    	project[115] =	1.0	|	2.3	|	2.4
    	project[116] =	1.0	|	1	|	1.7
    	project[117] =	1.0	|	0.8	|	1.8
    	project[118] =	1.0	|	1.7	|	2.3
    	project[119] =	1.0	|	0.4	|	1.3
    	project[122] =	1.0	|	2.1	|	2.9
    	project[123] =	1.0	|	2.1	|	2.4
    	project[125] =	1.0	|	1.4	|	1.8
    	project[126] =	1.0	|	0.9	|	1.7
    	project[127] =	1.0	|	2	|	2.1
    	project[129] =	1.0	|	0.2	|	2.6
    	project[133] =	1.0	|	2.2	|	2.5
    	project[134] =	1.0	|	1.8	|	2.3
    	project[136] =	1.0	|	1.9	|	2.5
    	project[137] =	1.0	|	1.3	|	2.7
    	project[138] =	1.0	|	1.2	|	2.2
    	project[140] =	1.0	|	0.4	|	1.5
    	project[141] =	1.0	|	1.3	|	1.5
    	project[142] =	1.0	|	0.6	|	0.8
    	project[144] =	1.0	|	1.5	|	1.7
    	project[146] =	1.0	|	2.1	|	2
    	project[147] =	1.0	|	2.7	|	2.4
    	project[150] =	1.0	|	1.8	|	1.9
    	project[151] =	1.0	|	2.5	|	2.7
    	project[153] =	1.0	|	0.5	|	1.7
    	project[154] =	1.0	|	0.4	|	0.5
    	project[155] =	1.0	|	1.8	|	2.5
    	project[156] =	1.0	|	1.2	|	0.9
    	project[158] =	1.0	|	0.9	|	2.9
    	project[159] =	1.0	|	2.2	|	1.6
    	project[160] =	1.0	|	0.3	|	1.7
    	project[161] =	1.0	|	0.4	|	2.7
    	project[162] =	1.0	|	2.2	|	2.9
    	project[164] =	1.0	|	0.1	|	1.6
    	project[165] =	1.0	|	1.1	|	2.8
    	project[167] =	1.0	|	3	|	2.6
    	project[170] =	1.0	|	0.3	|	0.2
    	project[172] =	1.0	|	1.4	|	2.8
    	project[176] =	1.0	|	1.3	|	1.9
    	project[177] =	1.0	|	1	|	1.1
    	project[178] =	1.0	|	1.2	|	2.8
    	project[179] =	1.0	|	1	|	2
    	project[180] =	1.0	|	1.5	|	1.4
    	project[181] =	1.0	|	0.3	|	2.2
    	project[182] =	1.0	|	0.1	|	0.3
    	project[183] =	1.0	|	0.2	|	3
    	project[184] =	1.0	|	1.9	|	1.5
    	project[185] =	1.0	|	0.2	|	0.5
    	project[186] =	1.0	|	1.4	|	1.2
    	project[187] =	1.0	|	3	|	2.4
    	project[189] =	1.0	|	1.4	|	2
    	project[190] =	1.0	|	0.1	|	2.5
    	project[192] =	1.0	|	1.1	|	1.7
    	project[193] =	1.0	|	1.1	|	1.5
    	project[194] =	1.0	|	0.4	|	0.3
    	project[197] =	1.0	|	2.4	|	2.9
    	project[201] =	1.0	|	1.9	|	2.5
    	project[204] =	1.0	|	1.2	|	2
    	project[205] =	1.0	|	2.3	|	2.4
    	project[206] =	1.0	|	0.2	|	0.5
    	project[207] =	1.0	|	2.1	|	2
    	project[208] =	1.0	|	1.2	|	1.6
    	project[209] =	1.0	|	1.5	|	1.2
    	project[211] =	1.0	|	0.9	|	2.7
    	project[212] =	1.0	|	1.4	|	2.9
    	project[213] =	1.0	|	1.6	|	3
    	project[216] =	1.0	|	1.5	|	1.1
    	project[218] =	1.0	|	1.7	|	2
    	project[220] =	1.0	|	2.7	|	2.5
    	project[221] =	1.0	|	1.6	|	1.6
    	project[226] =	1.0	|	0.7	|	2.9
    	project[228] =	1.0	|	2.7	|	2.2
    	project[229] =	1.0	|	1.5	|	2.2
    	project[230] =	1.0	|	0.1	|	0.1
    	project[231] =	1.0	|	1.2	|	1.6
    	project[233] =	1.0	|	0.1	|	0.5
    	project[235] =	1.0	|	2	|	1.9
    	project[236] =	1.0	|	0.8	|	0.7
    	project[237] =	1.0	|	0.4	|	1.9
    	project[238] =	1.0	|	0.9	|	1.8
    	project[239] =	1.0	|	2.3	|	1.9
    	project[242] =	1.0	|	0.8	|	3
    	project[243] =	1.0	|	2.5	|	1.9
    	project[244] =	1.0	|	0.9	|	2.1
    	project[245] =	1.0	|	2	|	2.8
    	project[246] =	1.0	|	1.6	|	1.7
    	project[249] =	1.0	|	0.1	|	0.2
    
        Clearly, you can tell that project 10 now is executed but the value of the optimal
        solution has stayed the same.
        
    


```python
"""
Problem 2 (a)
"""

# EXCEL READ ==================================================================

# Excel file and sheet name
fileXLS  = "OptiCoffee.xlsx"
sheetXLS = "Information"

doc = opxl.load_workbook(fileXLS)


# Read in single value variables ----------------------------------------------

## First row num less one
rowNum = 9 - 1

## s: Marginal costs of stockout backlog [thousands of USD/Ton]
s = doc[sheetXLS].cell(row = rowNum + 1, column = 2).value

## h: Hiring and training costs [thousands of USD/worker]
h = doc[sheetXLS].cell(row = rowNum + 2, column = 2).value

## f: Layoff costs [thousands of USD/worker]
f = doc[sheetXLS].cell(row = rowNum + 3, column = 2).value

## k: Labour hours required per ton produced [hrs/Ton]
k = doc[sheetXLS].cell(row = rowNum + 4, column = 2).value

## w: Regular time cost [thousands of UDS/worker/hr]
w = doc[sheetXLS].cell(row = rowNum + 5, column = 2).value

## o: Overtime cost [thousands of UDS/hr]
o = doc[sheetXLS].cell(row = rowNum + 6, column = 2).value

## c: Subcontarcting costs [thousands of UDS/Ton]
c = doc[sheetXLS].cell(row = rowNum + 7, column = 2).value

## a: Initial inventory [Ton]
a = doc[sheetXLS].cell(row = rowNum + 8, column = 2).value

## b: Initial workforce [worker]
b = doc[sheetXLS].cell(row = rowNum + 9, column = 2).value

## e: Initial backlog [worker]
e = doc[sheetXLS].cell(row = rowNum + 10, column = 2).value


# Read in Multivalued Monthly data --------------------------------------------

## First row num less one
rowNum = 3 - 1
firstCol = 1

## Number of periods in the sample
numPeriods = 12

## T: Set of months or periods
T = [doc[sheetXLS].cell(row = rowNum + 1, column = firstCol + col).value for col in range(1, numPeriods + 1)]

## d: Demand [Ton]
d = {T[col - 1]:doc[sheetXLS].cell(row = rowNum + 2, column = firstCol + col).value for col in range(1, numPeriods + 1)}

## p: Unit production costs [thousands of USD/Ton]
p = {T[col - 1]:doc[sheetXLS].cell(row = rowNum + 3, column = firstCol + col).value for col in range(1, numPeriods + 1)}

## i: Inventory holding costs [thousands of USD/Ton]
i = {T[col - 1]:doc[sheetXLS].cell(row = rowNum + 4, column = firstCol + col).value for col in range(1, numPeriods + 1)}

## n: Number of regular working hours [hrs]
n = {T[col - 1]:doc[sheetXLS].cell(row = rowNum + 5, column = firstCol + col).value for col in range(1, numPeriods + 1)}

## m: Maximum number of overtime hours per worker [hrs/worker]
m = {T[col - 1]:doc[sheetXLS].cell(row = rowNum + 6, column = firstCol + col).value for col in range(1, numPeriods + 1)}


# OPTIMIZATION MODEL ==========================================================

## Create the model -----------------------------------------------------------
m2 = Model('OptiCoffee')
m2.setParam(GRB.Param.OutputFlag, 0)


## Decision Variables ---------------------------------------------------------

W = {t:m2.addVar(name = "W["+str(t)+"]", vtype = GRB.INTEGER)    for t in T}
O = {t:m2.addVar(name = "O["+str(t)+"]", vtype = GRB.CONTINUOUS) for t in T}
H = {t:m2.addVar(name = "H["+str(t)+"]", vtype = GRB.INTEGER)    for t in T}
F = {t:m2.addVar(name = "F["+str(t)+"]", vtype = GRB.INTEGER)    for t in T}
P = {t:m2.addVar(name = "P["+str(t)+"]", vtype = GRB.CONTINUOUS) for t in T}
I = {t:m2.addVar(name = "I["+str(t)+"]", vtype = GRB.CONTINUOUS) for t in T}
S = {t:m2.addVar(name = "S["+str(t)+"]", vtype = GRB.CONTINUOUS) for t in T}
C = {t:m2.addVar(name = "C["+str(t)+"]", vtype = GRB.CONTINUOUS) for t in T}


## Objective Function ---------------------------------------------------------

### Regular Time Labor Cost
RTLC = quicksum(n[t] * w * W[t] for t in T)

### Overtime Labor Cost
OTLC = quicksum(o * O[t]        for t in T)

### Cost of Hiring
HC   = quicksum(h * H[t]        for t in T)

### Cost of Layoffs
FC   = quicksum(f * F[t]        for t in T)

### Cost of Holding Inventory
HIC  = quicksum(i[t] * I[t]     for t in T)

### Cost of Stocking Out
CSO  = quicksum(s * S[t]        for t in T)

### Production Costs
PC   = quicksum(p[t] * P[t]     for t in T)

### Sub-contracting cost
SC   = quicksum(c * C[t]        for t in T)

### Initilize the Actual Objective Function
FO = (RTLC + OTLC + HC + FC + HIC + CSO + PC + SC)

### Set the Objective Function to m2 Model
m2.setObjective(FO, GRB.MINIMIZE)


# CONSTRAINTS =================================================================

## Workforce, hiring, and layoffs
m2.addConstr (W[1] == b + H[1] - F[1])
m2.addConstrs(W[t] == W[t - 1] + H[t] - F[t] for t in T if t is not T[0])

## Capacity Constraints
m2.addConstrs(k * P[t] <= n[t] * W[t] + O[t] for t in T)

## Inventory Balance Constraints
m2.addConstr (a + P[1] + C[1] - e               == d[1] + I[1] - S[1])
m2.addConstrs(I[t - 1] + P[t] + C[t] - S[t - 1] == d[t] + I[t] - S[t] 
              for t in T if t is not T[0])

## Overtime Constraints
m2.addConstrs(O[t] <= m[t] * W[t] for t in T)

## Additional Constraints -----------------------------------------------------

FIRST_MONTH = 1

### Initial Inventory
m2.addConstr(I[FIRST_MONTH] == a)

### Initial Workforce
m2.addConstr(W[FIRST_MONTH] == b)

### Initial Backlog
m2.addConstr(S[FIRST_MONTH] == e)


## Optimize the model ---------------------------------------------------------
m2.update()
m2.optimize()


# PRINT SOLUTION ==============================================================

## Print to Console -----------------------------------------------------------
if m2.status == GRB.OPTIMAL:
    print('\n============= PROBLEM 2.1 =============')
    print('\nOptimal/Minimized Cost: %4f' % m2.objVal)
    print('\nDecision Variables ----------------------')
    for var in m2.getVars():
        print('%s\t%g' % (var.varName, var.x))

```

    
    ============= PROBLEM 2.1 =============
    
    Optimal/Minimized Cost: 39363.960000
    
    Decision Variables ----------------------
    W[1]	7
    W[2]	6
    W[3]	10
    W[4]	-0
    W[5]	6
    W[6]	-0
    W[7]	5
    W[8]	0
    W[9]	10
    W[10]	-0
    W[11]	-0
    W[12]	-0
    O[1]	0
    O[2]	0
    O[3]	0
    O[4]	0
    O[5]	32
    O[6]	0
    O[7]	24
    O[8]	0
    O[9]	0
    O[10]	0
    O[11]	0
    O[12]	0
    H[1]	0
    H[2]	0
    H[3]	4
    H[4]	0
    H[5]	6
    H[6]	0
    H[7]	5
    H[8]	0
    H[9]	10
    H[10]	0
    H[11]	0
    H[12]	0
    F[1]	-0
    F[2]	1
    F[3]	-0
    F[4]	10
    F[5]	0
    F[6]	6
    F[7]	0
    F[8]	5
    F[9]	-0
    F[10]	10
    F[11]	0
    F[12]	-0
    P[1]	522
    P[2]	534
    P[3]	960
    P[4]	0
    P[5]	592
    P[6]	0
    P[7]	462
    P[8]	0
    P[9]	917
    P[10]	0
    P[11]	0
    P[12]	0
    I[1]	100
    I[2]	0
    I[3]	403
    I[4]	0
    I[5]	0
    I[6]	0
    I[7]	0
    I[8]	0
    I[9]	0
    I[10]	0
    I[11]	0
    I[12]	0
    S[1]	80
    S[2]	0
    S[3]	0
    S[4]	116
    S[5]	0
    S[6]	0
    S[7]	0
    S[8]	452
    S[9]	0
    S[10]	422
    S[11]	934
    S[12]	1530
    C[1]	0
    C[2]	0
    C[3]	0
    C[4]	0
    C[5]	0
    C[6]	475
    C[7]	0
    C[8]	0
    C[9]	0
    C[10]	0
    C[11]	0
    C[12]	0
    


```python
"""
Problem 2 (b) Coding Portion
"""
        
## Write to Excel -------------------------------------------------------------

import xlwt
from xlwt import Workbook

### Create the workbook
wb = Workbook()

### Add the sheet name
s1 = wb.add_sheet('OptiCoffeeOutput')

### Write the column headers
s1.write(0, 0, 'Period')
s1.write(0, 1, 'Demand')
s1.write(0, 2, 'Production')
s1.write(0, 3, 'SubContracting')
s1.write(0, 4, 'Backlogs')
s1.write(0, 5, 'Inventory')
s1.write(0, 6, 'Workforce')
s1.write(0, 7, 'Hirings')
s1.write(0, 8, 'Layoffs')
s1.write(0, 9, 'OvertimeHours')

### Print the Values
row = 1
for t in T:
    s1.write(row, 0, t)
    s1.write(row, 1, d[t])
    s1.write(row, 2, P[t].x)
    s1.write(row, 3, C[t].x)
    s1.write(row, 4, S[t].x)
    s1.write(row, 5, I[t].x)
    s1.write(row, 6, W[t].x)
    s1.write(row, 7, H[t].x)
    s1.write(row, 8, F[t].x)
    s1.write(row, 9, O[t].x)
    row += 1

### Save the file
wb.save("OptiCoffee Analysis Output.xls")

```


```python
"""
Problem 2 (c) 
>> PLEASE SEE NOTE AT END <<
"""

## Only 4 production periods
periodLimit = 4

## Count if production is greater than 0 in a given period, store in binary list.
## sum of the output binary numbers must be less or equal to than the limit (4)
m2.addConstr(sum(P[t].x > 0 for t in T) <= periodLimit ) # <- This does not run!

## Optimize the model ---------------------------------------------------------
m2.update()
m2.optimize()


# PRINT SOLUTION ==============================================================

## Print to Console -----------------------------------------------------------
if m2.status == GRB.OPTIMAL:
    print('\n============= PROBLEM 2.2 =============')
    print('\nOptimal/Minimized Cost: %4f' % m2.objVal)
    print('\nDecision Variables ----------------------')
    for var in m2.getVars():
        print('%s\t%g' % (var.varName, var.x))


## Write to Excel -------------------------------------------------------------

import xlwt
from xlwt import Workbook

### Create the workbook
wb = Workbook()

### Add the sheet name
s1 = wb.add_sheet('OptiCoffeeOutput')

### Write the column headers
s1.write(0, 0, 'Period')
s1.write(0, 1, 'Demand')
s1.write(0, 2, 'Production')
s1.write(0, 3, 'SubContracting')
s1.write(0, 4, 'Backlogs')
s1.write(0, 5, 'Inventory')
s1.write(0, 6, 'Workforce')
s1.write(0, 7, 'Hirings')
s1.write(0, 8, 'Layoffs')
s1.write(0, 9, 'OvertimeHours')

### Print the Values
row = 1
for t in T:
    s1.write(row, 0, t)
    s1.write(row, 1, d[t])
    s1.write(row, 2, P[t].x)
    s1.write(row, 3, C[t].x)
    s1.write(row, 4, S[t].x)
    s1.write(row, 5, I[t].x)
    s1.write(row, 6, W[t].x)
    s1.write(row, 7, H[t].x)
    s1.write(row, 8, F[t].x)
    s1.write(row, 9, O[t].x)
    row += 1

### Save the file
wb.save("OptiCoffee Analysis Output Period Limit 2(c).xls")


"""
This problem would run and if the new constraint worked properly.
Essentially, the goal was to add a constraint with the following logic:
    Ensure that the count of production periods are less than the 
    production period limit of 4. However, it seems that this count
    operation does not work well with Gurobi's algorithm. I firmly believe
    If the logic was translated, the optimal solution would meet the 
    problem's requirement
"""

```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-7-5e027cc59b46> in <module>
         55     s1.write(row, 0, t)
         56     s1.write(row, 1, d[t])
    ---> 57     s1.write(row, 2, P[t].x)
         58     s1.write(row, 3, C[t].x)
         59     s1.write(row, 4, S[t].x)
    

    src\gurobipy\var.pxi in gurobipy.Var.__getattr__()
    

    src\gurobipy\var.pxi in gurobipy.Var.getAttr()
    

    src\gurobipy\attrutil.pxi in gurobipy.__getattr()
    

    AttributeError: Unable to retrieve attribute 'x'



```python

```
