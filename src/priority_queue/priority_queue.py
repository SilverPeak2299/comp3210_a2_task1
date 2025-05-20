from .node import Node

class PriorityQueue:
    head: Node
    size: int
    
    def __init__(self, head:Node = None):
        self.head = head
        self.size = 0
    
    
    def insert(self, dist:float, data):
        self.size += 1
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
        self.size -= 1
        
        if (self.head is None):
            raise Exception("list is empty")
            
        data = self.head.data
        self.head = self.head.next
        return data
        
    def print_queue(self):
        current_node = self.head
        while current_node is not None:
            print(f"{current_node.dist}    {current_node.data}")
            current_node = current_node.next

        
            
        
        
        
        
if __name__ == "__main__":
    queue = PriorityQueue()
    queue.insert(3, "node 1")
    queue.insert(4, "node 2")
    queue.insert(7, "node 3")
    queue.insert(5, "node 4")
    queue.insert(1, "node 5")
    
        
    print(queue.pop())
    print(queue.pop())
