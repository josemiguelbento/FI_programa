def visualize(l,m):

    import math
    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm, colors
    import numpy as np
    import sympy as sym


    n = 50
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

    x = np.sin(THETA) * np.cos(PHI)
    y = np.sin(THETA) * np.sin(PHI)
    z = np.cos(THETA)

    x1 = abs(Y_ml_real) * np.sin(THETA) * np.cos(PHI)
    y1 = abs(Y_ml_real) * np.sin(THETA) * np.sin(PHI)
    z1 = abs(Y_ml_real) * np.cos(THETA)

    x2 = abs(Y_ml_imag) * np.sin(THETA) * np.cos(PHI)
    y2 = abs(Y_ml_imag) * np.sin(THETA) * np.sin(PHI)
    z2 = abs(Y_ml_imag) * np.cos(THETA)

    x3 = Y_ml_abs * np.sin(THETA) * np.cos(PHI)
    y3 = Y_ml_abs * np.sin(THETA) * np.sin(PHI)
    z3 = Y_ml_abs * np.cos(THETA)

    norm = colors.Normalize()
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(331, projection='3d')
    ax.plot_surface(x3, y3, z3, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_abs)))
    ax.set_title(f"$|Y_{{{l}{m}}}|$")
    clrbr3 = cm.ScalarMappable(cmap=cm.jet)
    clrbr3.set_array(Y_ml_abs)
    fig.colorbar(clrbr3, shrink=0.4)

    ax = fig.add_subplot(332, projection='3d')
    ax.plot_surface(x1, y1, z1, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_real)))
    ax.set_title(f"Re$[Y_{{{l}{m}}}]$")
    clrbr1 = cm.ScalarMappable(cmap=cm.jet)
    clrbr1.set_array(Y_ml_real)
    fig.colorbar(clrbr1, shrink=0.4)

    ax = fig.add_subplot(333, projection='3d')
    ax.plot_surface(x2, y2, z2, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_imag)))
    ax.set_title(f"Im$[Y_{{{l}{m}}}]$")
    clrbr2 = cm.ScalarMappable(cmap=cm.jet)
    clrbr2.set_array(Y_ml_imag)
    fig.colorbar(clrbr2, shrink=0.4)

    ax = fig.add_subplot(334, projection='3d')
    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_abs)))
    ax.set_title(f"$|Y_{{{l}{m}}}|$")
    clrbr3 = cm.ScalarMappable(cmap=cm.jet)
    clrbr3.set_array(Y_ml_abs)
    fig.colorbar(clrbr3, shrink=0.4)

    ax = fig.add_subplot(335, projection='3d')
    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_real)))
    ax.set_title(f"Re$[Y_{{{l}{m}}}]$")
    clrbr1 = cm.ScalarMappable(cmap=cm.jet)
    clrbr1.set_array(Y_ml_real)
    fig.colorbar(clrbr1, shrink=0.4)

    ax = fig.add_subplot(336, projection='3d')
    ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_imag)))
    ax.set_title(f"Im$[Y_{{{l}{m}}}]$")
    clrbr2 = cm.ScalarMappable(cmap=cm.jet)
    clrbr2.set_array(Y_ml_imag)
    fig.colorbar(clrbr2, shrink=0.4)

    x11 = (1+Y_ml_real) * np.sin(THETA) * np.cos(PHI)
    y11 = (1+Y_ml_real) * np.sin(THETA) * np.sin(PHI)
    z11 = (1+Y_ml_real) * np.cos(THETA)

    x22 = (1+Y_ml_imag) * np.sin(THETA) * np.cos(PHI)
    y22 = (1+Y_ml_imag) * np.sin(THETA) * np.sin(PHI)
    z22 = (1+Y_ml_imag) * np.cos(THETA)

    x33 = (1+Y_ml_abs) * np.sin(THETA) * np.cos(PHI)
    y33 = (1+Y_ml_abs) * np.sin(THETA) * np.sin(PHI)
    z33 = (1+Y_ml_abs) * np.cos(THETA)

    ax = fig.add_subplot(337, projection='3d')
    ax.plot_surface(x33, y33, z33, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_abs)))
    ax.set_title(f"$|Y_{{{l}{m}}}|$+1")
    clrbr3 = cm.ScalarMappable(cmap=cm.jet)
    clrbr3.set_array(Y_ml_abs)
    fig.colorbar(clrbr3, shrink=0.4)

    ax = fig.add_subplot(338, projection='3d')
    ax.plot_surface(x11, y11, z11, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_real)))
    ax.set_title(f"Re$[Y_{{{l}{m}}}]$+1")
    clrbr1 = cm.ScalarMappable(cmap=cm.jet)
    clrbr1.set_array(Y_ml_real)
    fig.colorbar(clrbr1, shrink=0.4)

    ax = fig.add_subplot(339, projection='3d')
    ax.plot_surface(x22, y22, z22, rstride=1, cstride=1, facecolors=cm.jet(norm(Y_ml_imag)))
    ax.set_title(f"Im$[Y_{{{l}{m}}}]$+1")
    clrbr2 = cm.ScalarMappable(cmap=cm.jet)
    clrbr2.set_array(Y_ml_imag)
    fig.colorbar(clrbr2, shrink=0.4)

    plt.show()


if __name__ == "__main__":
    l = 3
    m = 1
    visualize(l,m)