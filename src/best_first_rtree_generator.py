import csv
import pickle

import time

from rtree.RTree_supplied import RTree

def main():
    start_time = time.time()
    rtree = RTree()

    with open("./data/restaurant_dataset.txt") as f:
        csv_reader = csv.reader(f, delimiter=" ")

        for id, x, y in csv_reader:
            rtree.insert(rtree.root, {"id": int(id),"x": float(x),"y": float(y)})
    
    with open("./output/rtree_binaries/best_first_rtree.pkl", "wb") as f:
        pickle.dump(rtree, f)

    print(f"Time to generate rtree: {round(time.time() - start_time, 4)} seconds")


if __name__ == "__main__":
    main()