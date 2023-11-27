from hello import *
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import time 
start = time.time()

def shuffle_in_unison(a, b):
        assert len(a) == len(b)
        shuffled_a = np.empty(a.shape, dtype=a.dtype)
        shuffled_b = np.empty(b.shape, dtype=b.dtype)
        permutation = np.random.permutation(len(a))
        for old_index, new_index in enumerate(permutation):
            shuffled_a[new_index] = a[old_index]
            shuffled_b[new_index] = b[old_index]
        return shuffled_a, shuffled_b

def build_model():
    
    neurons = 24
 

    # Initialize weights and biases for the neural network
    initializer = tf.initializers.GlorotUniform()
    w1 = tf.Variable(initializer(shape=(m, neurons)), dtype=tf.float32)
    b1 = tf.Variable(tf.zeros(shape=(neurons)), dtype=tf.float32)
    w2 = tf.Variable(initializer(shape=(neurons, neurons*4)), dtype=tf.float32)
    b2 = tf.Variable(tf.zeros(shape=(neurons*4)), dtype=tf.float32)
    w3 = tf.Variable(initializer(shape=(neurons*4, neurons*4)), dtype=tf.float32)
    b3 = tf.Variable(tf.zeros(shape=(neurons*4)), dtype=tf.float32)
    w4 = tf.Variable(initializer(shape=(neurons*4, 1)), dtype=tf.float32)
    b4 = tf.Variable(tf.zeros(shape=(1)), dtype=tf.float32)

    # Define model architecture
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=m),
        tf.keras.layers.Dense(units=neurons, activation='relu'),
        tf.keras.layers.Dense(units=neurons*4, activation='relu'),
        tf.keras.layers.Dense(units=neurons*4, activation='relu'),
        tf.keras.layers.Dense(units=1, activation='sigmoid'),
    ])
    
  
    
    model.layers[0].set_weights([w1, b1])
    model.layers[1].set_weights([w2, b2])
    model.layers[2].set_weights([w3, b3])
    model.layers[3].set_weights([w4, b4])

    return model


n, m = np.shape(traindata)


x = traindata
# x , outcome = shuffle_in_unison(x, outcome)
        
print(np.shape(x))


model = build_model()
model.compile(optimizer='adam', loss='binary_crossentropy')

history = model.fit(traindata,trainoutcome,epochs = 20)

gry = np.zeros(20)
ct = 0
grx = np.zeros(20)
for epoch, loss in enumerate(history.history['loss']):
    # print('Epoch {}: training loss: {}'.format(epoch+1, loss))
    # print(loss)
    gry[ct] = loss
    grx[ct] = ct + 1
    ct += 1

plt.plot(grx, gry)
plt.xlabel('Epoch number')
plt.ylabel('Loss')
plt.show()
y_hat = model.predict(x)


ct = 0
ctdum = 0
totct = 0
for i in traindata:
    outputprob = y_hat[totct]
    if outputprob > 0.6:
        if trainoutcome[totct] == 0 and traindata[totct][0] > 60 :
            ct += 1
        ctdum += 1
    elif outputprob < 0.4 and traindata[totct][0] > 60:
        if trainoutcome[totct] == 1:
            ct += 1
        ctdum += 1
    totct += 1
    
print("Train data accuracy")
print(100 - (ct / ctdum) * 100)


ct = 0
ctdum = 0
totct = 0
y_hat = model.predict(testdata)

for i in testdata:
    outputprob = y_hat[totct]
    if outputprob > 0.6:
        if testoutcome[totct] == 0 :
            ct += 1
        ctdum += 1
    elif outputprob < 0.4:
        if testoutcome[totct] == 1:
            ct += 1
        ctdum += 1
    totct += 1


print("Test data accuracy ")    
print(100 - (ct / ctdum) * 100)


neuralnetacc = (100 - (ct / ctdum) * 100)

end = time.time()
print("Time taken by this algorithm ")
print(end - start)


