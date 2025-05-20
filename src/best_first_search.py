import time
from rtree.Point import Point
from rtree.RTree_supplied import RTree, Node
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
            print(f"Finding {id} {x} {y}")
            best = best_first_search(rtree, Point(id, float(x), float(y)))
            
            output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {id}\n")
        
        run_time = time.time() - start_time
        avg_time = run_time / 200
        
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")

    
    
def best_first_search(rtree: RTree, q_point: Point) -> dict:
    priority_q = PriorityQueue()
    itter_count = 0
    
    # Start by inserting the root
    priority_q.insert(rtree.root.min_dist_to_point(q_point.x, q_point.y), rtree.root)
    
    while not priority_q.head == None:
        itter_count += 1
        
        current = priority_q.pop()
        assert(isinstance(current, Node))
        
        if current.is_leaf():
            try:
                best = min(current.data_points, key= lambda x : q_point.dist(Point(x["id"], x["x"], x["y"])))
                return best
                
            except ValueError:
                print(current.is_leaf())
                continue
            
        else:
            for child in current.child_nodes:
                priority_q.insert(child.min_dist_to_point(q_point.x, q_point.y), child)                
    
    # If the queue is empty and no Point was found, return None or raise an error
    raise Exception(str("could find no point " + str(itter_count)))

if __name__ == "__main__":
    main()

