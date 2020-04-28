import random
import math


class City:
    """Contains coordinates and id of a city"""

    def __init__(self, cityId, x, y):
        self.id = cityId
        self.x = x
        self.y = y


# dajmy ograniczenie, że muszą być przynajmniej 3 miasta. Huk, że dla 2 jest to oczywiste
# ale też 2 miasta wywalają program
def randomCityGenerator():  # creates 5 cities with random coordinates
    listOfCities = []

    print("Input '1' for 5 random cities or '2' for custom coordinates: ")
    mode = input()
    mode = int(mode)
    if mode != 1 and mode != 2:
        print("\n ERROR! Please choose 1 for random mode and 2 for custom mode.")
        exit()
    elif mode==1:
        random.seed(0)  # THIS WILL STOP RANDOM EXECUTION EACH TIME AND SAVE ONE STATE,
        for i in range(1, 6):  # FOR THE PURPOSE OF TESTING, Remove to make program use different
            xi = random.randrange(1, 250)  # numbers each time
            yi = random.randrange(1, 250)
            newCity = City(i, xi, yi)
            listOfCities.append(newCity)
    elif mode==2:
        for i in range(1, 6):
            print("\nPlease choose x{}".format(i), "coordinate:")
            xi = input()
            xi = int(xi)
            if xi < 1 or xi > 250:
                print("\n ERROR! Please choose x and y values in range 1 to 250.")
                exit()
            print("\nPlease choose y{}".format(i), "coordinate:")
            yi = input()
            yi = int(yi)
            if yi < 1 or yi > 250:
                print("\n ERROR! Please choose x and y values in range 1 to 250.")
                exit()
            newCity = City(i, xi, yi)
            listOfCities.append(newCity)

    return listOfCities


def calculateDistance(x1, y1, x2, y2):  # calculates distance between two given (x,y) coordinates
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # and returns positive value
    return round(dist, )


def calculateRoadsDistance(listOfCities):
    noOfCities = len(listOfCities)
    listOfPaths = []
    for i in range(0, noOfCities):
        for j in range(i + 1, noOfCities):
            path = calculateDistance(listOfCities[i].x, listOfCities[i].y,
                                     listOfCities[j].x, listOfCities[j].y)
            listOfPaths.append(path)

    return listOfPaths


def calcHeuristicFunction(w1, w2, w_graph):
    allPaths = []
    # get all weights from graph
    for i in range(0, len(w_graph.nodes)):
        for j in range(i + 1, len(w_graph.nodes)):
            path = w_graph.get_weight(i, j)
            allPaths.append(path)

    heuristic = w1 * calcTotalLength(allPaths) + w2 * calcAvgLength(w_graph)
    return heuristic


def calcTotalLength(allPaths):
    totalLength = sum(list(allPaths))
    return totalLength


# calculate average distance between 2 cities using dijkstra's algo
def calcAvgLength(w_graph):
    # list of distances between cities by dijkstra's algo
    total_distances = []
    # calculate shortest path to all cities for all cities
    for i in range(0, len(w_graph.nodes)):
        nodenum = w_graph.get_index_from_node(i)
        # Make a list keeping track of distance from node to any node
        # in self.nodes. Initialize to infinity for all nodes but the
        # starting node, keep track of "path" which relates to distance.
        dist = [None] * len(w_graph.nodes)
        for i in range(len(dist)):
            dist[i] = float("inf")

        dist[nodenum] = 0
        # Queue of all nodes in the graph
        queue = [i for i in range(len(w_graph.nodes))]
        # Set of numbers seen so far
        seen = set()
        while len(queue) > 0:
            # Get node in queue that has not yet been seen
            # that has smallest distance to starting node
            min_dist = float("inf")
            min_node = None
            for n in queue:
                if dist[n] < min_dist and n not in seen:
                    min_dist = dist[n]
                    min_node = n

            # Add min distance node to seen, remove from queue
            queue.remove(min_node)
            seen.add(min_node)
            # Get all next hops
            connections = w_graph.connections_from(min_node)
            # For each connection, update its path and total distance from
            # starting node if the total distance is less than the current distance
            # in dist list
            for (node, weight) in connections:
                tot_dist = weight + min_dist
                if tot_dist < dist[node.index]:
                    dist[node.index] = tot_dist
                    total_distances.append(tot_dist)

    avgLength = sum(list(total_distances)) / len(total_distances)
    return avgLength
