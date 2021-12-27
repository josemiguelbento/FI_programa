from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor

def visualize(l,m):

    import math
    import matplotlib.pyplot as plt
    from matplotlib import cm, colors
    import numpy as np
    import sympy as sym


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
    Y_ml_real = Y_ml.real
    Y_ml_imag = Y_ml.imag
    Y_ml_abs = np.abs(Y_ml)

    r = 1
    x = r*np.sin(THETA) * np.cos(PHI)
    y = r*np.sin(THETA) * np.sin(PHI)
    z = r*np.cos(THETA)

    x11 = (r+Y_ml_real) * np.sin(THETA) * np.cos(PHI)
    y11 = (r+Y_ml_real) * np.sin(THETA) * np.sin(PHI)
    z11 = (r+Y_ml_real) * np.cos(THETA)

    x22 = (r+Y_ml_imag) * np.sin(THETA) * np.cos(PHI)
    y22 = (r+Y_ml_imag) * np.sin(THETA) * np.sin(PHI)
    z22 = (r+Y_ml_imag) * np.cos(THETA)

    x33 = (r+Y_ml_abs) * np.sin(THETA) * np.cos(PHI)
    y33 = (r+Y_ml_abs) * np.sin(THETA) * np.sin(PHI)
    z33 = (r+Y_ml_abs) * np.cos(THETA)

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
    scale = 3

    dx31 = scale*x3.max() - scale*x1.min() + 1
    d = x.max() - x.min() + 1
    if d > dx31:
        dx31 = d
    d = x33.max() - x11.min() + 1
    if d > dx31:
        dx31 = d
    
    dx12 = scale*x1.max() - scale*x2.min() + 1
    d = x.max() - x.min() + 1
    if d > dx12:
        dx12 = d
    d = x11.max() - x22.min() + 1
    if d > dx12:
        dx12 = d
    
    dz1 = -scale*z3.min() + z.max() + 2
    d = -scale*z1.min() + z.max() + 2
    if d > dz1:
        dz1 = d
    d = -scale*z2.min() + z.max() + 2
    if d > dz1:
        dz1 = d
    
    dz2 = -z.min() + z33.max() + 2
    d = -z.min() + z11.max() + 2
    if d > dz2:
        dz2 = d
    d = -z.min() + z22.max() + 2
    if d > dz2:
        dz2 = d
    
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

    mlab.mesh(x, y, z-dz1, scalars=Y_ml_abs, colormap='jet')
    #mlab.text3d(-0.4, 0, 1.8-4, f'|Y{l}{m}|', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x+dx31, y, z-dz1, scalars=Y_ml_real, colormap='jet')
    #mlab.text3d(-0.4+3.8, 0, 1.8-4, f'Re[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    if m != 0:
        mlab.mesh(x+dx31+dx12, y, z-dz1, scalars=Y_ml_imag, colormap='jet')
    #mlab.text3d(7.4, 0, 1.8-4, f'Im[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x33, y33, z33-dz1-dz2, scalars=Y_ml_abs, colormap='jet')
    #mlab.text3d(-0.6, 0, 1.8-8, f'1+|Y{l}{m}|', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.mesh(x11+dx31, y11, z11-dz1-dz2, scalars=Y_ml_real, colormap='jet')
    #mlab.text3d(-0.4+3.4, 0, 1.8-8, f'1+Re[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    
    if m != 0:
        mlab.mesh(x22+dx31+dx12, y22, z22-dz1-dz2, scalars=Y_ml_imag, colormap='jet')
    #mlab.text3d(7.2, 0, 1.8-8, f'1+Im[Y{l}{m}]', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.text3d(-0.2, 0, scale*z3.max()+1, 'Abs', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31, 0, scale*z3.max()+1, 'Re', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(-0.2+dx31+dx12, 0, scale*z3.max()+1, 'Im', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.text3d(scale*x3.min()-2.5, 0, 0, 'R=Ylm', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x3.min()-2.5, 0, -dz1, 'Unit Sphere', scale=(0.2, 0.2, 0.2), color=(0,0,0))
    mlab.text3d(scale*x3.min()-2.5, 0, -dz1-dz2, 'R=(1+Ylm)', scale=(0.2, 0.2, 0.2), color=(0,0,0))

    mlab.view(-85,85,30)
    mlab.show()




if __name__ == "__main__":
    l = 10
    m = 5
    visualize(l,m)