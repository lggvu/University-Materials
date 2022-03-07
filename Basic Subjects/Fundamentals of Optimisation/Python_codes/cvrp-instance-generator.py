import random as rd

def gen(filename,K,N):
	#K : number of trucks
	#N : number of customers
	
	r = [] #request items of customers
	solution = [0 for i in range(N)]
	load = [0 for k in range(K)]
	
	for k in range(N):
		r.append(rd.randint(10,20))
		
	print(r)
	
	# gen random solution
	for i in range(N):
		selected_truck = rd.randint(0,K-1)
		print('selected truck = ',selected_truck)
		solution[i] = selected_truck
		load[selected_truck] += r[i]		
	
	c = [0 for k in range(K)] # capacity of trucks
	for k in range(K):
		c[k] = load[k] + rd.randint(0,3)
		
	print('solution = ',solution)
	print('c = ',c)

	M = N + 2*K
	d = [[rd.randint(3,10) for i in range(M)] for j in range(M)]
	print(d)
	
	f = open(filename,'w')
	f.write(str(N) + ' ' + str(K) + '\n')
	line = ''
	for ci in c:
		line = line + str(ci) + ' '
		
	f.write(line + '\n')
	
	line = ''
	for ri in r:
		line = line + str(ri) + ' '
	f.write(line + '\n')
	for i in range(M):
		line = ''
		for j in range(M):
			line = line + str(d[i][j]) + ' '
		f.write(line + '\n')
	
gen('cvrp-K3-N10.txt',3,10)	