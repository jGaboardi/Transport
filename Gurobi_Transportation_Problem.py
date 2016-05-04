# -*- coding: utf-8 -*-
'''
GNU LESSER GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
'''
# Building and Optimizing The Transportation Problem in
#        Python/Gurobi[gurobipy]

import numpy as np
import gurobipy as gbp
import time
np.random.seed(352)

def GuTransProb(Cij, Si, Dj):
    t1 = time.time()
    #  Data
    
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
    
    # Create Model, Set MIP Focus, Add Variables, & Update Model
    m = gbp.Model(' -- The Transportation Problem -- ')
    # Set MIP Focus to 2 for optimality
    gbp.setParam('MIPFocus', 2)
    descision_var = []
    for orig in supply_nodes_range:
        descision_var.append([])
        for dest in demand_nodes_range:
            descision_var[orig].append(m.addVar(vtype=gbp.GRB.CONTINUOUS, 
                                            obj=Cij[orig][dest], 
                                            name='x'+str(orig+10001)+'_'+str(dest+10001)))
    # Update Model Variables
    m.update()       
    
    #  Set Objective Function
    m.setObjective(gbp.quicksum(Cij[orig][dest]*descision_var[orig][dest] 
                            for orig in supply_nodes_range for dest in demand_nodes_range), 
                            gbp.GRB.MINIMIZE)
                            
    # Add Supply Constraints
    for orig in supply_nodes_range:
        m.addConstr(gbp.quicksum(descision_var[orig][dest] 
                            for dest in demand_nodes_range) - Si[orig] <= 0)
    # Add Demand Constraints
    for orig in demand_nodes_range:  
        m.addConstr(gbp.quicksum(descision_var[dest][orig] 
                            for dest in supply_nodes_range) - Dj[orig] >= 0,
                            'Demand_Constraint_%d' % orig)
    
    #  Optimize and Print Results
    try:
        m.optimize()
    except Exception as e:
        print e
        
    t2 = time.time()-t1
    print '******************************************************************************'
    print '| From SUPPLY Facility to DEMAND Facility x(Si)_(Dj) shipping # of units  '
    print '| ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓'
    print '|'
    selected = {}
    Closed = []
    for v in m.getVars():
        var = '%s' % v.VarName
        if v.x > 0:
            units = '%i' % v.x
            selected[var] = units
            print '|  Supply Facility #', var[1:6], 'is shipping', units, \
                                                'units to Demand Facility #', var[-5:]
        else:
            Closed.append([var[1:6], var[-5:]])
    print '******************************************************************************'
    print '    | Objective Value --------------------- ', int(m.objVal)
    print '    | Supply Facilities ------------------- ', len(Si)
    print '    | Total Supply Units ------------------ ', Si.sum()
    print '    | Demand Facilites -------------------- ', len(Dj)
    print '    | Total Demand Units ------------------ ', Dj.sum()
    print '    | Total Potential Combinations -------- ', len(Si)*len(Dj)
    print '    | Actual Combinations  ---------------- ', len(selected)
    print '    | Real Time to Optimize (sec.) -------- ', t2
    print '******************************************************************************'
    print '  --  The Transportation Simplex with Gurobi --'
    m.write('path.lp')
    
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
try:
    GuTransProb(Cij=Cost_Matrix, Si=Supply, Dj=Demand)
    print '\nJames Gaboardi, 2016'
    print '*******************************************************************'\
                                        '**********************\n\n'
except Exception as e:
    print e