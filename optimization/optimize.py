import csv

# Load the data from CSV
fileName = input("CSV to load data from: ")

with open(fileName, 'r') as file:
    csv_reader = csv.DictReader(file)
    data = [row for row in csv_reader]


# Data is a list of dictionaries each of which is one power plant
# Prompt user for target power production
target = int(input("Target power production in kWh (not bigger than the total production capacity of the set): "))
max_capacity = 0
for plant in data:
    max_capacity += plant["producción"]

# Hill-climbing: 
#   Consider all neighbours
#   Calculate the cost of all of them
#   Choose the best one