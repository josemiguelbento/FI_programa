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

    a = np.sqrt(((2 * l + 1) / (4 * np.pi)) * (((math.factorial(l - abs(m))) / (math.factorial(l + abs(m))))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = ((-1) ** abs(m) / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l)

    P_lm = sym.lambdify(s, P_lm)
    Y_lm = a * np.exp(1j * abs(m) * PHI) * P_lm(np.cos(THETA))
    if m<0: Y_lm = (-1)**m * Y_lm.conj()
    Y_lm_real = Y_lm.real
    Y_lm_imag = Y_lm.imag
    Y_lm_abs = np.abs(Y_lm)


    x1 = abs(Y_lm_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_lm_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_lm_real) * np.cos(THETA)

    x2 = abs(Y_lm_imag) * np.sin(THETA) * np.cos(PHI)
    y2 = abs(Y_lm_imag) * np.sin(THETA) * np.sin(PHI)
    z2 = abs(Y_lm_imag) * np.cos(THETA)

    x3 = Y_lm_abs * np.sin(THETA) * np.cos(PHI)
    y3 = Y_lm_abs * np.sin(THETA) * np.sin(PHI)
    z3 = Y_lm_abs * np.cos(THETA)

    #############################
    scale = 5

    dx31 = scale*x3.max() - scale*x1.min() + 1
    
    dx12 = scale*x1.max() - scale*x2.min() + 1
    
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x3*scale, y3*scale, z3*scale, scalars=Y_lm_abs, colormap='jet')
    #mlab.text3d(-0.4, 0, 1.8, f'|Y{l}{m}|', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    #mlab.colorbar(orientation='vertical')

    mlab.mesh((x1*scale+dx31), y1*scale, z1*scale, scalars=Y_lm_real, colormap='jet')
    #mlab.text3d(-0.4+3.8, 0, 1.8, f'Re[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x2*scale+dx31+dx12, y2*scale, z2*scale, scalars=Y_lm_imag, colormap='jet')
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
    for l in range(len(coeff)):
        for m in range(-l,l+1):
            R = R + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA)

    visualize_final(R, THETA, PHI)



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
    scale = 0.00001

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
    l = 3
    m = 1
    path = '../data/coeficientes.txt'
    earth = 1
    miu = 398600.4415
    r = 6378.1363
    r_orbit = 6500
    #visualize(l,m)
    coeff = ler_txt(path)
    print('coefficientes =')
    print(coeff)
    if earth==1:
        for l in range(len(coeff)):
            coeff[l] = -coeff[l]*miu*r**l
            coeff[l] = coeff[l]*(r/r_orbit)**(l+1)
    draw_coeff(coeff)