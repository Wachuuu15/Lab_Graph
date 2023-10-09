from  math import isclose
import math

class Numpi:
    def multMatrices(m1, m2):
        if len(m1[0]) == len(m2):
            matRes = [[0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0]]

            for i in range(4):
                for j in range(4):
                    for k in range(4):
                        matRes[i][j] += (m1[i][k] * m2[k][j])

            return matRes

    def mulVect(m1, vector):
        vecRes = [0.0, 0.0, 0.0, 0.0]
        for i in range(4):
            for j in range(4):
                vecRes[i] += (m1[i][j] * vector[j])

        return vecRes
    
    
    def multi4x4matrix(matrix1, matrix2):
        resultado = [
            [0.0,0.0,0.0,0.0],
            [0.0,0.0,0.0,0.0],
            [0.0,0.0,0.0,0.0],
            [0.0,0.0,0.0,0.0]]
        
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    resultado[i][j] += matrix1[i][k] * matrix2[k][j]
        return resultado
    
    def barycentricCoords(A, B, C, P):

        areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
                    (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

        areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
                    (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

        areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
                    (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

        areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
                    (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

        # Si el area del tri�ngulo es 0, retornar nada para
        # prevenir divisi�n por 0.
        if areaABC == 0:
            return None

        # Determinar las coordenadas baricentricas dividiendo el 
        # �rea de cada subtriangulo por el area del triangulo mayor.
        u = areaPCB / areaABC
        v = areaACP / areaABC
        w = areaABP / areaABC

        # Si cada coordenada est� entre 0 a 1 y la suma de las tres
        # es igual a 1, entonces son v�lidas.
        if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 and isclose(u+v+w, 1.0):
            return (u, v, w)
        else:
            return None


    def inverse_matrix(matrix):
        if len(matrix) != 4 or len(matrix[0]) != 4:
            print("Matriz debería ser de 4x4.")

        # Create an augmented matrix with identity matrix
        augmented_matrix = [row + [1 if i == j else 0 for j in range(4)] for i, row in enumerate(matrix)]

        # Apply Gauss-Jordan elimination
        for col in range(4):
            pivot_row = max(range(col, 4), key=lambda i: abs(augmented_matrix[i][col]))
            augmented_matrix[col], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[col]

            pivot_value = augmented_matrix[col][col]
            if pivot_value == 0:
                print("La matriz es singular.")

            for j in range(col, 8):
                augmented_matrix[col][j] /= pivot_value

            for i in range(4):
                if i != col:
                    factor = augmented_matrix[i][col]
                    for j in range(col, 8):
                        augmented_matrix[i][j] -= factor * augmented_matrix[col][j]

        inverse = [row[4:] for row in augmented_matrix]
        return inverse

    def norm_vector(vector):
        vector = list(vector)
        magnitud = math.sqrt(sum(v**2 for v in vector))
        
        if magnitud == 0:
            return vector
        
        norm = [v / magnitud for v in vector]
        norm = tuple(norm)
        return norm

    def vecResta(v1, v2):
        resta = (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])
        return resta
    
    def deny_array(vector):
        vector = list(vector)
        for i in range(len(vector)):
            vector[i] *= -1
        
        return vector

    def subtract_arrays(array1, array2):
        if len(array1) != len(array2):
            raise ValueError("Los arrays deben tener la misma longitud.")

        result = []
        for i in range(len(array1)):
            result.append(array1[i] - array2[i])

        return tuple(result)
    
    def dot_product(vector_a, vector_b):
        if len(vector_a) != len(vector_b):
            raise ValueError("Los vectores tienen que ser del mismo tamaño")
        
        product = sum(x * y for x, y in zip(vector_a, vector_b))
        return product
    
    def add_arrays(array1, array2):
        if len(array1) != len(array2):
            raise ValueError("Los arrays deben tener la misma longitud.")

        result = []
        for i in range(len(array1)):
            result.append(array1[i] + array2[i])

        return tuple(result)
    
    def multiply_scalar_array(scalar, array):
        result = []
        for i in range(len(array)):
            result.append(scalar * array[i])

        return tuple(result)
    
    #Sacar magnitud de un vector
    def magV(vector):
        vectorList = list(vector)
        return math.sqrt(sum(e ** 2 for e in vectorList))

    
   #Normalizacion
    def normalizeV(vector):
        vectorList = list(vector)
        mag = math.sqrt(sum(e ** 2 for e in vectorList))
        if mag == 0: #error if magnitude is 0
            print("Unable to normalize")
        
        normVector = [e / mag for e in vectorList]
        return normVector
        

    def divide_array_scalar(array,scalar):
        result = []
        for i in range(len(array)):
            result.append(array[i]/scalar)

        return tuple(result)