from methods import *
import os
import csv
import matplotlib.pyplot as plt
import random

def LagrangeInterpolation(point, data):

    result = 0
    x = point[0]
    y = point[1]
    index_i = 0
    for i in data:
        numerator = 1  #licznik
        denominator = 1 #mianownik
        xi = i[0]
        yi = i[1]

        index_j = 0
        for j in data:
            xj = j[0]
            yj = j[1]
            if index_i != index_j:
                numerator *= (float(x) - float(xj))
                denominator *= (float(xi) - float(xj))
            index_j += 1

        result += float(yi) * (numerator / denominator)
        index_i += 1
    return result


def Lagrange():

    for file in os.listdir('./data'):
        singleFile = open('./data/'+file, 'r')
        data = csv.reader(singleFile)
        data = list(data)
        singleFile.close()

        distance = []
        height = []
        interpolationResult = []
        part_points = 50                 #czesc punktow, co dziesiaty elemet do utworzenia podzbioru do interpolacji
        part_data = data[1::part_points]  #podzbior danych do interpolacji

        """
        #LOSOWY WYBOR ROZMIESZCZENIA PUNKTOW
        rand_indexes = []
        number_of_points = 50
        part_data = []

        for i in range(number_of_points):
            rand_indexes.append(random.randint(1, (len(data)-1)))
        rand_indexes.sort()
        rand_indexes = list(set(rand_indexes))
        rand_indexes.sort()

        for i in rand_indexes:
            part_data.append(data[i])
        """


        for point in data[1:]:
            x = point[0]
            y = point[1]
            distance.append(float(x))  #dane rzeczywiste
            height.append(float(y))    #dane rzeczywiste
            interpolationResult.append(float(LagrangeInterpolation(point, part_data)))

        # wektory podzbiorów danych rzeczywistych
        part_distance = distance[::part_points]
        part_height = height[::part_points]

        """
        #LOSOWY WYBOR ROZMIESZCZENIA PUNKTOW
        part_distance = []
        part_height = []
        for i in rand_indexes:
            part_distance.append(distance[i-1])
            part_height.append(height[i-1])
        """

        plt.scatter(distance, height, marker='.', color='green', label='dane rzeczywiste')
        plt.semilogy(distance, interpolationResult, color='blue', label='funkcja interpolacji Lagrangea')
        plt.scatter(part_distance, part_height, marker='.', color='red', label = 'podzbior danych rzeczywistych')
        plt.legend()
        plt.xlabel('Dystans [m]')
        plt.ylabel('Wysokosc [m]')
        plt.title('Interpolacja Lagrangea ' + file)
        plt.savefig('Interpolacja Lagrangea ' + file + '.png')
        plt.show()



        #BŁAD INTERPOLACJI
        new_data = data[1:]
        rms = 0.0
        for i in range(len(interpolationResult)):
            rms += (float(new_data[i][1]) - float(interpolationResult[i])) ** 2
        rms /= len(new_data)
        rms = rms ** 0.5
        print("Blad interpolacji: " + file + ": " ,rms)

    return 0
