from methods import *
import os
import csv
import matplotlib.pyplot as plt
import random

def lu_decomposition(matrix, vector_b, N):
    vector_y = ones(N)
    vector_x = ones(N)
    matrix_L = identity_matrix(N)
    matrix_U = copy_matrix(matrix)
    matrix_P = identity_matrix(N)  #macierz permutacji


    #PIVOTING
    for k in range(N-1):  # pomijam ostatnią kolumnę
        max_pivot = matrix_U[k][k]
        row_indeks = k
        for i in range(k, N):
            if abs(matrix_U[i][k]) > max_pivot:
                max_pivot = abs(matrix_U[i][k])
                row_indeks = i

        for j in range(k, N):
            tmp = matrix_U[k][j]
            matrix_U[k][j] = matrix_U[row_indeks][j]
            matrix_U[row_indeks][j] = tmp
        for j in range(k):
            tmp = matrix_L[k][j]
            matrix_L[k][j] = matrix_L[row_indeks][j]
            matrix_L[row_indeks][j] = tmp
        for j in range(N):
            tmp = matrix_P[k][j]
            matrix_P[k][j] = matrix_P[row_indeks][j]
            matrix_P[row_indeks][j] = tmp

        # TWORZENIE MACIERZY L I U
        for j in range(k+1, N):
            matrix_L[j][k] = matrix_U[j][k] / matrix_U[k][k]
            for i in range(k,N):
                matrix_U[j][i] = matrix_U[j][i] - (matrix_L[j][k] * matrix_U[k][i])

    vector_b = vector_multiply_matrix(vector_b, matrix_P)

    # Ly = b
    for i in range(N):
        sum = 0
        for p in range(i):
            sum += matrix_L[i][p] * vector_y[p]
        vector_y[i] = (1 / matrix_L[i][i]) * (vector_b[i] - sum)

    # Ux = y
    for i in range(N - 1, -1, -1):
        sum = 0
        for p in range(N - 1, i, -1):
            sum += matrix_U[i][p] * vector_x[p]
        vector_x[i] = (1 / matrix_U[i][i]) * (vector_y[i] - sum)

    return vector_x


def SplineInterpolation(data):
    m = len(data)  # m węzłów
    n = m-1    # n przedziałów
    A = zero_matrix(4*n)
    b = zeros(4*n)
    # x = [a0, b0, c0, d0, a1, b1, c1, d1,..., an-1, bn-1, cn-1, dn-1]

    #TWORZENIE Ax=b
    # Sj(xj) = f(xj)
    # a = f(x)
    for i in range(n):
        A[i][4*i] = float(1)
        b[i] = float(data[i][1])  # y

    #Sj(xj+1) = f(xj+1)
    #a + bh + ch^2 + dh^3 = f(x)
    for i in range(n):
        h = float(data[i+1][0]) - float(data[i][0]) # x1 - x0
        A[n+i][4*i] = float(1)
        A[n+i][4*i + 1] = h
        A[n+i][4*i + 2] = h ** 2
        A[n+i][4*i + 3] = h ** 3
        b[n+i] = float(data[i+1][1]) #y1

    # S'j-1(xj) = Sj'(xj)
    # b + 2ch+ 3dh^2 = 0
    for i in range(n - 1):
        h = float(data[i + 1][0]) - float(data[i][0])
        A[2*n + i][4 * i + 1] = float(1)
        A[2*n + i][4 * i + 2] = 2 * h
        A[2*n + i][4 * i + 3] = 3 * h ** 2
        A[2*n + i][4 * i + 5] = (-1)
        b[2*n + i] = float(0)

    # S''j-1(xj) = Sj''(xj)
    # 2c + 6dh = 0
    for i in range((n - 1)):
        h = float(data[i+1][0]) - float(data[i][0])
        A[2*n + (n-1) + i][4*i + 2] = float(2)
        A[2*n + (n-1) + i][4*i + 3] = 6*h
        A[2*n + (n-1) + i][4 * i + 6] = -2
        b[2*n + (n-1) + i] = float(0)

    # S''0(x0) = S''n-1(xn-1) = 0
    h = float(data[n][0]) - float(data[n-1][0])
    A[2*n + (n-1) + i +1 ][2] = float(1)
    A[2*n + (n-1) + i + 2][4*n-2] = float(2)
    A[2*n + (n-1) + i + 2][4*n -1] = 6*h

    result = lu_decomposition(A, b, 4*n)

    return result

