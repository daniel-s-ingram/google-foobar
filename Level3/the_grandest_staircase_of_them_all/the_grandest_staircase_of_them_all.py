#The number of different staircases that can be formed out of n bricks
#is equal to the number of distinct integer partitions of n
def count_distinct_partitions(n):
	table = [[0 for _ in xrange(n+1)] for _ in xrange(n+1)]
	table[0][0] = 1

	#Need to do more research before I can comment on why this works
	for i in xrange(1, n+1):
		for j in xrange(n+1):
			table[i][j] = table[i-1][j]
			if j >= i:
				table[i][j] = table[i][j]+table[i-1][j-i]

	return table[n][n]-1

def answer(n):
    # your code here
	return count_distinct_partitions(n)

print answer(10)