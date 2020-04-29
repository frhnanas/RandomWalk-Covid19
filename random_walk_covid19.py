# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 04:21:48 2020

@author: Farhan
"""


import numpy as np
import matplotlib.pyplot as plt
from random import random

x_min = 0
x_max = 100

y_min = 0
y_max = 100

x_range = x_max - x_min
y_range = y_max - y_min

pos_xy = []
posisi = []

n_particles = 10 #number particle
n_iteration = 100 #number iteration
for i in range(n_particles):
    x_pos = np.random.randint(x_min, x_max)
    y_pos = np.random.randint(y_min, y_max)
    pos_xy.append([x_pos, y_pos])
posisi.append(pos_xy)

for i in range(n_iteration):
    pos_trans = []
    for j in range(n_particles):
        x = posisi[i][j][0]
        y = posisi[i][j][1]
        
        rand = random()
        #right
        if(rand<=0.25):
            x = x + 1
        #down
        elif(rand<=0.50):   
            y = y - 1
        #left
        elif(rand<=0.75):
            x = x - 1
        #up
        else:
            y = y + 1
            
            
        if (x > x_max): 
            x = x - x_range
        if (x < 0): 
            x = x + x_range
            
        if (y > y_max):
            y = y - y_range
        if (y < 0): 
            y = y + y_range
            
    
        pos_trans.append([x,y])
    posisi.append(pos_trans)
   
fig, ax = plt.subplots(figsize=(10,10))
for i in range(n_iteration):
    for j in range(n_particles):
        ax.scatter(posisi[i][j][0], posisi[i][j][1])
plt.title('2D Random Walk Simulation with 4 Direction')
plt.grid()
plt.show()