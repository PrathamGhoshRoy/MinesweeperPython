# Objective: To create the minesweeper game for everyone to have some fun!

import random
import re

# Let us FIRST create a board object to represent the minesweeper game.
# This is so that we can just say "Create a new board object", or 
# "dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        # Keeping track of these parameters:
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Now we can create the board
        # Helper function:
        self.board = self.make_new_board() # Plant the bombs
        self.assign_values_to_board()

        # Initialize a set to keep track of which locations we've uncovered.
        # We'll save (row, col) tuples into this set.
        self.dug = set()


    def assign_values_to_board(self):
        # Now that we have the bombs planted, lets assign a number 0-8 for all the empty spaces.
        # which represents how many neighbouring bombs there are. We can precompute those and it'll
        # save us some effort checking what's around the board later on.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)

    def get_num_neighbouring_bombs(self, row, col):
        # Let's iterate through each of the neighbouring positions and sum number of bombs
        # Top left: (row-1, col-1)
        # Top middle: (row-1, col)
        # Top right: (row-1, col+1)
        # Left: (row, col-1)
        # Right: (row, col+1)
        # Bottom left: (row+1, col-1)
        # Bottom middle: (row+1, col)
        # Bottom right: (row+1, col+1)

        # Make sure to not go out of bounds!

        num_neighbouring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col:
                    # Our original location, don't check.
                    continue
                if self.board[r][c] == '*':
                    num_neighbouring_bombs +=1

        return num_neighbouring_bombs


    def make_new_board(self):
        # Construct a new board based on the dim size and num bombs
        # We should construct the list of lists here, since its a 2-D board (a representation)
        

        # Generate a new board (Filling a list with lists of emptiness)
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # This would create an array like this:
        # [[None, None, ...., None],
        # [None, None, ...., None],
        # [None, None, ...., None]]

        # Planting the bombs:
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 -1) # Return a random integer N such taht a <= N <= b
            row = loc // self.dim_size # We want the number of times dim_size goes into loc to tell us
            col = loc % self.dim_size # We want the remainder to tell us what index in that row the location

            if board[row][col] == '*':
                # This means we've actually planted a bomb there already so keep going
                continue

            board[row][col] = '*' # Plant the bomb
            bombs_planted += 1
        
        return board

    def dig(self, row, col):
        # Dig at that location!
        # Return True if successful dig, False if a bomb is dug

        # A few different scenarios:
        # 1. Hit a bomb -> Game over
        # 2. Dig at location with neighbouring bombs -> Finish dig
        # 3. Dig at location with no neighbouring bombs -> recursively dig neighbours!

        self.dug.add((row, col)) # Keeping track of where we have dug

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        # self.board[row][] == 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue # Don't dig where you've already dug
                self.dig(r, c)

        # If our initial dig didn't hit a bomb, we shouldn't hit a bomb here.
        return True
    
    def __str__(self):
        # Use of magic function which prints this object.
        # Return a string that shows the board to the player.
        
        # First lets create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # Put this together in a string
                string_rep = ''
        # Get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # Print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


# Play the game
def play(dim_size=10, num_bombs=10):
    # Step 1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: Show the user the board and ask for where they want to dig
    # Step 3a: If the location is a bomb, show game over message
    # Step 3b: If the location is not a bomb, dig recursively until
    #          until each square is at least next to a bomb
    # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!
    safe = True

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        # 0,0 or 0, 0 or 0,    0
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row, col: ")) # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # If the user input is valid, we dig
        safe = board.dig(row, col)
        if not safe: 
            # We dug a bomb! MAYDAY!
            break # GAME OVER GG WP

    # 2 ways to end loop, lets check which one
    if safe:
        print("CONGRATULATIONS! YOU ARE A POG CHAMP! MVP! CHICKEN DINNER!")
    else:
        print("SORRY, GAME OVER:(((((")
        # Let's reveal the whole board!
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': # Good practise to keep in mind :))
    play()
