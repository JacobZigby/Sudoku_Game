import numpy as np

#A sudoku grid like object
class Grid:

    #total number of squares in a grid
    TOTAL_SQUARES = 9 * 9
    #avaliable values in a 3 by 3 grid
    VALUES = {1,2,3,4,5,6,7,8,9}

    #constructor method
    def __init__(self):
        #initalize grid
        self.grid = None 
        #generate the grid itself
        self.generator()

    #Function to generate a grid
    def generator(self):
        #will start off by solveing the diagonals first and then generating solutions with backtracking
        
        #initalize grid
        self.grid = np.zeros((9,9), dtype = np.int8)

        #A temporary placeholder for diagonal quads
        temp_quad = list(self.VALUES)

        #create a for loop to populate the diagonals
        for i in range(3):
            #the offset to where the quadrants begin
            offset = i * 3

            #shuffle the last version of temp quad before placing it in the grid
            np.random.shuffle(temp_quad)
            self.grid[offset : 3 + offset, offset : 3 + offset] = np.reshape(temp_quad, (3,3))

        #call the filler function
        self.fill_grid(0,3)
        

    #Create a recursive backtracking method to fill in the grid
    def fill_grid(self, row, col):
        #base case/ending scenario
        if col == 9:
            #end of column has been reached, readjusting values
            col = 0
            row += 1
            if row == 9:
                #all squares have been filled, thus end the cycle
                return True

        #skip already filled in squares
        if self.grid[row, col] != 0:
            return self.fill_grid(row, col + 1)

        #put all available values into a list to chose from
        bag_of_values = self.avaliable_values(row, col)
        np.random.shuffle(bag_of_values)
        #fill in missing value using only valid values
        for value in bag_of_values:
            self.grid[row,col] = value
            if self.fill_grid(row, col+1):
                return True
            #if current iterations did not work, reset value
            self.grid[row, col] = 0
        #return false as no value was found
        return False


    #check for all avaliable values for a location
    def avaliable_values(self, row, col):
        #remove values found on the selected row
        values = self.VALUES - set(self.grid[row])
        #remove values found on selected column
        values = values - set(self.grid[:,col])

        #identify the quad
        col_quad = col // 3
        row_quad = row // 3
        
        #create a set to easily remo
        quad_set = set(self.grid[row_quad*3:(row_quad+1)*3, col_quad*3:(col_quad+1)*3].flatten())
        values = values - quad_set

        return list(values)

    #Check to see if a hypothetical value can fit into a given grid at selected location
    def is_valid(grid, row:int, col:int, value:int):
        #check to see if new value already exists in row
        if value in grid[row]:
            #if value exists return false
            print(f"Value {value} exists on row: {row}")
            return False
        
        #check to see if new value already exists in col
        if value in grid[:,col]:
            #if value exists return false
            print(f"Value {value} exists on col: {col}")
            return False

        #identify current quad by getting the floor division of current coordinates
        col_quad = col // 3
        row_quad = row // 3
        
        #create a list to easily check if value exists inside
        quad_list = grid[row_quad*3:(row_quad+1)*3, col_quad*3:(col_quad+1)*3].flatten()

        #check if the value exists inside the quad
        if value in quad_list:
            print(f"Value {value} exists in quad {(col_quad,row_quad)}")
            return False
        
        #if none of the conditions passed, return true as value does not exist yet
        return True

    #Check to see if a given value matches with the one found on the grid
    def is_match(self, row:int, col:int, value:int):
        if self.grid[row,col] == value:
            return True
        
        return False

    #method to remove values from valid sudoku grids, returns a new grid
    def random_removal(self, remove_num = 0):
        #create a copy of the grid as to not overwrite the original
        new_grid = self.grid.copy()
        
        #Check to see if remove_num contains a valid number, if not randomly assign one
        if(not remove_num or remove_num > self.TOTAL_SQUARES-17):
            #through a quick search we see that the minumue number of given squares that are needed to solve a sudoku is 17
            remove_num = np.random.randint(20,self.TOTAL_SQUARES-16)

        #create a 2d array to multiply ontop of the grid
        mask_array = ([0] * remove_num) + ([1] * (self.TOTAL_SQUARES-remove_num))

        np.random.shuffle(mask_array)
        mask_array = np.resize(mask_array, (9,9))

        return new_grid * mask_array

    #basic get function
    def get_grid(self):
        return(self.grid)

    #basic set function
    def set_grid(self, grid):
        self.grid = grid

    #create a set row and col method and an is_solvable method that uses a solve method

    def __eq__(self, grid: object) -> bool:
        pass

    def authenticator(grid, solved = True):
        #the grid should be a 2d array with the shape of 9 by 9
        if type(grid) not in [np.ndarray, list]:
            raise TypeError(f"Recieved: {type(grid)} Expected: (ndarray, List)")

        #change to numpy array and check to make sure size is 9X9
        if type(grid) is list:
            grid = np.array(grid)

        #offsets to be used to determin which quad to check at the specified time
        quad_col_offset = 0
        quad_row_offset = 0

        #Check to see if only one instance of each number exists per column or row
        for i in range(len(grid)):
            row = set(np.bincount(grid[i], minlength=10)[1:])
            col = set(np.bincount(grid[:,i],minlength=10)[1:])
            #if feed an incomplete grid, remove missing values
            if not solved:
                row -= {0}
                col -= {0}
                #add one
                row |= {1}
                col |= {1}

            #checks to see that only one of each possibility exists at a time
            if(row != {1} or col != {1}):
                #print a statement to help locate error locations
                print(f"Invalid value found in row or column: {i}")
                #returns a false testing is the test passes
                return False

            #checking quads
            if(i != 0 and i % 3 == 0):
                quad_col_offset = 0
                quad_row_offset += 1

            #The logical checking of the quad
            quad_set = set(
                #turning it into an array of unique values
                np.bincount(
                    grid[
                        quad_row_offset * 3 : (quad_row_offset + 1) * 3,
                        quad_col_offset * 3 : (quad_col_offset + 1) * 3
                    ].flatten(),
                    minlength=10
                )[1:]
            )

            if not solved:
                #I know, I could reorganize so I only call the if once, but I think it's more readable this way
                quad_set -= {0}
                quad_set |= {1}

            if(quad_set != {1}):
                #print a statment to help locate which quadrant has an error
                print(f"Invalid value found in quad: {i+1}") #plus one for quad identity
                #return a false for when a duplicate is found in a quadrant
                return False
            #quad section here
            #add the extra value for the next itteration
            quad_col_offset += 1

        return True
