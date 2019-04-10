
import itertools
import time
'''

Solution to the zebra puzzle exercises

'''


def imright(h1, h2):
    "House h1 is immediately right of h2 if h1-h2 == 1."
    return h1-h2 == 1

def nextto(h1, h2):
    "Two houses are next to each other if they differ by 1."
    return abs(h1-h2) == 1

def zebra_puzzle():
    houses = [first,_,middle,_,_] = [1,2,3,4,5]
    # return a generator expression
    return ((WATER,ZEBRA)
        for(red, green, ivory, yellow, blue) in itertools.permutations(houses)
        if imright(green, ivory)        #6
        for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in itertools.permutations(houses)
        if Englishman == red           #2
        if Norwegian == first           #10
        if nextto(Norwegian, blue)      #15
        for (cofee, tea, milk, oj, WATER) in itertools.permutations(houses)
        if cofee == green               #4
        if Ukranian == tea              #5
        if milk == middle               #9
        for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in itertools.permutations(houses)
        if Kools == yellow              #8
        if LuckyStrike == oj            #13
        if Japanese == Parliaments      #14
        for (dog, snails, fox, horse, ZEBRA) in itertools.permutations(houses)
        if Spaniard == dog              #3
        if OldGold == snails            #7
        if nextto(Chesterfields, fox)
        if nextto(Kools, horse)
       )

if __name__ == "__main__":
    
    # g is a generator
    g = zebra_puzzle()
    
    t0 = time.time()
    w,z = next(g)
    t1 = time.time()
    
    print ('w, z = {0},{1}'.format(w,z))
    print ('Search took {0} seconds'.format(t1-t0))


