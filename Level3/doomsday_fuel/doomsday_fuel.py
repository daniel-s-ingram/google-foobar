from fractions import Fraction, gcd

#Convert the state transition matrix to the standard form for absorbing Markov chains
def to_standard(m):
	standard = [state[:] for state in m]
	n = len(standard)

	terminal_states = []
	nonterminal_states = []
	weights = []

	#Find the terminal states and put a 1 on the diagonal for that row to 
	#symbolize that that state has a 100% of going back to itself (absorbing/terminal state)
	for i in xrange(n):
		weights.append(sum(m[i]))
		if sum(standard[i]) == 0:
			m[i][i] = 1
			standard[i][i] = 1
			terminal_states.append(i)
		else:
			nonterminal_states.append(i)

	#Convert matrix entries to probabilities
	for i in xrange(n):
		total = float(sum(m[i]))
		for j in xrange(n):
			m[i][j] = m[i][j]/total

	#Reorder the rows and columns so that the absorbing states are first
	i = 0
	for term in terminal_states:
		j = 0
		for state in terminal_states:
			standard[i][j] = m[term][state]
			j = j+1

		for state in nonterminal_states:
			standard[i][j] = m[term][state]
			j = j+1

		i = i+1

	for term in nonterminal_states:
		j = 0
		for state in terminal_states:
			standard[i][j] = m[term][state]
			j = j+1

		for state in nonterminal_states:
			standard[i][j] = m[term][state]
			j = j+1

		i = i+1

	return standard, terminal_states

#Matrix multiplication
def matmul(x, y):
	n = len(x)
	m = len(y)
	try:
		p = len(y[0])
	except:
		p = 0

	product = [[0 for _ in xrange(p)] for _ in xrange(n)]
	
	for i in xrange(n):
		for j in xrange(p):
			for k in xrange(m):
				product[i][j] += x[i][k]*y[k][j]

	return product

#Identity matrix of size nxn
def identity(n):
	identity_matrix = [[0 for _ in xrange(n)] for _ in xrange(n)]
	for i in xrange(n):
		identity_matrix[i][i] = 1
	return identity_matrix

#Calculates the least common denominator of the elements in an array
def lcd(denoms):
	n = len(denoms)

	lcd = denoms[1]*denoms[0]/gcd(denoms[1],denoms[0])
	for i in xrange(2, n):
		lcd = lcd*denoms[i]/gcd(lcd, denoms[i])

	print lcd
	return lcd

#Matrix inverse code from Stack Overflow user stackPusher
#https://stackoverflow.com/questions/32114054/matrix-inversion-without-numpy/39881366
#####################################################################################
def transposeMatrix(m):
    t = []
    for r in range(len(m)):
        tRow = []
        for c in range(len(m[r])):
            if c == r:
                tRow.append(m[r][c])
            else:
                tRow.append(m[c][r])
        t.append(tRow)
    return t

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeterminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeterminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
###########################
#end of Stack Overflow code

def answer(m):
    # your code here
	if len(m) == 1:
		return [1,1]

	#Convert state transition matrix to standard form for absorbing Markov chains so that the limiting matrix
	#can be found - this limitig matrix will contain the probabilities for ending up in each terminal state
	standard_m, terminal_states = to_standard(m)
	num_states = len(standard_m)
	num_terminal = len(terminal_states)

	#Grab the R and Q submatrices
	#R: probabilities of a nonterminal state transitioning to a terminal state
	#Q: probabilities of a nonterminal state transitioning to a nonterminal state
	R = [state[:num_terminal] for state in standard_m[num_terminal:num_states]]
	Q = [state[num_terminal:num_states] for state in standard_m[num_terminal:num_states]]
	I = identity(len(Q))

	#Calculate FR - the limiting matrix
	F = getMatrixInverse([[I[i][j]-Q[i][j] for j in xrange(len(Q))] for i in xrange(len(Q))])
	FR = matmul(F, R)

	#The probabilities we want are along the first row of FR
	probs = FR[0]

	#Convert the probabilities to a numerator and least common denominator
	numers = [0]*num_terminal
	denoms = [0]*num_terminal
	for i in xrange(num_terminal):
		numers[i] = Fraction(probs[i]).limit_denominator(2**31-1).numerator
		denoms[i] = Fraction(probs[i]).limit_denominator(2**31-1).denominator

	lc = lcd(denoms)

	for i in xrange(num_terminal):
		numers[i] = numers[i]*lc/denoms[i]
		probs[i] = numers[i]

	probs.append(lc)
	return probs

if __name__ == '__main__':
	m = [[0, 7, 0, 17, 0, 1, 0, 5, 0, 2],
         [0, 0, 29, 0, 28, 0, 3, 0, 16, 0],
         [0, 3, 0, 0, 0, 1, 0, 0, 0, 0],
         [48, 0, 3, 0, 0, 0, 17, 0, 0, 0],
         [0, 6, 0, 0, 0, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
	#print m
	print answer(m)