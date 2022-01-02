from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import math
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import sympy as sym

def visualize(Y_lm_real, THETA, PHI):
    scale = 1000
    scale_deform = 250
    Y_lm_real = Y_lm_real.real
    r = 1
    x = r*np.sin(THETA) * np.cos(PHI)
    y = r*np.sin(THETA) * np.sin(PHI)
    z = r*np.cos(THETA)

    x11 = (r+Y_lm_real*scale_deform) * np.sin(THETA) * np.cos(PHI)
    y11 = (r+Y_lm_real*scale_deform) * np.sin(THETA) * np.sin(PHI)
    z11 = (r+Y_lm_real*scale_deform) * np.cos(THETA)

    x1 = abs(Y_lm_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_lm_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_lm_real) * np.cos(THETA)

    

    dz1 = 0
    d = -scale*z1.min() + z.max() + 2
    if d > dz1:
        dz1 = d
    
    
    dz2 = 0
    d = -z.min() + z11.max() + 2
    if d > dz2:
        dz2 = d
    
    
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x1*scale, y1*scale, z1*scale, scalars=Y_lm_real, colormap='jet')

    mlab.mesh(x, y, z-dz1, scalars=Y_lm_real, colormap='jet')

    mlab.mesh(x11, y11, z11-dz1-dz2, scalars=Y_lm_real, colormap='jet')
    

    mlab.text3d(-0.2, 0, scale*z1.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.text3d(scale*x1.min()-2.5, 0, 0, 'R=Ylm', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x1.min()-2.5, 0, -dz1, 'Unit Sphere', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x1.min()-2.5, 0, -dz1-dz2, 'R=(1+Ylm)', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.view(-85,85,30)
    mlab.show()

def draw_coeff(coeff):
    
    n = 200
    phi = np.linspace(0, 2 * np.pi, n)
    theta = np.linspace(0, np.pi, n)

    [PHI, THETA] = np.meshgrid(phi, theta)
    
    R = PHI * 0
    for l in range(len(coeff)):
        for m in range(-l,l+1):
            R = R + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA)

    #visualize_final(R, THETA, PHI)
    visualize(R, THETA, PHI)



def get_spherical_harmonic(l, m, PHI, THETA):

    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - abs(m))) / (math.factorial(l + abs(m))))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = ((-1) ** abs(m) / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)

    P_lm = sym.lambdify(s, P_lm)
    Y_lm = a * np.exp(1j * abs(m) * PHI) * P_lm(np.cos(THETA))
    if m<0: Y_lm = (-1)**m * Y_lm.conj()

    return Y_lm

def visualize_final(R, THETA, PHI):
    

    Y_lm_real = R.real
    Y_lm_imag = R.imag
    Y_lm_abs = np.abs(R)


    x1 = abs(Y_lm_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_lm_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_lm_real) * np.cos(THETA)


    #############################
    scale = 3

    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()


    mlab.mesh(x1*scale, y1*scale, z1*scale, scalars=Y_lm_real, colormap='jet')


    #mlab.text3d(-0.2+dx31, 0, scale*z1.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    

    mlab.view(-85,85,30)
    mlab.show()

def ler_txt(path):
    text_file = open(path, "r")
    lines = text_file.readlines()
    coeff = np.zeros((len(lines), len(lines)*2-1))
    for l in range(len(lines)):
        string = lines[l].replace('\n', '')
        linha = string.split()
        for m in range(len(linha)):
            coeff[l][m] = float(linha[m])
        
        #coeff = []
        #for item in string.split():
        #    coeff[l].append(float(item))

    return np.array(coeff)

if __name__ == "__main__":
    #l = 2
    #m = 1
    path = '../data/coeficientes.txt'
    earth = 1
    miu = 398600.4415
    r = 6378.1363
    r_orbit = 6500
    #visualize(l,m)
    coeff = ler_txt(path)
    print('coefficientes =')
    print(coeff)
    if earth==0:
        for l in range(len(coeff)):
            coeff[l] = -coeff[l]*miu*r**l
            coeff[l] = coeff[l]*(r/r_orbit)**(l+1)
    draw_coeff(coeff)