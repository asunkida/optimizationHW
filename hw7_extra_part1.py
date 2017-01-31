#!/usr/bin/python
# Copyright 2016, Gurobi Optimization, Inc.
from gurobipy import *


n=4039
s=0


f = open('facebook_combined.txt', 'r')
G = {}
# Loop over lines and extract variables of interest
for line in f:
		line = line.strip()
		#print(line)
		nodes = line.split(' ')
		G[(int(nodes[0]), int(nodes[1]))]=1
		G[(int(nodes[1]), int(nodes[0]))]=1 

f.close()
print('Finished reading the file')
#net supply is 4038 for sink and -1 for all other nodes
#capacity at every edge
#cap is 4038 for all edges 

# Create model
m = Model("sp")

#add one variable for every edge
x={}
for k,v in G.items():
	x[k] = m.addVar(lb=0, ub=GRB.INFINITY, name='x_%d,%d' % k) #variable upper bound

m.update()


#print type(k[0])
#add objective
objExpr=LinExpr()
for k,v in G.items():
	objExpr.add(x[k],G[k])
m.setObjective(objExpr, GRB.MINIMIZE)

#add constraints
expr={}
rhs={}
for i in range(0,n):
	expr[i] = LinExpr()
	rhs[i]= -1 ### bi at every node i
rhs[s]=4038
#rhs[t]=-1


for k,v in G.items():
	expr[k[0]].add(x[k],1)
	expr[k[1]].add(x[k],-1)
	

for i in range(0,n):
	m.addConstr(expr[i], GRB.EQUAL, rhs[i])

#print expr[s]
#print rhs[s]
#print expr[4038]
#print rhs[4038]
#print expr[3674]
#print rhs[3674]
#print G.items()

#write the model
m.update()
m.write("minCostFlow.lp")


#optimize
m.optimize()
avg = m.objVal/4039
print "the average exposure time is "  
print avg

#print
for v in m.getVars():
	if v.varName.startswith("x_3674"):
		if v.x == 1:
			print('%s %g' % (v.varName, v.x))

