#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 18:04:21 2022

@author: rpasken
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def ddx(data,i,j,delta):


def ddy(data,i,j,delta):
        
#
# Ask for the name of the file with the data
#

#file_name = input("Enter the filename" )
file_name = "geopot.dat"
#
# Open and then read the data from the file. Specify that each element is separated
# by a comma
#

geopot = np.loadtxt(file_name, delimiter=",")

#
# Technically I already know how many rows and columns there are in the dataset. The
# next few lines allow me to make the code general and more elegant.
#

num_lats = len(geopot)
num_lons = len(geopot[0])

xm,ym = np.meshgrid(np.arange(num_lons),np.arange(num_lats))

v_f = np.empty((num_lats,num_lons))
u_f = np.empty((num_lats,num_lons))
v_e = np.empty((num_lats,num_lons))
u_e = np.empty((num_lats,num_lons))
#
#For now assume delta x and delta y are 1
#

delta = 400000.0
coriolis = 1e-4

for i in range(num_lats):
    for j in range(num_lons):
        if j > 0 and j < num_lons-1:
            v_e[i,j] = (geopot[i,j+1] - geopot[i,j-1]) / (2.0 * delta)
        elif j == 0:
            v_e[i,j] = (geopot[i,j+1] - geopot[i,j]) / delta
        elif j == num_lons-1:
            v_e[i,j] = (geopot[i,j] - geopot[i,j-1]) / delta
        
        if i > 0 and i < num_lats-1:
            u_e[i,j] = (geopot[i+1,j] - geopot[i-1,j]) / (2.0 * delta)
        elif i == 0:
            u_e[i,j] = (geopot[i+1,j] - geopot[i,j]) / delta
        elif i == num_lats-1:
            u_e[i,j] = (geopot[i,j] - geopot[i-1,j]) / delta
        u_e[i,j] = -u_e[i,j] / coriolis
        v_e[i,j] = v_e[i,j] / coriolis
        
        u_f[i,j] = -ddy(geopot,i,j,delta) / coriolis
        u_f[i,j] = ddx(geopot,i,j,delta) / coriolis


speed_e= np.sqrt(u_e * u_e + v_e * v_e) 
speed_f = np.sqrt(u_f * u_f + v_f * v_f)         
fig = plt.figure()
plt.contourf(xm,ym,speed_e-speed_f)
plt.colorbar()
plt.show()