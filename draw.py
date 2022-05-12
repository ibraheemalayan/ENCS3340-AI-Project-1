import networkx as nx
from json import load

from models import City

import matplotlib.pyplot as plt

data = None
with open("res.json", "r") as res_file:
    data = load(res_file)

g = nx.DiGraph()

for node in data["nodes"]:
    
    g.add_node(
        node["id"]["name"],
        latitude=node["id"]["lat"],
        longitude=node["id"]["lng"],
        pos=(node["id"]["lng"],node["id"]["lat"]))
    
edge_count = 0

for e in data["links"]:
    
    src_city = e["source"]["name"]
    
    target_city = e["target"]["name"]
    
    if src_city == target_city:
        continue
    
    City
    
    if e["driving_cost"] < 3000:
        continue
        
    if e["driving_cost"] > 50000:
        continue
    
    edge_count += 1
    
    
    g.add_edge(src_city, target_city, driving_cost=e["driving_cost"], walking_cost=e["walking_cost"])

pos=nx.get_node_attributes(g,'pos')
d_costs=nx.get_edge_attributes(g,'driving_cost')

print(f"d_costs is {d_costs}")

print(edge_count)
nx.draw_networkx(g, pos, cmap = plt.get_cmap('jet'), with_labels=True)
nx.draw_networkx_edge_labels(g,pos,edge_labels=d_costs)
plt.show()
