from math import factorial

def answer(l):
    # your code here
    n = len(l)
    array = [0 for _ in xrange(n)]
    triples = 0

    #Dynamic programming solution
    #Original solution was brute force O(n^3)
    for i in xrange(n):
    	for j in xrange(i):
            #If an earlier element l[j] divides a later element l[i], we've found a potential pair in a lucky triple
            #Increment array[i] to indicate we've found another divisor
            #Add to triples the number of divisors of l[j], as all of them will form lucky triples with l[j] and l[i]
    		if l[i]%l[j] == 0:
    			array[i] += 1
    			triples = triples+array[j]

    return int(triples)

if __name__ == '__main__':
	l = [1,2,3,4,5,6,12]
	print l
	print answer(l)