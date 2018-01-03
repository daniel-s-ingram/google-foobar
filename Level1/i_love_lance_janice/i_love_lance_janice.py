def answer(s):
    # your code here
    words = s.split(' ')
    alphabet = ['a','b','c','d','e','f','g','h','i','j',
                'k','l','m','n','o','p','q','r','s','t',
                'u','v','w','x','y','z']
    
    #For each character in the string, determine its location (k) in the alphabet and replace it with the letter at location 25-k 
    for i in xrange(len(words)):
        word = list(words[i])
        print word
        for j in range(len(word)):
            isLetter = False
            for k in xrange(len(alphabet)):
                if alphabet[k] == word[j]:
                    isLetter = True
                    break
            if isLetter:        
                word[j] = alphabet[25-k]
            
        words[i] = ''.join(word)
        
    return ' '.join(words)

if __name__ == '__main__':
    print answer("wrw blf hvv ozhg mrtsg'h vkrhlwv?")