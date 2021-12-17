# Week 10 - Data Envelope Analysis

## Overview of `DEA`
* Understand if you are efficient compared to your peers
* I.e. Measures the relative efficiency of organizational units

## Determining whether `inefficient` or `efficient`

### `Terminology` for Efficiencies
Term        | Description
------------|-------------
`Efficient` | `Max` value obtained among each value of the independant variable
Inefficient | `Minimum` value obtained among each value of the independant variable


<br> <img src = "Images/minMax.png" width = 400>

---
<br>

## `Setup` for Data Envelope Analysis


### `1` - Determine the following:

n | Step        | Description | Example
--|-------------|-------------|---------
1 | `Sets`      | Objects used | <img src = "Images/sets.png" width = 450>
2 | `Parameters`| Amount of input/ouput and indices | <img src = "Images/param.png" width = 450>
3 | `Variables` | ***lambdas***, ***phi*** * | <img src = "Images/vars.png" width = 450>
4 | `Objective Function` | Maximize `phi` | <img src = "Images/obj.png" width = 450>
5 | `Constraints` | One for each constraint. Phi is unconstrained. | <img src = "Images/cons.png" width = 450>

#### Notes on Variables `phi` and `lambda`
Variable Name | Description
--------------|-------------
***lambdas*** | percentage / fraction given to a person (set) 
***phi***     | Proportional change of the output needed to achieve efficiency

#### What if you need to add another `set` and `parameter` (whether input or output)?
* Add another input or output parameter
* Add associated constraint, using the original `<=` `(input)` or `>=` `(output)` constraint as template
* <img src = "Images/New Input Var.jpg" width = 550>

### `2` - Establish Actual Model
* Use Gurobi-Python or Excel to maximize phi s.t. constraints