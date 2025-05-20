import time
from rtree.rtree import RTree, Point, Rectangle
from priority_queue.priority_queue import PriorityQueue
import pickle

from sequencial_scan import read_csv

def main():
    with open("./output/best_first_rtree.pkl", "rb") as f:
        rtree = pickle.load(f)
    
    queries = read_csv("./data/query_points.txt")
    
   
    start_time = time.time()
    with open("./output/best_first_seach_output.txt", "w") as output:
        for id, x, y in queries:
            best = best_first_search(rtree, Point(id, float(x), float(y)))
            
            output.write(f"id= {best.id} x= {best.x} y= {best.y} for query {id}\n")
        
        run_time = time.time() - start_time
        avg_time = run_time / 200
        
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")

    
    
def best_first_search(rtree: RTree, q_point: Point) -> Point:
    priority_q = PriorityQueue()
    
    # Start by inserting the root
    priority_q.insert(rtree.head.dist_from(q_point.x, q_point.y), rtree.head)
    
    while not priority_q.head == None:
        current = priority_q.pop()
        
        if current.is_leaf():
            best = min(current.data_list, key= lambda x : x.dist(q_point))
            return best
            
        if isinstance(current, Rectangle):
            for child in current.data_list:
                priority_q.insert(child.dist_from(q_point.x, q_point.y), child)
    
    # If the queue is empty and no Point was found, return None or raise an error
    raise Exception("could find no point")   

if __name__ == "__main__":
    main()

