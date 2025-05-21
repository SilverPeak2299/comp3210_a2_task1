from multiprocessing import Pool
import time
import pickle
from sequencial_scan import read_csv
from best_first_search import best_first_search

from rtree.Point import Point

def search(args):
    rtree, queries = args
    result = []
    
    for id, x, y in queries:
        q = Point(id, x, y)
        best =  best_first_search(rtree, q)
        result.append({"point": best, "dist": q.dist(Point(best["id"], best["x"], best["y"]))})
        
    return result


def main():

    with open("./output/rtree_binaries/DaC_RTree_left.pkl", "rb") as f:
        rtree_right = pickle.load(f)
        
    with open("./output/rtree_binaries/DaC_RTree_right.pkl", "rb") as f:
        rtree_left = pickle.load(f)
        
    queries = read_csv("./data/query_points.txt")
    
    with open("./output/best_first_DaC_output.txt", "w") as output:    
        with Pool(2) as p:
            start_time = time.time()
            left_result, right_result = p.map(search, [[rtree_left, queries], [rtree_right, queries]])
            
            for results in zip(left_result, right_result):
                best = min(results, key= lambda p: p["dist"])
                best = best["point"]
                
                output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {id}\n")

            
        
        run_time = time.time() - start_time
        avg_time = run_time / 200
        
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")
        


if __name__ == "__main__":
    main()
    