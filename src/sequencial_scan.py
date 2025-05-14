import csv
from time import time
import math

def main():
    datapoints = read_csv("./data/restaurant_dataset.txt")
    queries = read_csv("./data/query_points.txt")

    start_time = time()
    with open("./output/sequential_search_output.txt", "w") as output:
        for id, x ,y in queries:
            best = search((x, y), datapoints)
            output.write(f"id= {best[0]} x= {best[1]} y= {best[2]} for query {id}\n")

        run_time = time() - start_time
        avg_time = run_time / 200

        output.write(f"The total runtime was {run_time} seconds, Averaging {avg_time} seconds per query")


def search(location: tuple, datapoints: list) -> tuple:
    """From the location finds the closest datapoint
        Args:
            location (tuple): takes the form of (x, y), the coordiantes of the palce to check
            datapoints (list): the list of datapoints to check against
        Returns:
            tuple: (id, x, y) the closest location to the query point
    """
    best = None

    for id, x, y in datapoints:
        if best is None:
            best = (id, x, y)
            continue

        if distance(location, x, y) < distance(location, best[1], best[2]):
            best = (id, x, y)
            
    if best is None:
        raise Exception("returning best is none -- :(")
    
    return best

        

def distance(location: tuple, x:float, y:float) -> float:
    """Returns the euclidan distance between 2 locations"""
    x_dist = abs(location[0] - x)
    y_dist = abs(location[1] - y)

    return math.sqrt(x_dist**2 + y_dist**2)




def read_csv(file_path: str) -> list:
    """ Reads CSVs and return them as lists
        Args:
            file_path (str): the path of the csv to read.
        Returns: 
            List: A list of tuples that contain the fields (ID, X, Y).
    """
    result = []

    with open(file_path) as file:
        csv_reader = csv.reader(file, delimiter=" ")

        for id, x, y in csv_reader:
            result.append((id, float(x) ,float(y)))

    return result

    
            


if __name__ == "__main__":
    main()
