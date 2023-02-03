import numpy as np
from Grid import Grid

def main():
    print("main code running")
    grid = Grid()
    print("print solved grid:")
    print(grid.get_grid(), end="\n\n")
    print("print unsolved grid:")
    print(grid.random_removal())


if __name__ == "__main__":
    main()
    print("Code executed successfully")
