from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import math
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import sympy as sym
import pandas as pd
from scipy.spatial import ConvexHull

from PyQt5.QtWidgets import QWidget, QHBoxLayout
import visvis as vv

class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.fig = vv.backends.backend_pyqt5.Figure(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.fig._widget)
        self.setLayout(layout)
        self.setWindowTitle('OBJ')
        self.show()

def get_series_SH(coeff, l_max, PHI, THETA, basis_matrix):  
    f = PHI * 0
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            #f = f + coeff[l][m+l] * get_spherical_harmonic(l, m, PHI, THETA).astype(complex).real
            f = f + coeff[l][m+l] * basis_matrix[:,j]

    return f

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

def get_Vertices_Faces():
    OBJ = pd.read_csv('data/Asteroide1.OBJ', delim_whitespace=True, \
                                    names=['TYPE', 'X1', 'X2', 'X3'])

    VERTICES = OBJ.loc[OBJ['TYPE'] == 'v'][['X1', 'X2', 'X3']].values \
                .tolist()

    FACES = OBJ.loc[OBJ['TYPE'] == 'f'][['X1', 'X2', 'X3']].values
    FACES = FACES - 1
    FACES = FACES.astype(int)
    FACES = FACES.tolist()

    return VERTICES, FACES

def get_cart_vertices(r, phi, theta):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    VERTICES = np.zeros((len(x),3)) 
    VERTICES[:,0] = x
    VERTICES[:,1] = y
    VERTICES[:,2] = z

    return VERTICES

def get_polar_vertices(VERTICES):
    N = len(VERTICES)
    r = np.tile(0.0, N)
    theta = np.tile(0.0, N)
    phi = np.tile(0.0, N)
    for i in range(N):
        r[i] = np.sqrt(VERTICES[i][0]**2 + VERTICES[i][1]**2 + VERTICES[i][2]**2)
        theta[i] = np.arccos(VERTICES[i][2]/r[i])
        phi[i] = math.atan2(VERTICES[i][1],VERTICES[i][0]) # beteween -PI and PI

    return r, theta, phi
    
def get_basis_matrix(phi, theta, l_max):
    k = (l_max+1)**2
    basis_matrix = np.zeros((len(phi),k)) # dtype=np.complex128 onde ha np.zero
    for l in range(l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m
            basis_matrix[:,j] = get_spherical_harmonic(l, m, phi, theta).astype(complex).real

    return basis_matrix

def get_coeff_least_square(A, f):
    f = f.reshape(len(f),1)
    B = A.T @ A
    print(f'det(B)={np.linalg.det(B)}')
    if np.linalg.det(B) == 0:
        coeff = np.linalg.pinv(B) @ A.T @ f
    else:
        coeff = np.linalg.inv(B) @ A.T @ f

    residual_error = f - A @ coeff

    return coeff, residual_error


def vector2matrix (vector, l_max):
    k = 0
    matrix = np.zeros((l_max+1, 2*l_max+1))
    for i in range(l_max+1):
        for j in range(1+2*i):
            matrix[i][j] = vector[k]
            k = k+1

    return matrix

def miu(V):


    hull=ConvexHull(V)
    vol=hull.volume
    rho=2 #g/cm3
    G=6.6742e-11
    m=vol*rho*G


    return m




def potential(r,phi, theta, l_max, mu, coeff):

    R_s=0.95*r
    pot=0
    for l in range(l_max + 1):
        for m in range(-l, l + 1):
            pot=pot+((R_s/r)**(m+1))*coeff[l][m]*get_spherical_harmonic(l,m,phi,theta).real


    pot=-1*(mu/R_s)*pot

    return pot

def visualizar_potential(VERTICES,coeff_LS_matrix):

    #   r=np.zeros(len(VERTICES))
    #  for i in range(len(VERTICES)):
    #      r[i]=np.sqrt(VERTICES[i][0] ** 2 + VERTICES[i][1] ** 2 + VERTICES[i][2] ** 2)
    # print(max(r))

    mu = miu(VERTICES)
    r = 0.4
    n = 10
    phi = np.linspace(0, math.pi * 2, n)
    theta = np.linspace(0, math.pi, n)
    s = (n, n)
    POT = np.zeros(s)
    PHI, THETA = np.meshgrid(phi, theta)

    for i in range(n):
        for j in range(n):
            POT[i, j] = potential(r, PHI[i, j], THETA[i, j], l_max, mu, coeff_LS_matrix)

    plt.figure(1)
    cp = plt.contourf(PHI, THETA, POT)
    plt.colorbar(cp)
    plt.show()


    return

#https://www.hindawi.com/journals/mpe/2015/582870/#introduction

if __name__ == "__main__":
    l_max =10

    print('getting vertices & faces....')
    VERTICES, FACES = get_Vertices_Faces()
    print('vertices & faces acquired....')

    print('calculating r_Ver & theta_Ver & phi_Ver....')
    r_Ver, theta_Ver, phi_Ver = get_polar_vertices(VERTICES)
    print('r_Ver & theta_Ver & phi_Ver calculated....')

    print('calculating Basis Matrix ....')
    Basis_Matrix = get_basis_matrix(phi_Ver, theta_Ver, l_max)
    print('Basis Matrix calculated....')

    print('calculating Coeff_LS & Residual_error_LS....')
    coeff_LS, res_error_LS = get_coeff_least_square(Basis_Matrix, r_Ver)
    print(f'Residual error: {np.linalg.norm(res_error_LS)}')
    print('Coeff_LS & Residual_error_LS calculated....')
    
    print('tranforming vector coeff in matrix....')
    coeff_LS_matrix = vector2matrix(coeff_LS, l_max)
    print('vector coeff in matrix calculated....')

    print('calculating series....')
    f = get_series_SH(coeff_LS_matrix, l_max, phi_Ver, theta_Ver, Basis_Matrix)
    print('series calculated....')

    print('calculating vertices_SH....')
    VERT_SH = get_cart_vertices(f, phi_Ver, theta_Ver)
    print('vertices_SH calculated....')

    print('Printing colormap for potential....')
    visualizar_potential(VERTICES, coeff_LS_matrix)
    print('Print done....')

    app = vv.use()
    app.Create()
    main_w = MainWindow()
    main_w.resize(1200, 800)

    vv.figure(1) 
    vv.clf()

    a1 = vv.subplot(121) 
    vv.title(f"Original")
    vv.mesh(vertices=VERTICES, faces=FACES, verticesPerFace=3)
    a1.bgcolor = 'black'
    a1.axis.showGrid = False
    a1.axis.visible = False
    a1.camera = '3d'
    a1.camera.azimuth = 120
    a1.camera.elevation = 25

    a2 = vv.subplot(122) 
    vv.title(f"SH")
    vv.mesh(vertices=VERT_SH, faces=FACES, verticesPerFace=3)
    a2.bgcolor = 'black'
    a2.axis.showGrid = False
    a2.axis.visible = False

    a2.camera = a1.camera

    app.Run()