def Spline():

    for file in os.listdir('./data'):
        singleFile = open('./data/' + file, 'r')
        data = csv.reader(singleFile)
        data = list(data)
        singleFile.close()

        part_points = 50                        #czesc punktow, co dziesiaty elemet do utworzenia podzbioru do interpolacji
        part_data = data[1::part_points]        #podzbior danych do interpolacji
        #data = [[1,6],[2, 4] ,[3, -2], [4,4], [5, 4]]
        #part_data = [[1,6], [3, -2], [5, 4]]

        """
        #LOSOWY WYBOR ROZMIESZCZENIA PUNKTOW
        rand_indexes = []
        number_of_points = 50
        part_data = []

        rand_indexes.append(int(1))
        for i in range(number_of_points-1):
            rand_indexes.append(random.randint(1, len(data)-1))
        rand_indexes.sort()
        rand_indexes = list(set(rand_indexes))
        rand_indexes.sort()

        for i in rand_indexes:
            part_data.append(data[i])
        """


        factors = SplineInterpolation(part_data)  #a0, b0, c0, d0, a1, a2...  - wynik z faktoryzacji LU

        #GRUPOWANIE WSPOLCZYNNIKOW
        factors_vector = []
        row = []
        for f in factors:
            row.append(f)
            if len(row) == 4:
                factors_vector.append(row)
                row = []

        #DOPASOWYWANIE DANYCH WEJSCIOWYCH DO ODPOWIEDNIEGO ZAKRESU
        interpolationResult = []
        for point in data[1:]:
            x = point[0]
            for i in range(1,len(part_data)):
                if float(part_data[i-1][0]) <= float(x) <= float(part_data[i][0]):
                    a, b, c, d = factors_vector[i-1]
                    h = float(x) - float(part_data[i - 1][0])  # x - x0
                    interpolationResult.append(a + b * h + (c * h ** 2) + (d * h ** 3))
                    break

        distance = []
        height = []
        for point in data[1:]:
            x = point[0]
            y = point[1]
            distance.append(float(x))  #dane rzeczywiste
            height.append(float(y))    #dane rzeczywiste

        difference = len(distance) - len(interpolationResult)   #roznica miedzy liczba danych x i y
        distance2 = distance[:(-1)*difference]
        part_distance = distance[::part_points]
        part_height = height[::part_points]

        """"
        # LOSOWY WYBOR ROZMIESZCZENIA PUNKTOW
        part_distance = []
        part_height = []
        for i in rand_indexes:
            part_distance.append(distance[i - 1])
            part_height.append(height[i - 1])
        """


        plt.scatter(distance, height, marker='.', color='green', label='dane rzeczywiste')
        plt.semilogy(distance2, interpolationResult, color='blue', label='funkcja interpolacji Spline')
        plt.scatter(part_distance, part_height, marker='.', color='red', label='podzbior danych rzeczywistych')
        plt.legend()
        plt.xlabel('Dystans [m]')
        plt.ylabel('Wysokosc [m]')
        plt.title('Interpolacja Spline ' + file)
        plt.savefig('Interpolacja Spline ' + file + '.png')
        plt.show()


        # BŁAD INTERPOLACJI
        new_data = data[1:]
        rms = 0.0
        for i in range(len(interpolationResult)):
            rms += (float(new_data[i][1]) - float(interpolationResult[i])) ** 2
        rms /= len(new_data)
        rms = rms ** 0.5
        print("Blad interpolacji: " + file + ": ", rms)

    return 0
