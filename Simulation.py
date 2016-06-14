import numpy as np
import re
import math
import operator
import time

f1 = open('Neural_network_training\Theta1.txt','r')
Theta1=np.matrix([list(map(float,line.split(','))) for line in f1])
f1.close()
f2 = open('Neural_network_training\Theta2.txt','r')
Theta2=np.matrix([list(map(float,line.split(','))) for line in f2])
f2.close()
print(Theta1)
print(Theta2)