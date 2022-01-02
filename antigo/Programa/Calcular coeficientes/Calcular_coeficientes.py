from mayavi import mlab
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
import math
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import numpy as np
import sympy as sym


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

def get_vertices(path):
    # Load the shape model. The first column lists whether the row is a vertex or face. The second,
    # third and fourth column list the coordiantes (vertex) and vertex indices (faces)
    COMET_67P_SHAPE_OBJ = pd.read_csv(path, delim_whitespace=True, \
                                  names=['TYPE', 'X1', 'X2', 'X3'])

    # Assign the vertices and faces
    VERTICES = COMET_67P_SHAPE_OBJ.loc[COMET_67P_SHAPE_OBJ['TYPE'] == 'v'][['X1', 'X2', 'X3']].values \
               .tolist()
    #faces = COMET_67P_SHAPE_OBJ.loc[COMET_67P_SHAPE_OBJ['TYPE'] == 'f'][['X1', 'X2', 'X3']].values
    
    return VERTICES

def get_polar_vertices(VERTICES):

    return [POL_VER_R, POL_VER_PHI,POL_VER_THETA]
    
def calculate_y_matrix(POL_VER_PHI,POL_VER_THETA ,l_max):
    k = (l_max+1)**2
    Y_matrix = np.zeros((len(POL_VER_PHI),k))
    for i in range(0, len(POL_VER_PHI)+1):
        for l in range(0, l_max+1):
            for m in range(-l,l+1):
                j = l**2 + l + m + 1
                Y_matrix[i][j] = get_spherical_harmonic(l, m, POL_VER_PHI, POL_VER_THETA)
    
    return Y_matrix

def vector2matrix (vector):
    l_max = np.sqrt(len(vector))-1
    for l in range(0, l_max+1):
        for m in range(-l,l+1):
            j = l**2 + l + m + 1
            matrix[l][m] = vector(j)

    return matrix


#https://www.hindawi.com/journals/mpe/2015/582870/#introduction

if __name__ == "__main__":
    l = 3
    m = 1
    path = '../data/Asteroide1.OBJ'
    l_max = 3

    VERTICES = get_vertices(path)
    [POL_VER_R, POL_VER_PHI,POL_VER_THETA]= get_polar_vertices(VERTICES)

    Y_matrix = np.array(calculate_y_matrix(POL_VER_PHI,POL_VER_THETA ,l_max))
    F_vector = np.array(POL_VER_R)

    A_vector = np.linalg.solve(Y_matrix, F_vector)
    
    A_matrix = vector2matrix(A_vector)

    draw_coeff(A_matrix)

    #coeff = np.array([[0.37],
    #         [0.020, 0.052, 0.020],
    #         [0.068, 0.012, 0.012, 0.012, 0.068],
    #         [0.0052, 0.0025, 0.0032, 0.0026, 0.0032, 0.0025, 0.0052]])
    #draw_coeff(coeff)