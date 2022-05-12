


from models import load_graph_and_cities
import networkx as nx

g, city_dict = load_graph_and_cities()

from math import sin, cos, sqrt, atan2, radians
def straight_line_distance(  src_city_name , goal_city_name ):
        
        # approximate radius of earth in km
        R = 6373.0
        
        src = city_dict[src_city_name]
        goal = city_dict[goal_city_name]
        
        lat1 = radians(src.lat)
        lon1 = radians(src.lng)
        lat2 = radians(goal.lat)
        lon2 = radians(goal.lng)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c * 1000
        
        print(f"Heuristic called for {src_city_name}, {goal_city_name} and returned {distance}")
        
        return distance

print(nx.astar_path(g, "Rahat", "Tiberias", heuristic=straight_line_distance, weight="driving_cost"))