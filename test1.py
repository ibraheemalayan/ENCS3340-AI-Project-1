import csv
from typing import List

import requests

from models import City

import networkx as nx

count = 0

def get_distance(origins, destinations):

    global count

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    # deepcode ignore HardcodedNonCryptoSecret: <>
    API_KEY = "AIzaSyBAXXKZP6Sdl22Hg0m4JaWecuPnwFpqGow"
    
    args = {
        "key": API_KEY,
        "units": "si",
        "origins": origins,
        "destinations": destinations,    
        "mode": "walking" # "driving"
    }
    
    headers = {
        "Accept": "application/json"
    }
    
    response = requests.request("GET", url, headers=headers, params=args)
    
    
    
    for row in response.json()["rows"]:
        
        for el in row["elements"]:
            print(el["distance"]["value"])
            count += 1
        
        print("\n")
        
    
    
cities: List[City] = []

g = nx.Graph()


def read_csv():

    with open('city_coordinates.csv') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            
            
            c = City(name=row[0], latitude=float(row[1]), longitude=float(row[2]))
            cities.append( c )
            
            g.add_node(c)
            
            for city in cities[:-1]:
                g.add_edge(c, city, driving_distance=23, walking_distance=20)    
                
            
            # print( f"{c.lat},{c.lng}|", end ="")
            
            
            
read_csv()






worklist=[]





max=6
for i in range(max):

    for j in range(5):

        noor = j + i*5
        worklist.append(cities[noor])
        
    destinations_sourcs = "|".join([ f"{city.lat},{city.lng}" for city in worklist])
    
    get_distance(destinations_sourcs, destinations_sourcs)
    
    print (worklist)
    worklist=[]
    
print(count)