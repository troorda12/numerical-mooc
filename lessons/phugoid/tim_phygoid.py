#code for propagating phugoid motion via trammel method

import numpy
import matplotlib.pyplot as plt

def radius_of_curvature(z, zt, C):
    '''calculates the radius of curvature of flight path at any point
    
    Inputs:
    z: float
        vertical position (positive z points down)
    zt: float
        initial vertical position
    C: float
        constant of integration
        
    Output:
    raddius: float
        radius of curvature'''
        
    return zt / (1./3 - (C/2.)*(zt/z)**1.5)
    
def rotate(x, z, xC, zC, angle):
    '''returns new position of a point under rotation along a radial line
    
    Inputs:
    x: float
        previous x-position of the point
    z: float
        previous z-position of the point
    xC: float
        x-location of the center of rotation
    zC: float
        z-location of the center of rotation
    angle: float
        angle of rotation
        
    Outputs:
    x_new: float
        new x-location of the rotated point
    z_new: float
        new y-location of the rotated point'''
        
    dx = x - xC
    dz = z - zC
    
    xN =  dx*numpy.cos(angle) + dz*numpy.sin(angle)
    zN = -dx*numpy.sin(angle) + dz*numpy.cos(angle)
    
    x_new = xC + xN
    z_new = zC + zN
    
    return x_new, z_new
    
def plot_flight_path(zt, z0, theta0):
    '''Plots the flight path.
    
    Inputs:
    zt: float
        trim height of the aircraft
    z0: float
        initial height of the aircraft
    theta0: float
        initial orientation of the aircraft
        
    Outputs:
    N/A'''
    
    #arrays for storing the coordinates of the flight path
    N = 1000    #number of plotting points
    x = numpy.zeros(N)
    z = numpy.zeros(N)
    
    #initial conditions
    x[0] = 0.
    z[0] = z0
    theta = theta0
    
    #calculate constant of integration
    C = (numpy.cos(theta) - (1./3)*(z[0]/zt))*(z[0]/zt)**.5
    
    #incremental distance along the flight path (curvilnear)
    ds = 1
    
    #obtain the curvilinear coordinates
    for i in range(1,N):
        #remember that the z-coordinate is positive-down
        normal = numpy.array([-numpy.sin(theta), -numpy.cos(theta)])
        R = radius_of_curvature(z[i-1], zt, C)
        center = numpy.array([x[i-1]+normal[0]*R, z[i-1]+normal[1]*R])
        dtheta = ds/R
        x[i], z[i] = rotate(x[i-1], z[i-1], center[0], center[1], dtheta)
        theta = theta + dtheta
        
    #plot
    plt.figure(figsize=(10,6))
    plt.plot(x, -z, color = 'k', ls='-', lw=2.0, label="$z_t=\ %.1f,\\,z_0=\ %.1f,\\,\\theta_0=\ %.2f$" % (zt, z[0], theta0))
    plt.axis('equal')
    plt.title("Flight path for $C$ = %.3f" % C, fontsize=18)
    plt.xlabel("$x$", fontsize=18)
    plt.ylabel("$z$", fontsize=18)
    plt.legend()
    plt.show()
    

plot_flight_path(64, 16, .9)