from node import Node

class PriorityQueue:
    head: Node
    
    def __init__(self, head:Node = None):
        self.head = head
    
    
    def insert(self, dist:float, data):        
        #If the list is empty
        if self.head is None:
            self.head = Node(dist= dist, data= data)
            return

        #Inserting into the start of the list
        if (dist < self.head.dist):
            self.head = Node(dist= dist, next= self.head, data= data)
            return
            
        prev_node = self.head
        curr_node = self.head.next
        
        while (curr_node is not None and curr_node.dist < dist):
            prev_node = prev_node.next
            curr_node = curr_node.next
            
        prev_node.next = Node(dist= dist, data= data, next= curr_node)
        
        
    def pop(self):
        if (self.head is None):
            raise Exception("list is empty")
            
        data = self.head.data
        self.head = self.head.next
        return data
        
            
        
        
        
        
if __name__ == "__main__":
    queue = PriorityQueue()
    queue.insert(3, "node 1")
    queue.insert(4, "node 2")
    queue.insert(7, "node 3")
    queue.insert(5, "node 4")
    queue.insert(1, "node 5")
    
    current_node = queue.head
    while current_node is not None:
        print(current_node.dist)
        current_node = current_node.next
        
    print(queue.pop())
    print(queue.pop())
