def answer(s):
    # your code here
    right_counter = 0
    salutes = 0

    #Loop through the entire string
    for i in s:
        #Increment a counter every time an employee walking to the right is encountered 
    	if i == '>':
    		right_counter += 1

        #Whenever an employee walking to the left is encountered, multiply the right_counter by two and add this to the
        #running sum of salutes - every employee walking to the left will salute every employee already encountered walking to the right
    	if i == '<':
    		salutes += 2*right_counter

    return salutes

if __name__ == '__main__':
	print answer("<<>><")
