# COMP3210 Assignment 2 Task 1
All txt output files can be found in the `output/` directory.

  Note: Due to the use of the fork parameter when establishing multiprocessing the scripts can only be run on UNIX systems.

## File Structure
- `data/`: The data files for the project
- `output/`: The output files for the project
- `output/rtee_binaries/`: The binary rtree files
- `src/`: The code to complete the project
- `src/data_structures/`: The data structures used in the project

## Steps for Replication
All scripts should be run from the root directory of the project.

1. Create a veritual enviroment (I mean only using STD so not really nesasery but I did)
2. Execute sequential search - `python src/sequential_search.py`
3. Generate rtree for best first search - `python src/best_first_rtree_generator.py`
4. Execute best first search - `python src/best_first_search.py`
5. Generate the split rtrees for divide and conquer search - `python src/divide_and_conquer_rtree_generator.py`
6. Execute divide and conquer search - `python src/best_first_DaC.py`

## General Comments
- I asked in lectures if I could use parallelism and was told I could.
- I initally wrote this using a prioity queue instead of a list, but it was too fast and the overhead of the DaC made it slower on such a small dataset.
- I wrote the multiprocessing approach to try cheat my way around the time requirement when I was still using the priority queue and left it after I swapped to a list, because it is just better and I thought it would give me something to talk about in the presentation.
- Python kinda sucks so I had to limit this to unix based systems to avoid alot of the multiprocessing overhead.

## System Snapshot
### Project File Tree
```zsh
❯ tree --charset=ascii
.
|-- data
|   |-- parking_dataset.txt
|   |-- query_points.txt
|   |-- restaurant_dataset.txt
|   `-- shop_dataset.txt
|-- output
|   |-- best_first_DaC_output.txt
|   |-- best_first_search_output.txt
|   |-- rtree_binaries
|   |   |-- best_first_rtree.pkl
|   |   |-- DaC_RTree_left.pkl
|   |   `-- DaC_RTree_right.pkl
|   `-- sequential_search_output.txt
|-- README.md
`-- src
    |-- __pycache__
    |   |-- best_first_search_array.cpython-312.pyc
    |   |-- best_first_search.cpython-312.pyc
    |   `-- sequencial_scan.cpython-312.pyc
    |-- best_first_DaC.py
    |-- best_first_rtree_generator.py
    |-- best_first_search.py
    |-- data_structures
    |   |-- __pycache__
    |   |   |-- Point.cpython-312.pyc
    |   |   |-- RTree_supplied.cpython-312.pyc
    |   |   `-- RTree.cpython-312.pyc
    |   |-- Point.py
    |   `-- RTree.py
    |-- divide_and_conquer_rtree_generator.py
    `-- sequencial_scan.py
```

### Python Info
```zsh
❯ python --version
Python 3.12.7
```

### System Info
```zsh
❯ neofetch
                    'c.
                 ,xNMM.
               .OMMMMo
               OMMM0,
     .;loddo:' loolloddol;.
   cKMMMMMMMMMMNWMMMMMMMMMM0:
 .KMMMMMMMMMMMMMMMMMMMMMMMWd.
 XMMMMMMMMMMMMMMMMMMMMMMMX.
;MMMMMMMMMMMMMMMMMMMMMMMM:
:MMMMMMMMMMMMMMMMMMMMMMMM:       danny@192-168-1-14.tpgi.com.au
.MMMMMMMMMMMMMMMMMMMMMMMMX.      ------------------------------
 kMMMMMMMMMMMMMMMMMMMMMMMMWd.    OS: macOS 15.5 24F74 arm64
 .XMMMMMMMMMMMMMMMMMMMMMMMMMMk   Host: Mac15,12
  .XMMMMMMMMMMMMMMMMMMMMMMMMK.   Kernel: Darwin 24.5.0
    kMMMMMMMMMMMMMMMMMMMMMMd     Uptime: 6d 18h 20m
     ;KMMMMMMMWXXWMMMMMMMk.      Shell: zsh 5.9
       .cooc,.    .,coo:.        Resolution: 1470x956 @ 60Hz
                                 CPU: Apple M3
                                 Memory: 2.87GiB / 16.00GiB (17%)
                                 CPU Usage: 7%
                                 Battery: 40%
                                 Song: The High Society - The Night Elben Kingdom - Feylight
                                 Local IP: 192.168.1.14
                                 Public IP: 2001:4479:2e02:3900:99fa:3eea:e635:1759
```