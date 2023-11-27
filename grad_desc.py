import numpy as np
from hello import *
from numpy import linalg as LA
def shuffle_in_unison(a, b):
        assert len(a) == len(b)
        shuffled_a = np.empty(a.shape, dtype=a.dtype)
        shuffled_b = np.empty(b.shape, dtype=b.dtype)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
            shuffled_a[new_index] = a[old_index]
            shuffled_b[new_index] = b[old_index]
        return shuffled_a, shuffled_b


n,m = np.shape(vec)



inp = vec
out = outcome



params = np.zeros([1 , m])

arr = [ 3.77088176e-04 ,-1.83389805e-02,1.35312572e-03,4.96789215e-01
, 4.66598750e-01,4.96366631e-01,4.76453799e-01,4.47631339e-01
, 4.67653908e-01,4.54031046e-01,5.00111724e-01,3.82790715e-01
, 3.77399828e-01 ,-7.29205194e-04 ,-5.12503221e-03,8.62432780e-05
, 7.75114993e-05,6.25739624e-03]

for i in range(m):
    params[0][i] = arr[i]

# print(inp , out , params)
inp , out = shuffle_in_unison(inp, out)

def calc_cost():
    global params , inp , out
    # print(params , inp , out)
    tmp = (inp @ params.T - out)
    return tmp

def diff_cost():
    global inp
    out = np.zeros([1 , m])
    tmp = calc_cost()
    # print(np.shape(tmp))
    for i in range(m):
        for j in range(n):
            out[0][i] += (1 / n) * tmp[j] * inp[j][i]

    return out  

def grad_desc(iter):
    global params
    for i in range(iter):
        params = params - 0.00001 * diff_cost()
        # print(params)
        print(np.sum(calc_cost() ** 2) / (2 * n))

grad_desc(20)

# #svd
# U , S , Vt = LA.svd(inp , full_matrices=False)
# # print(S)
# params = Vt.T @ LA.inv(np.diag(S)) @ U.T @ outcome
# params = np.reshape(params , (1 , 18))
# print(params)
# print(np.sum(calc_cost() ** 2) / (2 * n))

ct = 0
ctdum = 0
totct = 0
for i in vec:
    outputprob = np.inner(i,params)
    if outputprob > 0.6:
        if outcome[totct] == 0 and vec[totct][0] > 60 :
            ct += 1
        ctdum += 1
    elif outputprob < 0.4 and vec[totct][0] > 60:
        if outcome[totct] == 1:
            ct += 1
        ctdum += 1
    totct += 1
    
    
print(100 - (ct / ctdum) * 100)

