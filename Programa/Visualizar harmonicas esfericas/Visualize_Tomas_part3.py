from PyQt5.QtWidgets import QWidget, QHBoxLayout
import visvis as vv
from mayavi import mlab

class MainWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.fig = vv.backends.backend_pyqt5.Figure(self)
        layout = QHBoxLayout(self)
        layout.addWidget(self.fig._widget)
        self.setLayout(layout)
        self.setWindowTitle('Boas')
        self.show()


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

    mlab.figure(1, bgcolor=(1, 1, 1), size=(1000, 900))
    mlab.clf()

    mlab.mesh(x3*3.5, y3*3.5, z3*3.5, scalars=Y_ml_abs, colormap='jet')
    #mlab.colorbar(orientation='vertical')

    mlab.mesh((x1*3.5+4), y1*3.5, z1*3.5, scalars=Y_ml_real, colormap='jet')

    mlab.mesh(x2*3.5+8, y2*3.5, z2*3.5, scalars=Y_ml_imag, colormap='jet')

    mlab.mesh(x, y, z-4, scalars=Y_ml_abs, colormap='jet')

    mlab.mesh(x+4, y, z-4, scalars=Y_ml_real, colormap='jet')

    mlab.mesh(x+8, y, z-4, scalars=Y_ml_imag, colormap='jet')

    mlab.mesh(x33, y33, z33-8, scalars=Y_ml_abs, colormap='jet')

    mlab.mesh(x11+4, y11, z11-8, scalars=Y_ml_real, colormap='jet')

    mlab.mesh(x22+8, y22, z22-8, scalars=Y_ml_imag, colormap='jet')

    #mlab.text3d(0, 0, 4, 'text', scale=(1, 1, 1), color=(0,0,0))




    mlab.view(-85,90,25)
    mlab.show()






if __name__ == "__main__":
    l = 4
    m = 2
    visualize(l,m)