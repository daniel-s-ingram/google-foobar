#The number of different staircases that can be formed out of n bricks
#is equal to the number of distinct integer partitions of n
def count_distinct_partitions(m):
	table = [[0 for _ in xrange(m+1)] for _ in xrange(m+1)]
	table[0][0] = 1

	'''
	The number of partitions of a number n into at least k parts equals the number of partitions into exactly k parts
	plus the number of partitions into at least k-1 parts. Subtracting 1 from each part of a partition of n into k parts
	gives a partition of n-k into k parts. These two facts together are used for this algorithm.
	'''
	for n in xrange(1, m+1):
		for k in xrange(m+1):
			table[n][k] = table[n][k-1]
			if n >= k:
				table[n][k] += table[n-k][k]

	return table[m][m]

def answer(n):
    # your code here
	return count_distinct_partitions(n)

print answer(10)
