from hello import *
import numpy as np
from numpy import linalg as LA


n,m = np.shape(traindata)



inp = traindata
out = trainoutcome

params = np.zeros([1 , m])
# print(inp , out , params)
# inp , out = shuffle_in_unison(inp, out)

def calc_cost():
    global params , inp , out
    # print(params , inp , out)
    tmp = (inp @ params.T - out)
    return tmp

#svd
U , S , Vt = LA.svd(inp , full_matrices=False)
# print(S)
# A = U * S * Vto
# x = V * S * Ut * y 
# s = singular values. 
params = Vt.T @ LA.inv(np.diag(S)) @ U.T @ out
params = np.reshape(params , (1 , 24))
print(params)
print(np.sum(calc_cost() ** 2) / (2 * n))

ct = 0
ctdum = 0
totct = 0


for i in testdata:
    outputprob = np.inner(i,params)
    if outputprob > 0.6:
        if testoutcome[totct] == 0 and testdata[totct][0] > 60 :
            ct += 1
        ctdum += 1
    elif outputprob < 0.4 and testdata[totct][0] > 60:
        if testoutcome[totct] == 1:
            ct += 1
        ctdum += 1
    totct += 1
    
    
print(100 - (ct / ctdum) * 100)

svdacc = (100 - (ct / ctdum) * 100)

