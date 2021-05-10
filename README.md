# README

This is a python script for numerically integrating the equations of motion of a double pendulum, and presenting the results in cool and instructive ways. This code could be good for undergraduate or higher degree students in science disciplines who wish to become more familiar with complex dynamical systems. It could also be used by instructors to produce animations of the double pendulum. Some knowledge in Python is desirable. 

The project is developed by Ron Shnapp. First lines of code written on May, 2021.

## Usage

### Description

The script double_pendulum.py has two functions that represent the dynamical system, and a class that is used to integrate the equations and present the results. Edit the script in order to insert initial conditions, number of steps etc. Then, when the script is run, the integration is performed straight away and the results are stored inside the class instance. After thta, one can use the built methods to visualize the results.

### Requirements

To run the code you'll need Python and installed with NumPy. For visualizing static plots you'll need to have Matplotlib as well. All of these are easily obtained using e.g. the anaconda distribution.  

To make animations, a third party video editting software, such as ffmpeg (https://ffmpeg.org/), is currently needed. MoviePy can be used but it is not necessary. See details below. 

### gifs and animations

There are two options to make gifs and animations of your results:

1. The double_pendulum.make_images() method can be used to save series of images of the pendulums on the hard drive. After that use video a editing software such as ffmpeg to generate the animations in a verity of different formats.
2. MoviePy can be used to generate animations of the results using the double_pendulum.animate() method. Note that ffmpeg is still needed because it is used by MoviePy.

## The equation of motion

The motion of the pendulum is modeled using Newton's third law as two point masses that are connected with rigid massless rods. The position of the pendulums are specified uniquely through the angle each rod is making with respect to a vertical axis. Denoting by $x$ the angle of the first pendulum and by $y$ that of the second, the equations of motion are: 

$$ \ddot{x}= \frac{-\omega^2 \sin{(x)} - \sin{(x-y)}[\omega^2 \cos{(y)}+\dot{y}^2+\dot{x}^2\cos{(x-y)}]}{1+\sin^2(x-y)}$$

$$ \ddot{y}= -\omega^2 \sin{(y)} + \dot{x}^2 \sin{(x-y)} - \ddot{x}\cos{(x-y)}$$

where $\omega ^2 = g/l$ is a characteristic frequency. Then, the double pendulum system has a four dimensional phase space - $(x,y,\dot{x},\dot{y})$. The equations can be derived either writing the forces in polar coordinates and using Newton's law, or by writing the Euler–Lagrange equation - try it out!

For now, the script solves only the case where the two pendulums  have the  same rod length and thus the same $\omega$.

## Numerical integration

The script currently uses a simple 2nd order Runge-Kuta method to advance the state of the pendulum in time. For now, the time step in the integration is constant and there are no automatic validations for convergence. This means that the user has to insert a timestep argument, and make sure that it is small enough so that no errors or blow ups will occur. A possible extension of this project is to include automatic timestep choices, make functions for validations of convergence, and turn the integration method to higher order. 

## Spread it around

Did you use this code to find something amazing? This is great, and I'd love to hear about it! But also, it's important to spread it around to you friends. Help other people find the fascination in science by sharing tools you like. 

## Contributions

Contributions to this project are most welcome! Also, feel free to fork, extend and transform, and share this project as you see fit.

