import gurobipy as gp

'''Cagar datos de los archivos csv que generemos en diccionarios para no tener problemas de índices'''

cantidad_dias = 60
cantidad_cursos = 12
cantidad_libros = 48
cc = 1200 #capacidad de carga del camion
V = 99999999999 #Monto lo suficientemente grande

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

    X = modelo.addVars(I, T, vtype=gp.GRB.CONTINUOUS, name='X', lb=0)
    GAMMA = modelo.addVars(I, T, vtype=gp.GRB.CONTINUOUS, name='GAMMA', lb=0)
    Y = modelo.addVars(I, J, T, vtype=gp.GRB.CONTINUOUS, name='Y', lb=0)
    Z = modelo.addVars(I, K, T, vtype=gp.GRB.CONTINUOUS, name='Z', lb=0)
    B = modelo.addVars(I, J, T, vtype=gp.GRB.CONTINUOUS, name='B', lb=0)
    M = modelo.addVars(I, J, K, T, vtype=gp.GRB.CONTINUOUS, name='M', lb=0)
    Q = modelo.addVars(I, C, J, K, T, vtype=gp.GRB.CONTINUOUS, name='Q', lb=0)
    G = modelo.addVars(I, C, J, T, vtype=gp.GRB.CONTINUOUS, name='G', lb=0)
    CA = modelo.addVars(C, J, T, vtype=gp.GRB.BINARY, name='CA')
    CB = modelo.addVars(C, J, K, T, vtype=gp.GRB.BINARY, name='CB')
    F = modelo.addVars(I, T, vtype=gp.GRB.BINARY, name='F')
    H = modelo.addVars(T, vtype=gp.GRB.BINARY, name='H')

    modelo.update()

    '''Restricciones'''

    '''Restriccion 1'''
    for i in I:
        for j in J:
            modelo.addConstr(Y[i, j, 0] == 0, name="R1")

    '''Restriccion 2'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(Y[i, j, t] <= q[j], name="R2")

    '''Restriccion 3'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(Y[i, j, t] == Y[i, j, t - 1] + B[i, j, t] - gp.quicksum(M[i, j, t, k] for k in K),
                                 name="R3")

    '''Restriccion 4'''
    for i in I:
        for k in K:
            for t in T:
                for j in J:
                    modelo.addConstr(Z[i, k, t] == Z[i, k, t - 1] + M[i, j, t, k], name="R4")

    '''Restriccion 5'''
    for i in I:
        for t in T:
            modelo.addConstr(X[i, t] + GAMMA[i, t] <= s[i, t], name="R5")

    '''Restriccion 6'''
    for c in C:
        for j in J:
            for k in K:
                for t in T:
                    modelo.addConstr(gp.quicksum(Q[i, c, j, k, t] for i in I) <= cc * CB[c, j, k, t], name="R6")

    '''Restriccion 7'''
    for c in C:
        for j in J:
            for t in T:
                modelo.addConstr(gp.quicksum(G[i, c, j, t] for i in I) <= cc * CA[c, j, t], name="R7")

    '''Restriccion 8'''
    for c in C:
        for j in J:
            for k in K:
                for t in T:
                    modelo.addConstr(cc * 0.5 * CB[c, j, k, t] <= gp.quicksum(Q[i, c, j, k, t] for i in I), name="R8")

    '''Restriccion 9'''
    for c in C:
        for j in J:
            for t in T:
                modelo.addConstr(cc * 0.5 * CA[c, j, t] <= gp.quicksum(G[i, c, j, t] for i in I), name="R9")

    '''Restriccion 10'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(gp.quicksum(M[i, j, t, k] for k in K) <= Y[i, j, t], name="R10")

    '''Restriccion 11'''
    modelo.addConstr(gp.quicksum(H[t] for t in T) <= 40, name="R11")

    '''Restriccion 12'''
    sab_dom = [6, 7, 13, 14, 20, 21, 27, 28, 34, 35, 41, 42, 48, 49, 55, 56, 62]
    for t in sab_dom:
        modelo.addConstr(H[t] == 0, name="R12")
    sab_dom = [6,7,13,14,20,21,27,28,34,35,41,42,48,49,55,56,62]
    for t in sab_dom:
        modelo.addConstr(H[t] == 0, name='no se trabaja durante el fin de semana')

    '''Restriccion 13'''
    for i in I:
        for t in T:
            modelo.addConstr(F[i, t] <= H[t], name="R13")

    '''Restriccion 14'''
    for i in I:
        for t in T:
            modelo.addConstr(gp.quicksum(B[i, j, t] for j in J) == X[i, t] + GAMMA[i, t], name="R14")

    '''Restriccion 15'''
    for i in I:
        for t in T:
            modelo.addConstr(X[i, t] + GAMMA[i, t] <= V * F[i, t], name="R15")

    '''Restriccion 16'''
    for i in I:
        for k in K:
            modelo.addConstr(gp.quicksum(a[i,k,n] for n in N) == gp.quicksum(gp.quicksum(M[i,j,k,t] for t in T) for j in J) )

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
        for j in J:
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
                    modelo.addConstr(G[i, c, j, t] >= 0, name='G')

    '''
    FO = (quicksum(X[i,t]*c[i][t] + GAMMA[i,t]*cr[i][t] for i in I for t in T) + quicksum(R[w,t]*cw for w in W for 
    t in T) + quicksum(e[j]*CA[c,j,t]*cd[t] for c in C for j in J for t in T) + quicksum(e[j][k]*CB[c,j,k, 
    t]*cd[t] for c in C for j in J for t in T for k in K) + quicksum(g[j][t]*Y[i,j,t] for i in I for j in J for t in 
    T) + quicksum(c*H[t] for t in T))'''

    '''
    modelo.update()
    modelo.setObjective(FO, gp.GRB.MAXIMIZE)
    modelo.optimize()
    '''

except Exception as error:
    print(error)
