from math import sin, cos, sqrt, atan2, radians

class City():
    ''' class representing a node (city) '''
    
    def __init__(self, name: str, latitude: float, longitude: float) -> None:
        
        self.lat = latitude
        self.lng = longitude
        
        self.name = name 
        
    # Heruistic Function
    def straight_line_distance( src,goal ):
        
        # approximate radius of earth in km
        R = 6373.0
        
        lat1 = radians(src.lat)
        lon1 = radians(src.lng)
        lat2 = radians(goal.lat)
        lon2 = radians(goal.lng)
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        distance = R * c
        
        return distance
        
    def __str__(self) -> str:
        
        return f"City[ name={self.name}, lat={self.lat}, lng={self.lng}]"
        