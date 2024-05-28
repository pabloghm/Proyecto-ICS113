import gurobipy as gp

'''Cagar datos de los archivos csv que generemos en diccionarios para no tener problemas de índices'''

cantidad_dias = 60
cantidad_cursos = 12
cantidad_libros = 48

'''No tenemos definido una cantidad de camiones formalmente'''
cantidad_camiones = 20

'''No teneos definido una cantidad de colegios formalmente'''
cantidad_colegios = 50

'''No teneos definido una cantidad de bodegas formalmente'''
cantidad_bodegas = 5

T: range = range(1, cantidad_dias + 1)
J: range = range(1, cantidad_bodegas + 1)
K: range = range(1, cantidad_colegios + 1)
C: range = range(1, cantidad_camiones + 1)
I: range = range(1, cantidad_libros + 1)
N: range = range(1, cantidad_cursos + 1)

try:
    modelo = gp.Model("Distribuidora Edubooks")

    '''Variables de decisión'''
    X = modelo.addVars(I, T, vtype=gp.GRB.CONTINUOUS, name='X')
    GAMMA = modelo.addVars(I, T, vtype=gp.GRB.CONTINUOUS, name='GAMMA')
    Y = modelo.addVars(I, J, T, vtype=gp.GRB.CONTINUOUS, name='Y')
    Z = modelo.addVars(I, K, T, vtype=gp.GRB.CONTINUOUS, name='Z')
    B = modelo.addVars(I, J, T, vtype=gp.GRB.CONTINUOUS, name='B')
    M = modelo.addVars(I, J, K, T, vtype=gp.GRB.CONTINUOUS, name='M')
    Q = modelo.addVars(I, C, J, K, T, vtype=gp.GRB.CONTINUOUS, name='Q')
    G = modelo.addVars(I, C, J, T, vtype=gp.GRB.CONTINUOUS, name='G')
    CA = modelo.addVars(C, J, T, vtype=gp.GRB.BINARY, name='CA')
    CB = modelo.addVars(C, J, K, T, vtype=gp.GRB.BINARY, name='CB')
    F = modelo.addVars(I, T, vtype=gp.GRB.BINARY, name='F')
    H = modelo.addVars(T, vtype=gp.GRB.BINARY, name='H')

    '''Restricciones'''

    '''Naturaleza variables'''

    '''Para variable X'''
    for i in I:
        for t in T:
            modelo.addConstr(X[i, t] >= 0, name='X')

    '''Para variable GAMMA'''
    for i in I:
        for t in T:
            modelo.addConstr(GAMMA[i, t] >= 0, name='GAMMA')

    '''Para variable Y'''
    for i in I:
        for j in j:
            for t in T:
                modelo.addConstr(Y[i, j, t] >= 0, name='Y')

    '''Para variable Z'''
    for i in I:
        for k in K:
            for t in T:
                modelo.addConstr(Z[i, k, t] >= 0, name='Z')

    '''Para variable B'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(B[i, j, t] >= 0, name='B')

    '''Para variable M'''
    for i in I:
        for j in J:
            for k in K:
                for t in T:
                    modelo.addConstr(M[i, j, k, t] >= 0, name='M')

    '''Para variable Q'''
    for i in I:
        for c in C:
            for j in J:
                for k in K:
                    for t in T:
                        modelo.addConstr(Q[i, c, j, k, t] >= 0, name='Q')

    '''Para variable G'''
    for i in I:
        for c in C:
            for j in J:
                for t in T:
                    modelo.addConstr(G[i, c, j, t] >= 0, name='Q')
except Exception as error:
    print(error)
