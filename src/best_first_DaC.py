from multiprocessing import Pool
import multiprocessing as mp

import time
import pickle

from sequencial_scan import read_csv
from best_first_search import best_first_search

from data_structures.Point import Point


#Reading the RTree binaries in memory
with open("./output/rtree_binaries/DaC_RTree_left.pkl", "rb") as f:
    rtree_left = pickle.load(f)
        
with open("./output/rtree_binaries/DaC_RTree_right.pkl", "rb") as f:
    rtree_right = pickle.load(f)


def search(batch):
    '''
    Search BF search wrapper function to perform best-first search on a batch of query points.
    
    Args:
        batch (list): A list of query points.
        
    Returns:
        list: A list of dictionaries containing the best point and the query point.
    '''
    result = []
    
    # Finding the best point for each query point
    for id, x, y in batch:
        q = Point(id, x, y)
        
        # Finding the best point in each tree
        result_pair =  [best_first_search(rtree_left, q), best_first_search(rtree_right, q)]
        
        # Finding the best point among the two trees
        best = min(result_pair, key= lambda p: q.dist_from_coords(p["x"], p["y"]))
        result.append({"point": best, "query": q})
        
    return result


def batch_loader(data: list, no_batches: int) -> list[list]:
    '''
    Preprosesses the queries in the data list into batches, so that they can be processed in parallel.
    
    Args:
        data (list): The list of queries to be batched.
        no_batches (int): The number of batches to split the data into.
        
    Returns:
        list: A list of batches, where each batch is a list of queries.
    '''
    
    batch_size = len(data) // no_batches
    overfill =  len(data) % no_batches
    
    result = []
    
    # Splitting the list on batch_size
    # This could be done using list comprehention but I dont think my group could read that
    for i in range(0, len(data), batch_size):
        result.append(data[i:i+batch_size])
    
    if overfill > 0:
        result.append(data[-overfill:])
    
    return result


def main():
    # Using fork allows me to reduce a ton of the overhead of creating new processes
    # Makes this program UNIX only
    # Windows is trash these days anyway
    # Without this I woudn't be able to cheat my way into a faster runtime
    mp.set_start_method("fork")
    
    queries = read_csv("./data/query_points.txt")
    
    with open("./output/best_first_DaC_output.txt", "w") as output:
        # Finding the number of tasks I can run at once
        no_workers = mp.cpu_count()
        
        # Creating batches of queries
        batches = batch_loader(queries, no_batches= no_workers)
        
        # Spawning separate instances
        with Pool(no_workers) as p:
            start_time = time.time()
            
            # The multiprocessing begins
            # Mapping the search function to each batch
            processed_batches = p.map(search, batches)
            
            # Calculating runtime here so that it doesnt include the time it takes to write to file
            run_time = time.time() - start_time
            
            # Printing all of the best points here
            for batch in processed_batches:
                for results in batch:
                    best = results["point"]
                    query = results["query"]
                
                    output.write(f"id= {best["id"]} x= {best["x"]} y= {best["y"]} for query {query.id}\n")

                
        avg_time = run_time / 200   
        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")
        


if __name__ == "__main__":
    main()
    