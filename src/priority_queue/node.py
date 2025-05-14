class Node:
    dist: float
    next = None
    data = None
    
    def __init__(self, dist: float, next= None, data= None):
        self.dist = dist
        self.next = next
        self.data = data
        
if __name__ == "__main__":
    pass