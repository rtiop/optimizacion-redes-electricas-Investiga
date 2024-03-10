import csv
import copy
import math
from random import choice, random

def main():
    # Load the data from CSV
    fileName = input("CSV to load data from: ")

    with open(fileName, 'r') as file:
        csv_reader = csv.DictReader(file)
        data = [row for row in csv_reader]


    # Data is a list of dictionaries each of which is one power plant

    # Change data type of all data to integer    
    for station in data:
            station ["id"] = int(station["id"])
            station ["co2"] = float(station["co2"])
            station ["precio"] = float(station["precio"])
            station ["producción"] = float(station["producción"])


    # Prompt user for target power production
    target = int(input("Target power production in kWh (not bigger than the total production capacity of the set): "))
    max_capacity = 0
    for plant in data:
        max_capacity += plant["producción"]

    # Check if the target is in the possible range
    if target > max_capacity:
        raise ValueError("Target above max production capacity.")
    
    # Get CO2 cost coefficient
    co2Coef = max(0,float(input("Coefficient for CO2 cost (min 0): ")))


    # Create initial configuration (all active)
    arrangement = []
    for x in data:
        arrangement.append(dict(id = x["id"], activity = True))

    # Set max_temperature according to the size of the problem
    max_temperature = int(2*math.sqrt(len(data)))

    # Simulated annealing:
    #   Run hill climbing
    #   With a certain probability choose a different random arrangement
    #   
    done = False
    temperature = max_temperature
    best_arrangement = arrangement
    while done == False:
        neighbours = find_neighbours(data, arrangement)
    
        # Calculate the cost of all neighbours and find the smallest cost
        costs = []
        min_cost = math.inf
        for x in neighbours:
            current_cost = cost(data,x, target, co2Coef)
            costs.append(current_cost)
            min_cost = min(min_cost, current_cost)

        # Find the arrangement with the smallest cost (optimal neighbour) 
        # If better, choose it. Else maybe choose it.
        if min_cost < cost(data, arrangement, target, co2Coef):
            for x in range(len(costs)):
                if costs[x] == min_cost:
                    arrangement = copy.deepcopy(neighbours[x])
        elif random() < temperature/max_temperature:
            arrangement = random_arrangement(data)
            temperature = max(1, temperature-1)
        else:
            done = True
        if cost(data, best_arrangement, target, co2Coef) > cost(data, arrangement, target, co2Coef):
            best_arrangement = copy.deepcopy(arrangement)
                

    # Calculate performance of the solution given
    production = 0
    co2 = 0
    price = 0
    min_cost = cost(data, best_arrangement, target, co2Coef)
    for x in range(len(data)):
        if best_arrangement[x]["activity"] == True:
            production += data[x]["producción"]
            co2 += data[x]["co2"]
            price += data[x]["precio"]
    difference = production - target
    co2_per_kwh = co2/production
    price_per_kwh = price/production
    print("Difference between production and target = "+ str(difference))
    print("CO2 per kWH = " + str(co2_per_kwh) + " kCO2-eq/kWh")
    print("Price per kWH = " + str(price_per_kwh) + " Euros/kWh")
    print(best_arrangement)
    print("Cost of solution = " + str(min_cost))



def cost(data, arrangement, target, co2Coef):
    cost = 0
    production = 0
    co2 = 0
    price = 0
    for x in range(len(data)):
        if arrangement[x]["activity"] == True:
            production += data[x]["producción"]
            co2 += data[x]["co2"]
            price += data[x]["precio"]

    productionCost = 10 * max(0,(target - production))
    co2Cost = co2Coef * co2
    priceCost = price
    cost = productionCost + co2Cost + priceCost
    return cost

def find_neighbours(data, arrangement):
    first_level_neighbours = list()
    second_level_neighbours = list()
    arrangement = list(arrangement)

    # Add neighbours (one difference) of the present arrangement
    for x in range(len(data)):
        new_neighbour = copy.deepcopy(arrangement)
        new_neighbour[x]["activity"] ^= True
        first_level_neighbours.append(new_neighbour)

    # Add neighbours of neighbours
    for current_neighbour in first_level_neighbours:
        for x in range(len(data)):
            new_neighbour = copy.deepcopy(current_neighbour)
            new_neighbour[x]["activity"] ^= True
            second_level_neighbours.append(new_neighbour)
    
    neighbours = first_level_neighbours + second_level_neighbours
    final_neighbours = []

    # Remove duplicates
    for x in neighbours:    
        if x not in final_neighbours:
            final_neighbours.append(x)

    # Remove original arrangement
    while arrangement in final_neighbours:
        final_neighbours.remove(arrangement)        

    return final_neighbours

def random_arrangement(data):
    arrangement = []
    for x in range(len(data)):
        arrangement.append(dict(id=x, activity=choice([True, False])))
    return arrangement
    
main()