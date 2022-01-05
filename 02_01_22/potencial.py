import math
import numpy as np
import sympy as sym
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d import Axes3D
from mayavi import mlab
from mpl_toolkits.basemap import Basemap
from tvtk.api import tvtk

# Plot
#################################################################################################################

def matplot_mollweide(X, Y, Values, cmap):
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(X, Y, Potencial, cmap=cm.RdBu)
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    fig.colorbar(clrbr, orientation='horizontal')
    ax.grid(color='k')

#################################################################################################################

def get_ass_leg(l, m, THETA): # egm96 norm for a (beacuase of coefficients with this norm)
    if m == 0: 
        a = np.sqrt( (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    else: 
        a = np.sqrt( 2 *  (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    s = sym.Symbol('s')
    G = (s ** 2 - 1) ** l
    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = (1 / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)
    P_lm = sym.lambdify(s, P_lm)

    return (a * P_lm(np.sin(THETA)))

def read_file(name, lmax):
    path = 'data/' + name
    with open(path, 'r') as infile:
        lines = infile.readlines()
    line = np.array([lin.split() for lin in lines])
    arr_size = int((4 + lmax) / 2 * (lmax - 1))

    l = line[0:arr_size,0].astype('int64')
    m = line[0:arr_size,1].astype('int64')
    C = line[0:arr_size,2].astype('float64')
    S = line[0:arr_size,3].astype('float64')

    return l, m, C, S

def get_pot(l, m, C, S, THETA, PHI, MU, R_T, r):
    arr_size = len(l)
    # Initialize U=1 because of J0 (The sum when l=0,m=0 we have Plm=1 since Cnm=1(I think) what is inside of sum stays 1, in the end its multiplied by MU/r)??????
    U = 1
    for i in range(arr_size):
        U = U + (R_T / r)**l[i] * get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    U = U * MU / r
    return -U

def get_cart(PHI, THETA, r):
    X = r * np.cos(THETA) * np.cos(PHI)
    Y = r * np.cos(THETA) * np.sin(PHI)
    Z = r * np.sin(THETA)

    return X, Y, Z

def get_undulation(THETA, PHI, MU, R_T):
    lmax = 16
    l, m, C, S = read_file('earth_egm96_to360.ascii.txt', lmax)
    Potencial = -get_pot(l, m, C, S, THETA, PHI, MU, R_T, R_T)
    zonal_ind = np.where(m == 0)
    zonal_l = l[zonal_ind]
    zonal_m = m[zonal_ind]
    zonal_C = C[zonal_ind]
    zonal_S = S[zonal_ind]
    zonal_Potencial = -get_pot(zonal_l, zonal_m, zonal_C, zonal_S, THETA, PHI, MU, R_T, R_T)
    T = Potencial - zonal_Potencial
    N = R_T**2 * T / MU # [m]

    return N


# EARTH EGM96
if __name__ == "__main__":

    # Gravitational parameter of Earth [m^3 s^-2]
    MU = 3.986004405e14 

    # Mean equitorial radius [m]
    R_T = 6.3781363e6

    # Calculate potencial Radius [m]
    r =  R_T + 100e3

    # max ind
    lmax = 5

    # Read File
    l, m, C, S = read_file('earth_egm96_to360.ascii.txt', lmax)
    #C[0] = 0

    # Define phi & theta
    n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    theta = np.linspace(-np.pi/2, np.pi/2, n)
    [PHI, THETA] = np.meshgrid(phi, theta)

    # Potencial
    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, r)

    # Potencial mollweide
    """fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial, cmap=cm.RdBu)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Potencial 3D
    """X, Y, Z = get_cart(PHI, THETA, r)
    norm = colors.Normalize()
    ax = plt.subplot(111, projection = '3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=cm.RdBu(norm(Potencial)))
    plt.show()

    # Potencial for 2 different r
    r2 =  R_T + 105e3
    Potencial2 = get_pot(l, m, C, S, THETA, PHI, MU, R_T, r2)

    if Potencial.min() < Potencial2.min():
        vmin = Potencial.min()
    else:
        vmin = Potencial2.min()

    if Potencial.max() > Potencial2.max():
        vmax = Potencial.max()
    else:
        vmax = Potencial2.max()

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111, projection = 'mollweide')
    ax.pcolormesh(PHI, THETA, Potencial2, cmap=cm.RdBu, vmin=vmin, vmax=vmax)
    ax.set_title(f'h = {(r2-R_T)*1e-3} Km')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(np.linspace(vmin,vmax,200))
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')

    plt.show()"""

    # Earth format 3D
    """arr_size = len(l)
    f = 0
    for i in range(arr_size):
        f = f + get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    X, Y, Z = get_cart(PHI, THETA, 150*f+1)

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=f, colormap='seismic')
    mlab.view(-85,85,30)
    mlab.show()"""

    # Earth format mollweide
    """arr_size = len(l)
    f = 0
    for i in range(arr_size):
        f = f + get_ass_leg(l[i], m[i], THETA) * (C[i] * np.cos(m[i] * PHI) + S[i] * np.sin(m[i]* PHI))
    X, Y, Z = get_cart(PHI, THETA, 150*f+1)
    
    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(PHI, THETA, f, cmap=cm.seismic)
    clrbr = cm.ScalarMappable(cmap=cm.seismic)
    clrbr.set_array(f*100000)
    fig.colorbar(clrbr, orientation='horizontal')
    ax.grid(color='k')
    plt.show()"""

    # Potencial(r) THETA = 0
    """n = 200
    phi = np.linspace(-np.pi, np.pi, n)
    r = np.linspace(R_T, R_T + 5000e3, n)
    [PHI, R] = np.meshgrid(phi, r)
    THETA = 0

    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R)
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Y, Potencial, cmap=cm.RdBu)
    ax.set_title(f'elevation angle = {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Potencial(r) PHI = 0
    """theta = np.linspace(-np.pi/2, np.pi/2, n)
    r = np.linspace(R_T, R_T + 5000e3, n)
    [THETA, R] = np.meshgrid(theta, r)
    PHI = 0

    Potencial = get_pot(l, m, C, S, THETA, PHI, MU, R_T, R)
    X, Y, Z = get_cart(PHI, THETA, R*1e-3)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    ax.pcolormesh(X, Z, Potencial, cmap=cm.RdBu)
    ax.set_title(f'azimuth angle = {0}')
    ax.set_xlabel('X [Km]')
    ax.set_ylabel('Y [Km]')
    clrbr = cm.ScalarMappable(cmap=cm.RdBu)
    clrbr.set_array(Potencial)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Gravitational Potencial [Nm/kg]')
    ax.grid(color='k')
    plt.show()"""

    # Undulation  [m]
    """N = get_undulation(THETA, PHI, MU, R_T)

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, N, cmap=cm.jet)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array([-100, 80])
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Geoid height [m]')
    ax.grid(color='k')
    plt.show()"""
    
    """X, Y, Z = get_cart(PHI, THETA, 10000*N+R_T)

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=N, colormap='jet')
    mlab.show()"""

    # Undulation (perfect sphere)
    rm = 6371.0088e3
    Pot = -get_pot(l, m, C, S, THETA, PHI, MU, rm, rm)
    R = rm**2 * Pot / MU

    fig=plt.figure(figsize=(10,10))
    ax = plt.subplot(111)
    m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,\
            llcrnrlon=-180,urcrnrlon=180,resolution='c')
    m.drawcoastlines()
    ax.pcolormesh(PHI*180/np.pi, THETA*180/np.pi, R, cmap=cm.jet)
    clrbr = cm.ScalarMappable(cmap=cm.jet)
    clrbr.set_array(R*1e-3)
    cbar = fig.colorbar(clrbr, orientation='horizontal')
    cbar.set_label('Ellipsoid [Km]')
    ax.grid(color='k')
    plt.show()

    X, Y, Z = get_cart(PHI, THETA, R)
    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()
    mlab.mesh(X, Y, Z, scalars=R, colormap='jet')
    mlab.show()

