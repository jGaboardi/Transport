# -*- coding: utf-8 -*-
# The Traveling Salesperson Problem
# Branch and Bound Method
# This script creates a linear programming file to be read into an optimizer.
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Developed by:  James D. Gaboardi, MSGIS
#                08/2015
#                © James Gaboardi



#    1. IMPORTS
# Other imports may be necessary for matrix creation and manipulation 
import numpy as np


#    2. DEFINED FUNCTIONS
# Objective Function 
def get_objective_function_TSP_BB():
    outtext = ' obj: '
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += str(Cij[i,j]) + 'x' + str(i+1) + '_' + str(j+1) + ' + '
        outtext += temp + ' \n      '
    outtext = outtext[:-11] + ' \n'
    return outtext    

# Add Constraints
# Add Assignment Constraints by summed rows x_ij
def get_summed_rows():
    counter = 0
    outtext = ''
    for i in range(rows):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for j in range(cols):
            temp += 'x' + str(j+1) + '_' + str(i+1) + ' + '
        outtext += temp[:-2] + '= 1\n'
    return outtext
#Add Assignment Constraints by summed columns x_ji  
def get_summed_cols():
    counter = 9
    outtext = ''
    for j in range(cols):
        counter = counter + 1
        temp = ' c' + str(counter) + ':  '
        for i in range(rows):
            temp += 'x' + str(j+1) + '_' + str(i+1) + ' + '
        outtext += temp[:-2] + '= 1\n'
    return outtext
      
# Declaration of Bounds
def get_bounds():
    outtext = ''
    for i in range(rows):
        temp = ''
        for j in range(cols):
            temp += ' 0 <= x' + str(i+1) + '_' + str(j+1) + ' <= 1\n'
        outtext += temp    
    return outtext
    
# Declaration of Decision Variables (form can be: Binary, Integer, etc.)
# In this case decision variables are General.
def get_decision_variables():
    outtext = ''
    for i in range(1, rows+1):
        temp = ''
        for j in range(1, cols+1):
            temp += ' x' + str(i) + '_' + str(j) + '\n'
        outtext += temp
    return outtext


#    3. DATA READS & VARIABLE DECLARATION
# Cost Matrix
Cij = np.random.randint(1, 5, 81)
Cij = Cij.reshape(9,9)
rows, cols = Cij.shape
# Cost Sum
CijSum = np.sum(Cij)

tour_nodes = range(len(Cij[0]))

    
#    4. START TEXT FOR .lp FILE
# Declaration of Objective Function
text = "The Traveling Salesperson Problem\n"
text += "Branch and Bound Method\n"
text += "'''\n"
text += 'Minimize\n'          
text += get_objective_function_TSP_BB()
text += '\n'
# Declaration of Constraints
text += 'Subject To\n'
text += get_summed_rows()
text += '\n'
text += get_summed_cols()
text += '\n'
# Declaration of Bounds
text += 'Bounds\n' 
text += get_bounds()
text += '\n'
# Declaration of Decision Variables form: Binaries
text += 'Binaries\n'
#text += get_decision_variables()
text += '\n'
text += 'End\n'
text += "'''\n"
text += "© James Gaboardi, 2015"                


#   5. CREATE & WRITE .lp FILE TO DISK
# Fill path name  --  File name must not have spaces.
outfile = open('name.lp', 'w')
outfile.write(text)
outfile.close()