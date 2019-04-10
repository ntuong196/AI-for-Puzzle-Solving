'''
Created on Sun Oct  14 2018
Modified on Thu 18 2018
- fixed display of DP table

@author: frederic


Dynamic Programming prac sheet solution

Compare versions of the Levenshtein edit distance.




'''

import time
import numpy as np

# Exercises 1 and 2

#    Instead of using the memoize function, we could directly add a
#    dictionary to the 'lev' function.


def memoize(fn):
    """Memoize fn: make it remember the computed value for any argument list"""
    def memoized_fn(*args):
        # print args
        if not args in memoized_fn.cache:
            memoized_fn.cache[args] = fn(*args)
##        else:
##            print( 'new ' ,args)
        return memoized_fn.cache[args]
    memoized_fn.cache = {}
    return memoized_fn



def lev(a, 
        b, 
        insert_cost = lambda x:1 , 
        delete_cost = lambda x:2 , 
        match_cost = lambda x,y: 0 if x==y else 4):        
    '''
    Compute the Levenshtein distance between the
    two sequences a and b
    @param
        a :  sequence
        b :  sequence
        insert_cost : insert cost function , 
        delete_cost : deletion cost function , 
        match_cost : match cost function        
            
    '''
    # Python trick:
    # the test
    #   if len(some_string)==0:
    # can be replaced with
    #   if some_string:
    
#    print ('debug lev >> a = {} , b = {}  '.format(a,b))
    
    if len(a)==0:
        # cost of inserting all elements of sequence b
        return sum([insert_cost(y) for y in b])
    if len(b)==0: 
        # cost of deleting all elements of sequence a
        return sum([delete_cost(x) for x in a])
    
    # the sequences a and b are non-empty
    return min(
        lev(a[:-1], b[:-1])+match_cost(a[-1],b[-1]) ,
        lev(a, b[:-1])+insert_cost(b[-1]) ,
        lev(a[:-1], b)+delete_cost(a[-1]) 
        )

def fill_lev_table(a,b):
    '''
    Lazy way to fill a Levenshtein
    of edit distance of word 'a' into word 'b'
    '''
    levm = memoize(lev)
    
#    levm = lev
    # print head row (word b)
    print('\t'*2,end='')
    print(*(c for c in b),sep='\t')
    print('')    

    print('\t'*2,end='')
    print( *( levm('',b[:j+1]) for j in range(len(b)))  ,sep='\t')
    print('')    
    for i in range(len(a)):
        print(a[i],'\t',i+1,end='\t')
        for j in range(len(b)):
            print(levm(a[:i+1],b[:j+1]),end='\t')
        print('\n')    
    

# ----------------------------------------------------------------------------


