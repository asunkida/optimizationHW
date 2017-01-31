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



############ Write you code from here #################

# Put model data into matrices/vectors and call lp_optimize
# create a new model 
model = Model()
#m = [[0 for j in range(C)] for i in range(N)]
#n = [[0 for j in range(C)] for i in range(N)]
m = [0 for i in range(N)]
n = [0 for i in range(N)]
dotprod = [0 for j in range(C)]
vsum = 0
zsum = 0

objsum = 0
# create variables , lowerbound is 0 by default, w[j]
for i in range (0,N):
    m[i] = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
    n[i] = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
    objsum = objsum + m[i]*(-y[i]) + n[i]*y[i]



model.update()


model.setObjective(objsum, GRB.MAXIMIZE)
model.update()

for i in range (0,N):
    vsum = vsum + m[i] + n[i]
    zsum = zsum - m[i] + n[i]
    model.addConstr(m[i] >= 0)
    model.addConstr(n[i] >= 0)

model.addConstr(vsum, GRB.EQUAL, 1)
model.addConstr(zsum, GRB.EQUAL, 0)

for j in range(0,10):
    dotprod[j] = 0
    for i in range (0,N):
        dotprod[j] = dotprod[j] - m[i]*x[i][j] + n[i]*x[i][j]
    model.addConstr(dotprod[j], GRB.EQUAL, 0)


model.optimize()



model.reset()

m = [0 for i in range(N)]
n = [0 for i in range(N)]
#s = [0 for i in range(N)]
objsum = 0
#ssum = 0
bsum = 0
dotprod = [0 for j in range(C)]


for i in range(0,N):
    m[i] = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
    n[i] = model.addVar(lb = 0, ub = GRB.INFINITY, vtype = GRB.CONTINUOUS)
    objsum = objsum + m[i]*(y[i]) - n[i]*y[i]

model.update()

model.setObjective(objsum, GRB.MAXIMIZE)

for i in range (0,N):
    bsum = bsum + m[i] - n[i]
    model.addConstr(m[i] >= 0)
    model.addConstr(n[i] >= 0)
    model.addConstr(m[i] + n[i], GRB.EQUAL, 1)

model.addConstr(bsum, GRB.EQUAL, 0)

for j in range(0,10):
    dotprod[j] = 0
    for i in range (0,N):
        dotprod[j] = dotprod[j] + m[i]*x[i][j] - n[i]*x[i][j]
    model.addConstr(dotprod[j], GRB.EQUAL, 0)

model.optimize()


