import csv
import copy
import math
from random import choice

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

    # Get number of tries
    tries = int(input("Number of tries: "))

    prices = []
    co2s = []
    differences = []
    costs = []

    for n in range(tries):
        arrangement = random_arrangement(data)
        production = 0
        co2 = 0
        price = 0
        for x in range(len(data)):
            if arrangement[x]["activity"] == True:
                production += data[x]["producción"]
                co2 += data[x]["co2"]
                price += data[x]["precio"]
        prices.append(price/production)
        co2s.append(co2/production)
        differences.append(production - target)
        costs.append(cost(data,arrangement, target, co2Coef))

    av_difference = sum(differences)/len(differences)
    av_co2 = (sum(co2s)/len(co2s))
    av_price = (sum(prices)/len(prices))
    av_cost = sum(costs)/len(costs)
    print("Average difference between production and target = "+ str(av_difference))
    print("Average CO2 per kWH = " + str(av_co2) + " kCO2-eq/kWh")
    print("Average price per kWH = " + str(av_price) + " Euros/kWh")
    print("Average cost = " + str(av_cost))



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
    
def random_arrangement(data):
    arrangement = []
    for x in range(len(data)):
        arrangement.append(dict(id=x, activity=choice([True, False])))
    return arrangement

main()