# edit operation codes
dict_op = {0:'match', 1: 'insert', 2 :'delete',
           'match':0, 'insert':1, 'delete':2}

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Exercise 3
def dynprog(x,
          y,
        insert_cost = lambda c:2 , 
        delete_cost = lambda c:1 , 
        match_cost = lambda cx, cy: 0 if cx==cy else 5):        
    '''
    Compute the Levenshtein distance between the  two sequences x and y 
    @param
        x :  sequence
        y :  sequence
        insert_cost : insert cost function , 
        delete_cost : deletion cost function , 
        match_cost = match cost function

    Compute the cost of editing sequence x into sequence y.
    Let nx , ny = len(x) , len(y)
    Sequence x is indexed from 0 to nx-1 (similar remark for y).
    M[nx,ny] is the cost of editing from x to y
    Note that M[0,3] is the cost of matching the empty string to the first 
    3 characters of sequence y.
    
    
    @return
    M,P
    where 
        M is the DP cost matrix
        M[i,j] : cost of matching x[:i] to y[:j]
                Note that x[i] and y[j] are not taken into account for M[i,j]
        M[nx,ny] : cost of matching x[:nx] to y[:ny]
        and
        P is the parent array to trace back the edit sequence
        P is used by the function 'explain_seq'
    '''
    
    #    x[0],...,x[nx-1]
    #    y[0],...,y[ny-1]
    #
    #    M : cost matrix

    nx = len(x)
    ny = len(y)
     
    # Cost matrix M
    # M[i,j] cost of matching the slice  x[:i] to the slice y[:j]
    # M[nx,ny] will be the cost of matching the whole sequences       
    M = np.zeros((nx+1,ny+1),dtype=float)

    # P[i,j] indicates to op code use for the last optimal operation
    # in matching the slice  x[:i] to the slice y[:j] 
    P = np.zeros((nx+1,ny+1),dtype=int) # parent 
    
    M[1:,0] = np.cumsum([delete_cost(c) for c in x])   
    P[1:,0] = dict_op['delete'] # delete op code 

    M[0,1:] = np.cumsum([insert_cost(c) for c in y])
    P[0,1:] = dict_op['insert'] # insert op code
    
    for ix in range(1,nx+1):
        for iy in range(1,ny+1):
            # print('ix {} iy {} '.format(ix,iy) )
            # M[ix][iy] cost of matching 
            # x[:ix] =x[0],..,x[ix-1 to y[:iy] = y[0],..,y[iy-1]
            L = [M[ix-1,iy-1] + match_cost(x[ix-1],y[iy-1]), # match x[ix-1] and  y[iy-1]
                 M[ix,iy-1] + insert_cost(y[iy-1]), # insert  y[iy-1]
                 M[ix-1,iy] + delete_cost(x[ix-1])] # delete  x[ix-1] 
            i_min = np.argmin(L)
            P[ix][iy] = i_min
            M[ix][iy] = L[i_min]
    return M,P


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    

def explain_dynprog(x,y,M,P):
    '''
    Retrieve the optimal sequence of edit operations given the dyn prog tables M,P
    @pre
     M,P have been computed by dynamic_1
    '''
    nx = len(x)
    ny = len(y)
    L =[]
    ix,iy = nx, ny
    while ix>0 and iy>0:
        if P[ix,iy]==0: #'match op':            
            L.append( ' match {} and {} '.format(x[ix-1],y[iy-1]))
            ix -= 1
            iy -= 1
        elif P[ix,iy]==1:# 'insert op'
            L.append( 'insert '+str(y[iy-1]))
            iy -= 1
        else: # 'delete op'
            L.append( 'delete '+str(x[ix-1]))
            ix -= 1
    #print('<A> ix = {} iy = {} '.format(ix,iy) )
    while ix>0:
        L.append( 'delete '+str(x[ix-1]))
        ix -= 1
    while iy>0:
        L.append( 'insert '+str(y[iy-1]))
        iy -= 1
    
    return list(reversed(L))
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    pass

    # Exercises 1 and 2
    if 1:
#        fill_lev_table('','b')
    
#        fill_lev_table('crook','book')
        w1 = 'boating'
        w2 = 'aortic'
        fill_lev_table(w1,w2)
        
#        fill_lev_table('sitting','kitten')
    #    fill_lev_table('billing','ailigs')
    #    
    #    t0 = time.time()
    #    d = lev(w1,w2)
    #    t1 = time.time()
    #    print ('time naive lev : ', t1-t0, ' edit distance ',d) 
    #
    #    lev = memoize(lev)
    #    t0 = time.time()
    #    d = lev(w1,w2)
    #    t1 = time.time()
    #    print ('time memoized lev : ', t1-t0, ' edit distance ',d )
# 

    
    # Exercise 3
    
    if 0:    
        #    w1 = 'aephgrowr'
        #    w2 = 'bsaraaspdmr'    
        w1 = 'trump'
        w2 = 'dumbpark'
        w1, w2 = '', 'boo'
        
#        w1 = 'pumpkin'
#        w2 = 'plank'

        w1 = 'boating'
        w2 = 'aortic'
        
        
        print('w1 = {}'.format(w1))
        print('w2 = {}'.format(w2))

        M,P = dynprog(w1,w2, 
                      insert_cost = lambda c:1 , 
                      delete_cost = lambda c:2 , 
                      match_cost = lambda cx, cy: 0 if cx==cy else 4)    
        
        
        
        print('DP matrix')
        print(M)
        L = explain_dynprog(w1,w2,M,P)    
        print(L)


