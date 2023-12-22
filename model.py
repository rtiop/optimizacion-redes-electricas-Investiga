import cs50
import random

TYPES_OF_PRODUCERS = [
    "Eólico",
    "Solar",
    "Mareomotriz",
    "Central eléctrica (petroleo)"
]

TYPES_OF_CONSUMERS = [
    "Hogares",
    "Industria",
    "Transportes"
]

class Producer():
    def __init__(self, type, x, y, id):
        if not type in TYPES_OF_PRODUCERS:
            raise TypeError
        self.type = type
        self.x = x
        self.y = y
        self.id = id
    def __str__(self):
        return f"{self.type} n{self.id}"

class Consumer():
    def __init__(self, type, x, y, id):
        if not type in TYPES_OF_CONSUMERS:
            raise TypeError
        self.type = type
        self.x = x
        self.y = y
        self.id =id
    def __str__(self):
        return f"{self.type} n{self.id}"

def main():
    
    number_of_producers = cs50.get_int("Número de productores: ")
    number_of_consumers = cs50.get_int("Número de consumidores: ")

    producers = []
    for n in range(number_of_producers):
        x = random.random()
        y = 2 * random.random()
        type = random.choice(TYPES_OF_PRODUCERS)
        producers.append(Producer(type,x,y,n+1))

    consumers = []
    for n in range(number_of_consumers):
        x = random.random()
        y = 2 * random.random()
        type = random.choice(TYPES_OF_CONSUMERS)
        producers.append(Consumer(type,x,y,n+1))
    raise NotImplementedError

main()