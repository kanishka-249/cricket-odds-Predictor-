# import numpy as np 
# from grad_desc import *

# def initialize_adam(parameters) :
    
#     L = len(parameters) // 2
#     v = {}
#     s = {}
    
  
#     for l in range(1, L + 1):
   
#         x,y = np.shape(parameters["W" + str(l)])
#         v["dW" + str(l)] = np.zeros([x,y])
#         s["dW" + str(l)] = np.zeros([x,y])
#         x,y = np.shape(parameters["b" + str(l)])
#         v["db" + str(l)] = np.zeros([x,y])
#         s["db" + str(l)] = np.zeros([x,y])
    
#     return v, s

# def update_parameters_with_adam(parameters, grads, v, s, t, learning_rate = 0.01,
#                                 beta1 = 0.9, beta2 = 0.999,  epsilon = 1e-8):
    
#     L = len(parameters) // 2              
#     v_corrected = {}                         
#     s_corrected = {}                         
#     alpha = learning_rate
  
#     for l in range(1, L + 1):
       
#         v["dW" + str(l)] = beta1*v["dW" + str(l)] + (1-beta1)*(grads['dW' + str(l)])
#         v["db" + str(l)] = beta1*v["db" + str(l)] + (1-beta1)*(grads['db' + str(l)])
        
#         v_corrected["dW" + str(l)] = v["dW" + str(l)]/(1 - ((beta1)**t))
#         v_corrected["db" + str(l)] = v["db" + str(l)]/(1 - ((beta1)**t))
        
        
#         s["dW" + str(l)] = beta2*(s["dW" + str(l)])+(1-beta2)*((grads['dW' + str(l)])**2)
#         s["db" + str(l)] = beta2*(s["db" + str(l)])+(1-beta2)*((grads['db' + str(l)])**2)
        
        
#         s_corrected["dW" + str(l)] = s["dW" + str(l)]/(1 - ((beta2)**t))
#         s_corrected["db" + str(l)] = s["db" + str(l)]/(1 - ((beta2)**t))
        
#         parameters["W" + str(l)] = parameters["W" + str(l)] - alpha*(v_corrected["dW" + str(l)]/(np.sqrt(s_corrected["dW" + str(l)])+epsilon))
#         parameters["b" + str(l)] = parameters["b" + str(l)] - alpha*(v_corrected["db" + str(l)]/(np.sqrt(s_corrected["db" + str(l)])+epsilon))
        

#     return parameters, v, s, v_corrected, s_corrected


# v, s = initialize_adam(params)
# parameters, v, s, vc, sc  = update_parameters_with_adam(parametersi, grads, vi, si, t, learning_rate, beta1, beta2, epsilon)
