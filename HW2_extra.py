# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 22:09:14 2016

@author: Jing Sun, UNI:JS4938
"""

import sys
from gurobipy import *
#from myMatrixLpSolver import *


# Open a file
f = open('dataLR.txt', 'r')
N=10000
C=10
x = [[0 for j in range(C)] for i in range(N)] 
y = [0 for i in range(N)] 
# Loop over lines and extract variables of interest
i=-1
for line in f:
		i=i+1
		line = line.strip()
		columns = line.split(',')
		y[i]=float(columns[0])
		for j in range(0,10):
			x[i][j] = float(columns[j+1])

f.close()



# Put model data into matrices/vectors and call lp_optimize
# create a new model 
model = Model()
w = [0 for j in range (C)]
dotprod = [0 for i in range (N)]

# create variables , lowerbound is 0 by default, w[j]
for j in range (0,10):
    w[j] = model.addVar(lb = - GRB.INFINITY, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
 
b = model.addVar(lb = - GRB.INFINITY, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
V = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)

model.update()
model.setObjective(V, GRB.MINIMIZE)
#model.update()

for i in range (0,N):
    dotprod[i] = 0
    for j in range(0,10):
        dotprod[i] = dotprod[i] + w[j]*x[i][j]      
    model.addConstr(V >= dotprod[i] + b - y[i])
    model.addConstr(V >= y[i] - dotprod[i] - b)

model.optimize()

print 'Model Status for (a):', model.status

print ("optimal solution for (a) is ")
print ("w = [")

for j in range (0,10):
    print "%f ," %w[j].x
print ("]")

print "b = %f" %b.x

#Reset model and construct LP for question (b)
model.reset()
m = [0 for j in range (C)]
s = [0 for i in range (N)] 
dotprod = [0 for i in range (N)]

for j in range (0,10):
    m[j] = model.addVar(lb = - GRB.INFINITY, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)

for i in range (0,N):	
    s[i] = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
 
b = model.addVar(lb = - GRB.INFINITY, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
#V = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)

model.update()
model.setObjective(V, GRB.MINIMIZE)
model.update()

totalsum = 0;
for i in range (0,N):
    dotprod[i] = 0
    for j in range(0,10):
        dotprod[i] = dotprod[i] + m[j]*x[i][j]      
    model.addConstr(s[i] >= dotprod[i] + b - y[i])
    model.addConstr(s[i] >= y[i] - dotprod[i] - b)
    totalsum = totalsum + s[i]
    
model.setObjective(totalsum, GRB.MINIMIZE)

model.optimize()
print 'Model Status for (b):', model.status
print ("optimal solution for (b) is ")
print ("m = [")

for j in range (0,10):
    print "%f ," %m[j].x
print ("]")

print "b = %f" %b.x

# optimizationHW
