file  = open('a2.csv', 'r')
file2 = open('a_prepared.csv', 'w')
i = 0

for line in file:
	i += 1
	
	file2.write("%d , %s" % (i, line))
