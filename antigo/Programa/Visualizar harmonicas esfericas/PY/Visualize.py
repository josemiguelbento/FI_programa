def visualize(l,m):

    import math
    import cmath
    import matplotlib.pyplot as plt
    import numpy as np
    import sympy as sym

    j = complex(0, 1)

    n = 50
    phi = np.linspace(0, 2 * math.pi, n)
    theta = np.linspace(0, math.pi, n)

    [PHI, THETA] = np.meshgrid(phi, theta)


    a = math.sqrt(((2 * l + 1) / (4 * math.pi)) * (((math.factorial(l - m)) / (math.factorial(l + m)))))

    s = sym.Symbol('s')

    G = (s ** 2 - 1) ** l

    H = (1 - s ** 2) ** (m / 2)
    P_ml = ((-1) ** m / (math.factorial(l) * (2 ** l))) * H * sym.diff(G, s, m + l)

    R = np.zeros((n, n))
    x = np.zeros((n, n))
    y = np.zeros((n, n))
    z = np.zeros((n, n))

    for l in range(n):
        for k in range(n):
            p = complex(a * cmath.exp(j * m * PHI[l, k]) * P_ml.subs(s, math.cos(THETA[l, k])))
            R[l, k] = abs(p.real)

    for l in range(n):
        for k in range(n):
            x[l, k] = R[l, k] * math.sin(THETA[l, k]) * math.cos(PHI[l, k])
            y[l, k] = R[l, k] * math.sin(THETA[l, k]) * math.sin(PHI[l, k])
            z[l, k] = R[l, k] * math.cos(THETA[l, k])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z)

    plt.show()

