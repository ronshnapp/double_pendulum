# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from numpy import sin, cos
import matplotlib.pyplot as plt





#================================
# the basic equations of motion:
#================================

def x_dot_dot(x,y,x_dot,y_dot):
    num = -sin(x) - sin(x-y) * ( cos(y) + y_dot**2 + x_dot**2*cos(x-y))
    denum = 1.0 + sin(x-y)**2
    return num / denum

def y_dot_dot(x,y,x_dot,y_dot):
    return x_dot**2 * sin(x-y) - x_dot_dot(x,y,x_dot,y_dot)*cos(x-y) - sin(y)





#======================================
# the class from handling the pendulum:
#======================================

class double_pendulum():
    '''
    A class used to handel the pendulum solutions. It's methods are used
    for integrating the equation of motion, and it can be used to generate
    series of images of the double pendulum for generating gifs or videos.
    
    inputs:
        x0, y0, x_dot0, y_dot0, floats. Initial conditions stading for angle
        of the first and second pendulums and their angular velocities 
        respectively.
        
        dt - a constant time step for the integration. Accordingly this solver
        does not check for convergence.
    '''
    
    
    def __init__(self, x0, y0, x_dot0, y_dot0, dt):
        
        self.t = [0.0]
        self.x = [x0]
        self.y = [y0]
        self.x_dot = [x_dot0]
        self.y_dot = [y_dot0]    
        self.dt = dt 


    def step(self):
        '''
        solves and updates a single timestep in the pendulum dynamics.
        This uses the 2nd order Runge Kuta method for integration. This direct
        implementation is quicker than using numpy arrays.
        '''
        xi = self.x[-1]
        yi = self.y[-1]
        x_doti = self.x_dot[-1]
        y_doti = self.y_dot[-1]
        
        dx_i_m = x_doti * self.dt
        dy_i_m = y_doti * self.dt
        dx_dot_i_m = x_dot_dot(xi, yi, x_doti, y_doti) * self.dt
        dy_dot_i_m = y_dot_dot(xi, yi, x_doti, y_doti) * self.dt
    
        x_m = xi + dx_i_m
        y_m = yi + dy_i_m
        x_dot_m = x_doti + dx_dot_i_m
        y_dot_m = y_doti + dy_dot_i_m
    
        dx_i = x_dot_m * self.dt
        dy_i = y_dot_m * self.dt
        dx_dot_i = x_dot_dot(x_m, y_m, x_dot_m, y_dot_m) * self.dt
        dy_dot_i = y_dot_dot(x_m, y_m, x_dot_m, y_dot_m) * self.dt
    
        self.t.append(self.t[-1] + self.dt)
        self.x.append(xi + dx_i)
        self.y.append(yi + dy_i)
        self.x_dot.append(x_doti + dx_dot_i)
        self.y_dot.append(y_doti + dy_dot_i)
        
        
    def plot_dp_traces(self, dt, t0, tf, alpha=0.4, s=2):
        '''
        will trace the position of the double pendulum rod tips between times
        t0 and tf, and time steps of dt.
        alfa and s determine the dots transperancy and size
        '''
        L = 1.0
        x, y = np.array(self.x), np.array(self.y)
        x1, y1 = L*sin(x), -L*cos(x)
        x12, y12 = L*sin(y), -L*cos(y)
        x2, y2 = x1+x12, y1+y12
        
        t = np.array(self.t)
        jf = np.where(t>=tf)[0][0]
        j0 = np.where(t>=t0)[0][0]
        dj = np.where(t>=dt)[0][0]
        
        fig, ax = plt.subplots()
        ax.scatter(x1[j0:jf:dj], y1[j0:jf:dj], color='r', s=s, alpha=alpha)
        ax.scatter(x2[j0:jf:dj], y2[j0:jf:dj], color='b', s=s, alpha=alpha)
        ax.set_xlim([-2.1*L, 2.1*L])
        ax.set_ylim([-2.1*L, 2.1*L])
        ax.set_aspect('equal')
        fig.set_size_inches(8,8)
        return fig, ax
        
    
    def calculate_kinetic_energy(self):
        '''
        Will calcualte and return the kinetic energy of the double pendulum
        system: Ek = 0.5*(V1^2 + V2^2). Returns result as a numpy 
        array.
        '''
        L = 1.0
        xd, yd = np.array(self.x_dot) , np.array(self.y_dot)
        
        e1 = 0.5 * L**2 * xd**2
        tmp = xd**2 + yd**2 + xd*yd* cos(np.array(self.x) - np.array(self.y))
        e2 = 0.5 * L**2 * tmp
        return e1 + e2
    
    
    def calculate_potential_energy(self):
        '''
        Will calcualte and return the potential energy of the double pendulum
        system: Ek = g*H = (L/T)^2 * (-2 cos(x) - cos(y)).
        '''
        return -2*cos(self.x) - cos(self.y)
    
    
    def plot_one_frame(self, ax, i):
        '''
        will plot the pendulum at iteration i onto a given matplotlib 
        AxesSubplot, ax. used by make_images.
        '''
        L = 1.0
        x, y = self.x[i], self.y[i]
        x1, y1 = L*sin(x), -L*cos(x)
        x12, y12 = L*sin(y), -L*cos(y)
        x2, y2 = x1+x12, y1+y12
    
        ax.plot([0,x1], [0,y1], 'r-', lw=.6)
        ax.plot([x1, x2], [y1, y2], 'b-', lw=.6)
        ax.scatter([0, x1, x2], [0, y1, y2], s=[2,16,16], color=['k','r','b'])
    
        ax.set_xlim([-2.1*L, 2.1*L])
        ax.set_ylim([-2.1*L, 2.1*L])
        ax.set_aspect('equal')
        
    def make_images(self, dt, t0, tf):
        '''
        will generate a series of images with the pendulum state and save
        them on the hard drive. 
        the series begins at time t0, end at tf, and the time interval is dt.
        '''
        fig, ax = plt.subplots()
        
        t = np.array(self.t)
        jf = np.where(t>=tf)[0][0]
        j0 = np.where(t>=t0)[0][0]
        dj = np.where(t>=dt)[0][0]
        
        N = int(np.ceil((jf-j0)/dj))
        print('saveing %d frame: %d --> %d'%(N, j0, jf))
        
        for e, i in enumerate(range(j0, jf, dj)):
            self.plot_one_frame(ax, i)
            fig.savefig('./images/im%04d.jpg'%(e+1))
            ax.clear()
        plt.close(fig)
        







if __name__ == '__main__':
    
    
    import time
    start_time = time.time()
    
    steps = 6280*4*5
    dt = 0.00005
    dp = double_pendulum(1.5, 2.25, 0.0, 0.0, dt)
    for i in range(steps):
        dp.step()
        
    t = np.array(dp.t)
    x = np.array(dp.x)
    y = np.array(dp.y)
    x_dot = np.array(dp.x_dot)
    y_dot = np.array(dp.y_dot)
    
    print('solved %d steps in %.2f seconds' %(steps,time.time() - start_time))


    #fig, ax = plt.subplots()
    #ax.plot(t[::10],x[::10])
    #ax.plot(t[::10],y[::10])
    
    
    
    
    
    
    