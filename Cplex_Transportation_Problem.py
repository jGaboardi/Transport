# -*- coding: utf-8 -*-


'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''

# Building and Optimizing The Transportation Problem in
#        Python/cplex.CPLEX

import numpy as np
import cplex as cp
import time
t1 = time.time()
np.random.seed(352)

def Cplex_TransProb(Cij, Si, Dj):
    # Reshape Data
    
    Cij = Cij.reshape(matrix_rows,matrix_cols)
    Si = Si.reshape(matrix_rows,1)
    Dj = Dj.reshape(matrix_cols,1)

    # Indices & Variable Names
    supply_nodes = len(Cij)
    demand_nodes = len(Cij[0])
    supply_nodes_range = range(len(Cij))
    demand_nodes_range = range(len(Cij[0]))
    all_nodes_len = len(Cij) * len(Cij[0])
    ALL_nodes_range = range(all_nodes_len)
    
    x = 'x'
    desc_var = []
    for i in supply_nodes_range:
        for j in demand_nodes_range:
             desc_var.append(x + str(i+10001) + '_' + str(j+10001))
    descision_var = np.array(desc_var)
    descision_var = descision_var.reshape(matrix_rows,matrix_cols)
   
    # Create Model
    m = cp.Cplex()
    m.set_problem_name('\n -- The Transportation Problem -- ')   # Problem Name
    print m.get_problem_name()
    m.set_problem_type(m.problem_type.LP)         # Problem Type  ==>  Linear Programming
    m.parameters.emphasis.mip.set(2)              # Set MIP Emphasis to '2' --> Optimal
    print m.parameters.get_changed()
    print '\nProblem Type\n    ' + str(m.problem_type[m.get_problem_type()])
    m.objective.set_sense(m.objective.sense.minimize)  # ==>  Minimize
    print 'Objective Sense\n    ' + str(m.objective.sense[m.objective.get_sense()])
    
    # Add Client Decision Variables
    m.variables.add(names = [desc_var[i] for i in ALL_nodes_range],  
                            obj = [Cij[i][j] for i in supply_nodes_range 
                                             for j in demand_nodes_range],
                            types = ['C'] * all_nodes_len)

    # Add Supply Constraints
    for orig in supply_nodes_range:      
        supply_constraints = cp.SparsePair(ind = [descision_var[orig][dest] 
                                                for dest in demand_nodes_range],                           
                                                val = [1] * demand_nodes)
        m.linear_constraints.add(lin_expr = [supply_constraints],                 
                                    senses = ['L'], 
                                    rhs = Si[orig])
    
    # Add Demand Constraints
    for orig in demand_nodes_range:       
        demand_constraints = cp.SparsePair(ind = [descision_var[dest][orig] 
                                                for dest in supply_nodes_range],                           
                                                val = [1] * supply_nodes)
        m.linear_constraints.add(lin_expr = [demand_constraints],                 
                                    senses = ['G'], 
                                    rhs = Dj[orig])

    #  Optimize and Print Results
    m.solve()
    t2 = round(time.time()-t1,3)
    solution = m.solution
    
    print '******************************************************************************'
    print '| From SUPPLY Facility to DEMAND Facility x(Si)_(Dj) shipping # of units  '
    print '| ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓'
    print '|'
    selected = {}
    Closed = []
    for f in desc_var:
        if solution.get_values(f) > 0:
            units = '%i' % solution.get_values(f)
            selected[f] = solution.get_values(f)
            print '|  Supply Facility #', f[1:6], 'is shipping', units, \
                                                'units to Demand Facility #', f[-5:]
        else:
            Closed.append([f[1:6], f[-5:]])
    print '******************************************************************************' 
    print 'Total cost                   = ', solution.get_objective_value()
    print 'Solution status              = ', solution.get_status(), ':', \
                                        solution.status[solution.get_status()]
    print 'Supply Facilities             = ', len(Si)
    print 'Total Supply Units           = ', Si.sum()
    print 'Demand Facilities             = ', len(Dj)
    print 'Total Demand Units           = ', Dj.sum()
    print 'Total Potential Combinations = ', len(Si)*len(Dj)
    print 'Actual Combinations          = ', len(selected) 
    print 'Real Time to Optimize (sec.) = ', t2, '\n\n'
    m.write('pathCPLEX_TransSimplex.lp')

#########################################################################################
# Data can be read-in or simulated
    
Supply = np.random.randint(50,200,5)   # Vector of Units Supplied
Demand = np.random.randint(25,30,7)    # Vector of Units Demanded

matrix_rows = len(Supply)                # Supply (i) x Demand (j)
matrix_cols = len(Demand)

Cost_Matrix = np.random.randint(3, 
                                50, 
                                matrix_rows*matrix_cols)

# Call Function   
Cplex_TransProb(Cij=Cost_Matrix, Si=Supply, Dj=Demand)

print '******************************************************************************'
print '  --  The Transportation Simplex with CPLEX --'
print '\n James Gaboardi, 2016'
print '******************************************************************************\n\n'