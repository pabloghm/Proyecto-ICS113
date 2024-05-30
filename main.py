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
    '''Restriccion 1'''
    for i in I:
        for j in J:
            modelo.addConstr(Y[i,j,0] == 0, name='La bodega parte vacía')
    
    '''Restriccion 2'''
    for j in J:
        for t in T:
            modelo.addConstr(Y[i,j,t] <= q[j], name='No sobrepasar la capacidad de almacenaje por bodega')
    
    '''Restriccion 3'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(Y[i,j,t] == Y[i,j,t-1] + B[i,j,t] - gp.quicksum(M[i,j,t,k] for j in J), name='Conservacion de inventario en la bodega')

    '''Restriccion 4'''
    for i in I:
        for k in K:
            for t in T:
                for j in J:
                    modelo.addConstr(Z[i,k,t] == Z[i,k,t-1] + M[i,j,t,k] , name='Conservacion de inventario en el colegio')
    
    '''Restriccion 5'''
    for i in I:
        for t in T:
            modelo.addConstr(X[i,t] + GAMMA[i,t] <= s[i,t], name='cantidad producida de libro no puede ser mayor a la capacidad de produccion')
    
    '''Restriccion 6'''
    for c in C:
        for j in J:
            for k in K:
                for t in T:
                    modelo.addConstr(gp.quicksum(Q[i,c,j,k,t] for i in I) <= cc * CB[c,j,k,t], name='la cantidad de libros desde la bodega al colegio no puede ser mayor a la capacidad de carga del camión')

    '''Restriccion 7'''
    for c in C:
        for j in J:
            for t in T:
                modelo.addConstr(gp.quicksum(G[i,c,j,t] for i in I) <= cc * CA[c,j,t], name='la cantidad de libro desde la fabrica a la bodega no puede ser mayor a la capacidad de carga del camión')

    '''Restriccion 8'''
    for c in C:
        for j in J:
            for k in K:
                for t in T:
                    modelo.addConstr(cc * 0.5 * CB[c,j,k,t] <= gp.quicksum(Q[i,c,j,k,t] for i in I), name='la cantidad de libros desde la bodega al colegio no puede ser menor a la mitad de la capacidad de carga del camión')

    '''Restriccion 9'''
    for c in C:
        for j in J:
            for t in T:
                modelo.addConstr(cc * 0.5* CA[c,j,t] <= gp.quicksum(G[i,c,j,t] for i in I), name='la cantidad de libro desde la fabrica a la bodega no puede ser menor a la mitad de la capacidad de carga del camión')

    '''Restriccion 10'''
    for i in I:
        for j in J:
            for t in T:
                modelo.addConstr(gp.quicksum(M[i,j,t,k] for k in K) <= Y[i,j,t], name='la cantidad de libros llevados desde la bodega no puede ser mayor que la cantidad almacenada en la bodega')
    
    '''Restriccion 11'''
    modelo.addConstr(gp.quicksum(H[t] for t in T), name='la fabrica no puede funcionar más días por sobre los días hábiles')

    '''Restriccion 12'''
    sab_dom = [6,7,13,14,20,21,27,28,34,35,41,42,48,49,55,56,62]
    for t in sab_dom:
        modelo.addConstr(H[t] == 0, name='no se trabaja durante el fin de semana')

    '''Restriccion 13'''
    for i in I:
        for t in T:
            modelo.addConstr(F[i,t] <= H[t], name='No se producen libros los días que no funcinoe la fabrica')
    
    '''Restriccion 14'''
    for i in I: 
        for t in T:
            modelo.addConstr(gp.quicksum(B[i,j,t] for j in J) == X[i,t] + GAMMA[i,t], name='la cantidad de librosque fueronn dejados en la bodega es igaul a la cantidad producida')

    '''Restriccion 15'''
    for i in I:
        for t in T:
            modelo.addConstr(X[i,t] + GAMMA[i,t] <= V * F[i,t], name='la cantidad de libro a producir en el dia no puede ser mayor a un monto V')

    '''Restriccion 16'''
    for i in I:
        for k in K:
            modelo.addConstr(gp.quicksum(a[i,k,n] for n in N) == gp.quicksum(gp.quicksum(M[i,j,k,t] for t in T) for j in J), name='cumplir la necesidad de libros por colegio' )
    
    '''Restriccion 17'''
    for i in I:
        modelo.addConstr(w[i] <= gp.quicksum(GAMMA[i,t] for t in T), name='cumplir la cantidad minima de libros reciclados')

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
