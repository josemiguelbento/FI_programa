from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import math
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import sympy as sym

def visualize(l,m):

    n = 200
    phi = np.linspace(0, 2 * np.pi, n)
    theta = np.linspace(0, np.pi, n)

    [PHI, THETA] = np.meshgrid(phi, theta)


    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - m)) / (math.factorial(l + m)))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (m / 2)
    P_ml = ((-1) ** m / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, m + l)

    P_ml = sym.lambdify(s, P_ml)
    Y_ml = a * np.exp(1j * m * PHI) * P_ml(np.cos(THETA))
    
    Y_ml = np.where(np.isnan(Y_ml), 0, Y_ml)
    
    Y_ml_real = Y_ml.real
    Y_ml_imag = Y_ml.imag
    Y_ml_abs = np.abs(Y_ml)


    x1 = abs(Y_ml_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_ml_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_ml_real) * np.cos(THETA)

    x2 = abs(Y_ml_imag) * np.sin(THETA) * np.cos(PHI)
    y2 = abs(Y_ml_imag) * np.sin(THETA) * np.sin(PHI)
    z2 = abs(Y_ml_imag) * np.cos(THETA)

    x3 = Y_ml_abs * np.sin(THETA) * np.cos(PHI)
    y3 = Y_ml_abs * np.sin(THETA) * np.sin(PHI)
    z3 = Y_ml_abs * np.cos(THETA)

    #############################
    scale = 5

    dx31 = scale*x3.max() - scale*x1.min() + 1
    
    dx12 = scale*x1.max() - scale*x2.min() + 1
    
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x3*scale, y3*scale, z3*scale, scalars=Y_ml_abs, colormap='jet')
    #mlab.text3d(-0.4, 0, 1.8, f'|Y{l}{m}|', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    #mlab.colorbar(orientation='vertical')

    mlab.mesh((x1*scale+dx31), y1*scale, z1*scale, scalars=Y_ml_real, colormap='jet')
    #mlab.text3d(-0.4+3.8, 0, 1.8, f'Re[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x2*scale+dx31+dx12, y2*scale, z2*scale, scalars=Y_ml_imag, colormap='jet')
    #mlab.text3d(7.4, 0, 1.8, f'Im[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))


    mlab.text3d(-0.2, 0, scale*z3.max()+1, 'Abs', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31, 0, scale*z3.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31+dx12, 0, scale*z3.max()+1, 'Im', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    

    mlab.view(-85,85,30)
    mlab.show()

def draw_coeff(coeff):
    
    n = 200
    phi = np.linspace(0, 2 * np.pi, n)
    theta = np.linspace(0, np.pi, n)

    [PHI, THETA] = np.meshgrid(phi, theta)
    
    R = PHI * 0
    for l in range(len(coeff)-1):
        for m in range(-l,l):
            R = R + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA)

    visualize_final(R, THETA, PHI)



def get_spherical_harmonic(l, m, PHI, THETA):

    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - m)) / (math.factorial(l + m)))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (m / 2)
    P_ml = ((-1) ** m / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, m + l)

    P_ml = sym.lambdify(s, P_ml)
    

    Y_ml = a * np.exp(1j * m * PHI) * P_ml(np.cos(THETA))

    return Y_ml

def visualize_final(R, THETA, PHI):
    
    R = np.where(np.isnan(R), 0, R)

    Y_ml_real = R.real
    Y_ml_imag = R.imag
    Y_ml_abs = np.abs(R)


    x1 = abs(Y_ml_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_ml_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_ml_real) * np.cos(THETA)

    x2 = abs(Y_ml_imag) * np.sin(THETA) * np.cos(PHI)
    y2 = abs(Y_ml_imag) * np.sin(THETA) * np.sin(PHI)
    z2 = abs(Y_ml_imag) * np.cos(THETA)

    x3 = Y_ml_abs * np.sin(THETA) * np.cos(PHI)
    y3 = Y_ml_abs * np.sin(THETA) * np.sin(PHI)
    z3 = Y_ml_abs * np.cos(THETA)

    #############################
    scale = 5

    dx31 = scale*x3.max() - scale*x1.min() + 1
    
    dx12 = scale*x1.max() - scale*x2.min() + 1
    
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x3*scale, y3*scale, z3*scale, scalars=Y_ml_abs, colormap='jet')
    #mlab.text3d(-0.4, 0, 1.8, f'|Y{l}{m}|', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    #mlab.colorbar(orientation='vertical')

    mlab.mesh((x1*scale+dx31), y1*scale, z1*scale, scalars=Y_ml_real, colormap='jet')
    #mlab.text3d(-0.4+3.8, 0, 1.8, f'Re[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x2*scale+dx31+dx12, y2*scale, z2*scale, scalars=Y_ml_imag, colormap='jet')
    #mlab.text3d(7.4, 0, 1.8, f'Im[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))


    mlab.text3d(-0.2, 0, scale*z3.max()+1, 'Abs', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31, 0, scale*z3.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31+dx12, 0, scale*z3.max()+1, 'Im', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    

    mlab.view(-85,85,30)
    mlab.show()


if __name__ == "__main__":
    l = 3
    m = 1
    coeff = [[0.37],
             [0.020, 0.052, 0.020],
             [0.068, 0.012, 0.012, 0.012, 0.068],
             [0.0052, 0.0025, 0.0032, 0.0026, 0.0032, 0.0025, 0.0052]]
    #visualize(l,m)
    draw_coeff(coeff)