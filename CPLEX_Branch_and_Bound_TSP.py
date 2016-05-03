# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Building and Optimizing a Branch and Bound Directed 
#        Traveling Salesperson problem in Python/CPLEX
#
'''
Adapted from:

Bertsimas, D., and J. N. Tsitsiklis 
    Ch. 11
    p. 488
    1997 
    Introduction to Linear Optimization 
    Nashua, NH: Athena Scientific
'''

import numpy as np
import cplex as cp
import time
t1 = time.time()
np.random.seed(352)

def CPLEX_TSP(nodes, min_cost, max_cost):
    #     1. Read In (or Create)Data
    # CREATE
    # Cost Matrix
    Cij = np.random.randint(min_cost, max_cost, nodes**2)
    Cij = Cij.reshape(nodes,nodes)
    # Cost Sum
    CijSum = np.sum(Cij)
    
    tour_nodes = range(len(Cij[0]))
    
    #       2. Create Model, Set MIP Focus, Add Variables, & Update Model
    m = cp.Cplex()                                      # Create model
    m.parameters.emphasis.mip.set(2)                    # Set MIP emphasis to '2' --> Optimal
    m.set_problem_type(m.problem_type.LP)               # Set problem type
    m.objective.set_sense(m.objective.sense.minimize)   # Objective Function Sense  ==>  Minimize
    
    # Tour Index
    desc_var = []
    for orig in tour_nodes:
        desc_var.append([])
        for dest in tour_nodes:
            desc_var[orig].append('x'+str(orig+1)+'_'+str(dest+1))
    # Add Tour Variables
    m.variables.add(names = [desc_var[i][j] for i in tour_nodes for j in tour_nodes], 
                        lb = [0] * nodes**2, 
                        ub = [1] * nodes**2,
                        obj = [Cij[i][j] for i in tour_nodes for j in tour_nodes], 
                        types = ['B'] * nodes**2)
    
    # Add IJ Assignment Constraints
    for orig in tour_nodes:       
        ij_assignment_constraints = cp.SparsePair(ind = [desc_var[orig][dest] 
                                            for dest in tour_nodes],                           
                                            val = [1] * len(Cij[0]))
        m.linear_constraints.add(lin_expr = [ij_assignment_constraints],                 
                                senses = ['E'], 
                                rhs = [1]);
    # Add JI Assignment Constraints
    for orig in tour_nodes:       
        ji_assignment_constraints = cp.SparsePair(ind = [desc_var[dest][orig] 
                                            for dest in tour_nodes],                           
                                            val = [1] * len(Cij[0]))
        m.linear_constraints.add(lin_expr = [ji_assignment_constraints],                 
                                senses = ['E'], 
                                rhs = [1]);
    
    #       5. Optimize and Print Results
    try:
        m.solve()
        
    
    
    except Exception as e:
        print e
     
    solution = m.solution   
    t2 = time.time()-t1
    print '**********************************************************************'
    print ' Solution status    = ' , solution.get_status(), ':', solution.status[solution.get_status()]
    print ' Nodes on Path ---------------------------- ', len(Cij)
    print ' Objective Value -------------------------- ', solution.get_objective_value()
    print ' Avg. Value / Arc ------------------------- ', float(solution.get_objective_value())/float(len(Cij))
    print ' Total Network Travel Cost ---------------- ', CijSum
    print ' Real Time to Optimize (sec.) ------------- ', t2
    print ' '
    print ' Cij ', len(Cij)*' ↓' , '        Tour by Node Order'
    NoP = []
    for row in desc_var:
        for node in row:
            if solution.get_values(node) > 0 :
                var = '%s' % node
                NoP.append(var)
    for i in range(len(NoP)):
        print ' -- ', Cij[i], ' --    ', NoP[i]
    print '**********************************************************************'
    print ' -- Branch and Bound Directed Traveling Salesperson Problem -- '
    m.write('pathCPLEX_TSP.lp')
    
try:
    CPLEX_TSP(100,5,900)
    print '\nJames Gaboardi, 2015'
except Exception as e:
    print e