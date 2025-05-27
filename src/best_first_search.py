import time
from data_structures.Point import Point
from data_structures.RTree import RTree, Node

import pickle

from sequencial_scan import read_csv


def main():
    with open("./output/rtree_binaries/best_first_rtree.pkl", "rb") as f:
        rtree = pickle.load(f)
    
    # Reading the query points from the file
    queries = read_csv("./data/query_points.txt")
    
    start_time = time.time()
    
    with open("./output/best_first_search_output.txt", "w") as output:
        
        # Searching each point in queries
        for id, x, y in queries:
            best = best_first_search(rtree, Point(id, float(x), float(y)))
            output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {id}\n")
        
        # Calculating the total runtime and average time per query
        run_time = time.time() - start_time
        avg_time = run_time / 200
        
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")

    
    
def best_first_search(rtree: RTree, q_point: Point) -> dict:
    '''
    An implementation of the best first search algorithm.
    
    Args: 
        rtree: The RTree to search.
        q_point: The query point.
    
    Returns:
        The closest point to the query point.
        is a dict in the form of {"id": int, "x": float, "y": float}
    '''
    list = []
    
    # Start by inserting the root
    list.append(rtree.root)
    
    # While the list is not empty
    while list:
        # Sort the list by min distance to query point
        list = sorted(list, key= lambda x : x.min_dist_to_point(q_point.x, q_point.y))
        
        # Getting the best element
        current = list.pop(0)
        
        # So my LSP will stop screaming at me about types
        assert(isinstance(current, Node))
        
        if current.is_leaf():
            # finding the closest point
            best = min(current.data_points, key= lambda x : q_point.dist(Point(x["id"], x["x"], x["y"])))
            return best

            
        else:
            # adding everything
            for child in current.child_nodes:
                list.append(child)               
    
    # If the queue is empty and no Point was found, return None or raise an error
    raise Exception(str("could find no point"))


if __name__ == "__main__":
    main()

