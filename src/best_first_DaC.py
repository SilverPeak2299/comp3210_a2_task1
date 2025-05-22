import time
import pickle
from sequencial_scan import read_csv
from best_first_search import best_first_search

from rtree.Point import Point


def main():

    with open("./output/rtree_binaries/DaC_RTree_left.pkl", "rb") as f:
        rtree_right = pickle.load(f)
        
    with open("./output/rtree_binaries/DaC_RTree_right.pkl", "rb") as f:
        rtree_left = pickle.load(f)
        
    queries = read_csv("./data/query_points.txt")
    start_time = time.time()

    with open("./output/best_first_DaC_output.txt", "w") as output:    
        for id, x, y in queries:
            q_point = Point(id, x, y)
            result = [best_first_search(rtree_left, q_point), best_first_search(rtree_right, q_point)]
            best = min(result, key= lambda p: q_point.dist(Point(p["id"], p["x"], p["y"])))
            
            output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {id}\n")

        run_time = time.time() - start_time
        avg_time = run_time / 200
        
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")
        


if __name__ == "__main__":
    main()
    