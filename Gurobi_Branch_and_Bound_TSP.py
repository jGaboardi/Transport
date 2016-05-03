# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Building and Optimizing a Branch and Bound Directed 
#        Traveling Salesperson problem in Python/Gurobi[gurobipy]
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
import gurobipy as gbp
import time
t1 = time.time()
np.random.seed(352)
def GuTSP(nodes, min_cost, max_cost):
    #     1. Read In (or Create)Data
    # CREATE
    # Cost Matrix
    Cij = np.random.randint(min_cost, max_cost, nodes**2)
    Cij = Cij.reshape(nodes,nodes)
    # Cost Sum
    CijSum = np.sum(Cij)
    
    tour_nodes = range(len(Cij[0]))
    
    #       2. Create Model, Set MIP Focus, Add Variables, & Update Model
    m = gbp.Model(' -- Branch and Bound Directed Traveling Salesperson Problem -- ')
    # Set MIP Focus to 2 for optimality
    gbp.setParam('MIPFocus', 2)
    # Add Decision Variables
    desc_var = []
    for orig in tour_nodes:
        desc_var.append([])
        for dest in tour_nodes:
            desc_var[orig].append(m.addVar(vtype=gbp.GRB.BINARY, 
                                                obj=Cij[orig][dest], 
                                                name='x'+str(orig+1)+'_'+str(dest+1)))
    # Update Model Variables
    m.update()       
    
    #       3. Set Objective Function
    m.setObjective(gbp.quicksum(Cij[orig][dest]*desc_var[orig][dest] 
                            for orig in tour_nodes for dest in tour_nodes), 
                            gbp.GRB.MINIMIZE)
    
    #       4. Add Constraints
    #Add Assignment Constraints by summed rows x_ij
    for orig in tour_nodes:
        m.addConstr(gbp.quicksum(desc_var[orig][dest] 
                            for dest in tour_nodes) == 1)
    #Add Assignment Constraints by summed columns x_ji                        
    for orig in tour_nodes:
        m.addConstr(gbp.quicksum(desc_var[dest][orig] 
                            for dest in tour_nodes) == 1)
    
    #       5. Optimize and Print Results
    try:
        m.optimize()
    except Exception as e:
        print e
        
    t2 = time.time()-t1
    print '**********************************************************************'
    print '    | Nodes on Path ---------------------------- ', len(Cij)
    val = m.objVal
    print '    | Objective Value -------------------------- ', val
    avg = float(m.objVal)/float(len(Cij))
    print '    | Avg. Value / Arc ------------------------- ', avg
    print '    | Total Network Travel Cost ---------------- ', CijSum
    print '    | Real Time to Optimize (sec.) ------------- ', t2
    print '    | '
    print '    | Cij ', len(Cij)*' ↓' , '        Tour by Node Order'
    NoP = []
    for v in m.getVars():
        if v.x > 0:
            var = '%s' % v.VarName
            NoP.append(var)
    
    for i in range(len(NoP)):
        print '    |  -- ', Cij[i], ' --    ', NoP[i]
    print '    |                               ^^^^ Tour by Node Order'
    print '**********************************************************************'
    print ' -- Branch and Bound Directed Traveling Salesperson Problem -- '
    m.write('path_Gurobi_TSP.lp')
    
try:
    GuTSP(100,5,900)
    print '\nJames Gaboardi, 2015'
except Exception as e:
    print e