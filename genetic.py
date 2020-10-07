import math
import random

# Town object, contains x and y position of towns on a cartesian plane
class Town:
    # Basic contstructor, allows initialization with defined position
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Method to determine Euclidean distance between two Towns
    def toNextTown(self, nextTown):
        deltaX = abs(self.x - nextTown.x)
        deltaY = abs(self.y - nextTown.y)
        distance = math.sqrt(pow(deltaX, 2) + pow(deltaY, 2))
        return distance

# Salesman object, contains a list of Towns to visit in order, distance, and fitness value
class Salesman:

    # Basic constructor, allows initialization of a Salesman with an exisiting list of Towns
    def __init__(self, townList):
        self.distance = 0
        self.townList = townList
        random.shuffle(self.townList) #shuffle to randomize Town visit order

        # For loop iterates through list of towns and totals the distance to visit each town
        for town in range(0, len(townList)):
            if (town + 1) < len(townList):
                self.distance += townList[town].toNextTown(townList[town + 1])
            else:
                self.distance += townList[town].toNextTown(townList[0])

        self.fitness = 1/self.distance # Assign fitness based on distance to visit each town

# Population object, contains a list of Salesman and fittest Salesman
class Population:

    # Basic constructor, allows initialization of a Salesman population from a list of Towns
    def __init__(self, townList, populationSize):
        self.salesmanList = []
        self.populationSize = populationSize

        # For loop to fill population with Salesman objects
        for i in range(0, populationSize):
            self.salesmanList.append(Salesman(townList))

    # Method to overwrite salesmanList memeber for lack of multiple constructors
    def overwriteSalesmanList(self, salesmanList):
        self.salesmanList = salesmanList

    # Method loops through population of Salesman and finds the most fit Salesman
    def fittest(self):
        self.fittest = self.salesmanList[0]
        for salesman in range(1, len(self.salesmanList)):
            if(self.fittest.fitness < self.salesmanList[salesman].fitness):
                self.fittest = self.salesmanList[salesman]
            else:
                continue
        return self.fittest

# Genetic_Algorithm object, contains methods to evolve population, create children, and mutate
# Takes in a list of Towns and Population
class Genetic_Algorithm:

    #Basic constructor, allows initialization of Genetic_Alforithm from Towns and Population
    def __init__(self, townList, population):
        self.townList = townList
        self.population = population
        self.sampleSize = 10 # Number of Salesman randomly selected from the population
        self.mutationRate = 0.01 # 1% chance of children having town indexs swapped

    # Method to evolve the population
    def evolve(self):
        # Create a list of next generation Salesman
        nextGen = []

        for i in range(0, len(self.population.salesmanList)):
            nextGen.append(self.createChild())

        # create and return new population object after overwriting with list of children
        nextPopulation = Population(self.townList, self.population.populationSize)
        nextPopulation.overwriteSalesmanList(nextGen)
        return nextPopulation

    # Method to create a child from two parent Salesman
    def createChild(self):
        child = Salesman(self.townList)

        # copy two random sample populations from the createSample method
        samplePopulation1 = self.createSample()
        samplePopulation2 = self.createSample()

        # Choose most fit parent from both samples
        parent1 = samplePopulation1.fittest()
        parent2 = samplePopulation2.fittest()

        # create random index point on child, each section has one parent's genes
        randomIndex = int(random.random() * len(self.townList))

        # for loop copying the Town lists of each parent's based upon random index
        for i in range(0, len(self.townList)):
            if i < randomIndex:
                child.townList[i] = parent1.townList[i]
            else:
                child.townList[i] = parent2.townList[i]

        if(random.random() <= self.mutationRate):
            child = self.mutateChild(child)
        return child

    # Method to mutate a child by swapping towns at random indexes
    def mutateChild(self, child):
        randomTown1 = int(random.random() * len(child.townList))
        randomTown2 = int(random.random() * len(child.townList))
        child.townList[randomTown1], child.townList[randomTown2] = child.townList[randomTown2], child.townList[randomTown1]
        return child

    # Method to create sample group of random Salesman from the initial population
    def createSample(self):
        sampleGroup = []
        for i in range(0, self.sampleSize):
            randomSalesman = int(random.random() * len(self.population.salesmanList))
            sampleGroup.append(self.population.salesmanList[randomSalesman])
        samplePopulation = Population(townList, self.sampleSize)
        samplePopulation.overwriteSalesmanList(sampleGroup)
        return samplePopulation

# Here, the code is executed sequentially

# Create a list of all towns
townList = []

# Create and append all towns to townList
for i in range(0, 10):
    randomX = int(random.random() * 100)
    randomY = int(random.random() * 100)
    townList.append(Town(randomX, randomY))

# Creating Population of fifty Salesman, Salesman are auto generated
salesmanPopulation = Population(townList, 50)

# Print out the untermensch
print("Gen 1 distances")
for salesman in salesmanPopulation.salesmanList:
    print(salesman.distance)

# Creating Genetic_Algorithm object from salesmanPopulation and townList
ga = Genetic_Algorithm(townList, salesmanPopulation)

# Evolving the population 100 times
for i in range(0, 1000):
    salesmanPopulation = ga.evolve()

# Print out the distances of the supersolden
print("Gen 100 distances")
for salesman in salesmanPopulation.salesmanList:
    print(salesman.distance)
