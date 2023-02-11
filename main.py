# import numpy as np
from Grid import Grid

def main():
    #Here we'll just test the class to make sure it works correctly
    print("main code running")
    grid1 = Grid()
    print("print solved grid1:")
    print(grid1.get_grid(), end="\n\n")
    print("print unsolved grid1:")
    unsolved1 = grid1.random_removal()
    print(unsolved1, end = "\n\n")

    grid2 = Grid()
    print("print solved grid2:")
    print(grid2.get_grid(), end="\n\n")
    print("print unsolved grid1:")
    unsolved2 = grid2.random_removal()
    print(unsolved2, end = "\n\n")

    print("testing solver")
    print(unsolved1, end="\n\n")
    grid3 = Grid(unsolved1, False)
    print(grid3.get_grid())

if __name__ == "__main__":
    main()
    print("Code executed successfully")
