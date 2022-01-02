from mayavi import mlab
import math
import numpy as np
import sympy as sym

def visualize(l,m):

    n = 200
    phi = np.linspace(0, 2 * np.pi, n)
    theta = np.linspace(-np.pi/2, np.pi/2, n)
    [PHI, THETA] = np.meshgrid(phi, theta)

    if m == 0: a = np.sqrt( (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    else: a = np.sqrt( 2 *  (2 * l + 1)  * math.factorial(l - abs(m)) / math.factorial(l + abs(m)))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (abs(m) / 2)
    P_lm = (1 / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, abs(m) + l) # egm96

    P_lm = sym.lambdify(s, P_lm)
    if m>=0: Y_lm_real = a * P_lm(np.sin(THETA)) * np.cos(abs(m)*PHI)
    else: Y_lm_real = a * P_lm(np.sin(THETA)) * np.sin(abs(m)*PHI)

    scale = 1/(np.sqrt(2*4*np.pi))

    r = 1
    x = r*np.cos(THETA) * np.cos(PHI)
    y = r*np.cos(THETA) * np.sin(PHI)
    z = r*np.sin(THETA)

    x11 = (r+Y_lm_real*scale) * np.cos(THETA) * np.cos(PHI)
    y11 = (r+Y_lm_real*scale) * np.cos(THETA) * np.sin(PHI)
    z11 = (r+Y_lm_real*scale) * np.sin(THETA)


    x1 = abs(Y_lm_real) * np.cos(THETA) * np.cos(PHI)
    y1 = abs(Y_lm_real) * np.cos(THETA) * np.sin(PHI)
    z1 = abs(Y_lm_real) * np.sin(THETA)



    #############################
    scale = 1/(np.sqrt(2*4*np.pi))*3
    ##############################

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()


    mlab.mesh((x1*scale), y1*scale, z1*scale, scalars=Y_lm_real, colormap='jet')

    mlab.mesh(x, y, z-5, scalars=Y_lm_real, colormap='jet')

    mlab.mesh(x11, y11, z11-10, scalars=Y_lm_real, colormap='jet')


    mlab.view(-85,85,30)
    mlab.show()


if __name__ == "__main__":
    l = 2
    m = 2
    visualize(l,m)