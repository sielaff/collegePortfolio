import numpy as np
import matplotlib.pyplot as plt
import sys
import time

x = []
y = []

fName = sys.argv[1]
data = np.genfromtxt(fName, delimiter=',')
for a in data:
    x.append(a[0])
    y.append(a[1])
    
# now x and y are populated with the points

def min_max(list):
    max = list[0]                                        # normalize the list
    min = list[0]
    for a in list:
        if a > max:
            max = a
        if a < min:
            min = a
    for a in range(0,len(list)):
        list[a] = (list[a]-min)/(max-min) 
    return list

def square_error(m, b, x_list, y_list):
    error = 0
    for i in range(0, len(x_list)):                       # sigma to calculate total error
        error += (y_list[i] - (m * x_list[i] + b))**2    
    return error

def gradient(mb, x_list, y_list, alpha):
    total_b_deriv = 0
    total_m_deriv = 0
    m_new = mb[0]
    b_new = mb[1]	
    total_error = square_error(m_new, b_new, x_list, y_list)
    b_deriv = 0
    m_deriv = 0						   # calculate partial derivatives
    for i in range(0, len(x_list)):
        m_deriv += (-2*x_list[i]*(y_list[i]-(m_new*x_list[i]+b_new)))/8
        b_deriv += (-2*(y_list[i]-(m_new*x_list[i]+b_new)))/8
    
    mb[0] = m_new - m_deriv*alpha
    mb[1] = b_new - b_deriv*alpha			   # update m and b
    return

def model(x_list, y_list):
    #b = np.random.rand(1)
    #m = np.random.rand(1)
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    b = 0
    m = 0
    alpha = 0.01
    iter = 100000
    new_x = min_max(x_list)
    new_y = min_max(y_list)
  
    plt.plot(x, y, 'ro')
    plt.show()
  
    for i in range (0, iter): 
        mb = [m, b]
        gradient(mb, new_x, new_y, alpha)
        m = mb[0]
        b = mb[1]

    	x_plot = [0, 1]
  	y_plot = [b, m + b]
  	#plt.plot(x_plot, y_plot, '--')
  	
	ln, = ax.plot(x_plot)
        ax.set_xlim([0,1])
	ln.set_ydata(y_plot)
	plt.pause(0.00001)
	ln.remove()
	#fig.canvas.draw()
    return

model(x, y)
