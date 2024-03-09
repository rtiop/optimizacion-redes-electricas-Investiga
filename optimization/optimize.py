import csv
import copy

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
    co2Coef = max(0,float(input("Coeficient for CO2 cost (min 0): ")))


    # Create initial configuration (all active)

    arrangement = []
    for x in data:
        arrangement.append(dict(id = x["id"], activity = True))


    # Hill-climbing: 
    #   Consider all neighbours
    #   Calculate the cost of all of them
    #   Choose the best one
    done = False
    while done == False:
        neighbours = find_neighbours(data, arrangement)
        costs = []
        for x in neighbours:
            costs.append(cost(data,x, target, co2Coef))
        min_cost = min(costs)


def cost(data, arrangement, target, co2Coef):
    cost = 0
    production = 0
    co2 = 0
    price = 0
    for x in arrangement:
        if x["activity"] == True:
            production += data[x["id"]]["producción"]
            co2 += data[x["id"]]["co2"]
            price += data[x["id"]]["price"]

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
    
main()