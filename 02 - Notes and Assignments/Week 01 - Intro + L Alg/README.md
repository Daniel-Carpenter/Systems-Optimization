# Week 1

## Intro to Operations Research

### Types of Analytics Overview
Analytics Type|Description
-|-
`Descriptive`     | insight into past events, using historical data
`Predictive`      | provides insight on what will happen in the
`Prescriptive`    | helps with decision making by providing actionable advice

### Classifications of optimization models
Option 1|vs|Option 2
-|-|-
`Static` (*fixed*)    |*vs.*| `dynamic` (*can be updated*)
`Linear`              |*vs.*| `nonlinear`
`Integer`             |*vs*.| `noninteger`
`Deterministic` (is a vacuum) |*vs*.| `stochastic` (many unkowns)

* *We will be using `static`, `linear`, `non-integer`, `deterministic` models*

### `Prescriptive Analytics` (*LP Optimization*) ***in General***

#### In order to optimize anything (*via `linear programming`*), you must have:
Step| Name                    | Description               |Example
----|-------------------------|---------------------------|----
1   | `Input Data`            | Form of sets or parameters| Weights in stock
2   | `Descision variables`   | *Solution*                | Weights in stock
3   | `Constraints`           | *Limiting factor*         | Portfolio = 100%, total dollars invested <= amt. you own, etc.
4   | `Objective Function`    | *Maximize` or `minimize* a function  | Expected Return


### `Linear Programming` ***Example***
Step| Name                    | Example               
----|-------------------------|----
1   | `Input Data`            | <img src = Images/Exam1.1-1.jpg width = 600>
2   | `Descision variables`   | <img src = Images/Exam1.1-2.jpg width = 600>
3   | `Constraints`           | <img src = Images/Exam1.1-3.jpg width = 600>
4   | `Objective Function`    | <img src = Images/Exam1.1-4.jpg width = 600>



---

## Linear Algebra

### Determine if two matrices can be multiplied together (defined)
<img src = "Images/mmultDefined.png" width = 350>

Topic|Example
-|-
Dot product ***in general*** | <img src = "Images/dotProd.png" width = 550> <br>
Go *from* System of Linear Equations *to* Matrix Notation | <img src = "Images/fromSysToMatrixNotation.png" width = 350> <br> 
Solve for `v` from inverse | <img src = "Images/solveXY.png" width = 350> <br> 
 Find determent of `2x2 matrix`| <img src = "Images/2x2Deter.png" width = 350> <br> 
 `Cofactor` of 2x2 matrix | <img src = "Images/cofactor.png" width = 150> <br> 
 Inverse of 2x2 matrix | <img src = "Images/inverse2x2.png" width = 350> <br> 

<br>

### `Solve System of Linear Equations`
Step|Description|Example
-|-|-
1 - 4   |How to ***solve*** a `system of linear equations` with `Gaussian Elimination`| <img src = "Images/linAlgSolve.jpg" width = 550>

### Types of `Solutions to Linear Equations`
Solution Type|Description|Example
-|-|-
`One Solution`    | ***Intersection of two lines*** | <img src = "Images/linAlg1Soln.jpg" width = 300>
`No Solution`     | ***Parallel Lines*** |<img src = "Images/linAlgNoSoln.jpg" width = 300>
`Infinite Solutions` | ***Same Line***, `Linear Dependence`|<img src = "Images/linAlgInfSoln.jpg" width = 300>


### Resources
* [Main Calculator](https://matrixcalc.org/en/)
* [Linear Algebra Full Notes](https://sooners-my.sharepoint.com/personal/danielcarpenter_ou_edu/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fdanielcarpenter%5Fou%5Fedu%2FDocuments%2F1%2E%20School%2F1%2E%20University%20of%20Oklahoma%2F1%20%2D%20Undergraduate%20%28Economics%20and%20Finance%29%2F4%2E%20Senior%2FSPRING%202020%2FLinear%20Alg%2E%20%28MATH%2D3333%2D001%29%2FLecture%20Notes%2FCourse%20Notes%20Binder%2Epdf&parent=%2Fpersonal%2Fdanielcarpenter%5Fou%5Fedu%2FDocuments%2F1%2E%20School%2F1%2E%20University%20of%20Oklahoma%2F1%20%2D%20Undergraduate%20%28Economics%20and%20Finance%29%2F4%2E%20Senior%2FSPRING%202020%2FLinear%20Alg%2E%20%28MATH%2D3333%2D001%29%2FLecture%20Notes)