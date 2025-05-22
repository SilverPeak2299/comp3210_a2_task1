import pickle
import time

from rtree.RTree_supplied import RTree
from sequencial_scan import read_csv


def main():
    #finding the midpoint to split the rtree on
    resturants = read_csv("./data/restaurant_dataset.txt")
    x_max = max(resturants, key= lambda x: x[1])
    x_min = min(resturants, key= lambda x: x[1])
    dx = x_max[1] + x_min[1]
 
    middle_point = dx/2
    
    rtree_left = RTree()
    rtree_right = RTree()
    
    for id, x, y in resturants:
        if x < middle_point:
            rtree_left.insert(rtree_left.root, {"id": int(id),"x": float(x),"y": float(y)})
        else:
            rtree_right.insert(rtree_right.root, {"id": int(id),"x": float(x),"y": float(y)})
    
    # Saving Rtrees       
    with open("./output/rtree_binaries/DaC_RTree_left.pkl", "wb") as f:
        pickle.dump(rtree_left, f)
        
    with open("./output/rtree_binaries/DaC_RTree_right.pkl", "wb") as f:
        pickle.dump(rtree_right, f)
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Generated 2 trees in {time.time() - start_time} seconds")