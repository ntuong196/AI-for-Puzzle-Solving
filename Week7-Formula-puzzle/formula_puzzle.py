#
#  Instructions:
#
#   Complete the fill_in(formula) function
#
#   Hints:
#    itertools.permutations
#    and str.maketrans  are handy functions
#    Using the 're' module leads to more concise code.

import re, itertools

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f
    
def fill_in(formula):
    ''' Return a generator that enumerate  all possible fillings-in
        of letters in formula with digits.'''

    ## INSERT YOUR CODE HERE

    
def valid(f):
    """Formula f is valid if and only if it has no 
    numbers with leading zero, and evals true."""
    try: 
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False

print( solve('ODD + ODD == EVEN'))
print (solve('A**2 + BC**2 == BD**2'))

##    Should output
##    >>> 
##    655 + 655 == 1310
##    2**1 + 34**1 == 36**1

#print (re.split('([A-Z]+)', 'A**2 + BC**2 == BD**2'))
