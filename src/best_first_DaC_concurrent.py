from multiprocessing import Pool
import multiprocessing as mp
import time
import pickle
from sequencial_scan import read_csv
from best_first_search_array import best_first_search

from rtree.Point import Point

with open("./output/rtree_binaries/DaC_RTree_left.pkl", "rb") as f:
    rtree_left = pickle.load(f)
        
with open("./output/rtree_binaries/DaC_RTree_right.pkl", "rb") as f:
    rtree_right = pickle.load(f)



def search(batch):
    result = []
    
    for id, x, y in batch:
        q = Point(id, x, y)
        result_pair =  [best_first_search(rtree_left, q), best_first_search(rtree_right, q)]
        best = min(result_pair, key=lambda p: q.dist_from_coords(p["x"], p["y"]))
        result.append({"point": best, "query": q})
        
    return result

def batch_loader(data: list, no_batches: int) -> list[list]:
    batch_size = len(data) // no_batches
    overfill =  len(data) % no_batches
    
    result = []
    # Splitting the list on batch_size
    for i in range(0, len(data), batch_size):
        result.append(data[i:i+batch_size])
    
    if overfill > 0:
        result.append(data[-overfill:])
    
    return result

def main():
    mp.set_start_method("fork")
    queries = read_csv("./data/query_points.txt")
    
    with open("./output/best_first_DaC_output.txt", "w") as output:
        no_workers = mp.cpu_count()
        
        batches = batch_loader(queries, no_batches= no_workers)
        
        with Pool(no_workers) as p:
            start_time = time.time()
            processed_batches = p.map(search, batches)
            run_time = time.time() - start_time
            
            for batch in processed_batches:
                for results in batch:
                    best = results["point"]
                    query = results["query"]
                
                    output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {query.id}\n")

                
        avg_time = run_time / 200   
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")
        


if __name__ == "__main__":
    main()
    