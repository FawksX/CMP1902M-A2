import random


class Difficulty:
    """Class to represent the difficulty of the game."""

    def __init__(self, mines, rows, columns):
        self.mines = mines
        self.rows = rows
        self.columns = columns


class Board:
    """Class to represent the board."""

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.solution_board = createSolutionBoard(difficulty)
        self.blank_board = createBlankBoard(difficulty)

    def print(self):
        self.printBoard(self.blank_board)

    def printDebug(self):
        self.printBoard(self.solution_board)

    def printBoard(self, board):
        """Print the board."""
        for row in self.blank_board:
            self.__printSpacer()
            for cell in row:
                print('| ' + cell, end=' ')
            print("|", end=' ')
            print(" ")
        self.__printSpacer()
        print("\n")



    def __printSpacer(self):
        print("-" * (board.difficulty.columns * 4 + 1))

    def check(self, row, column):
        """Check the board."""
        if self.solution_board[row][column] == '*':
            print("You hit a mine! Game over.")
            return False
        else:
            self.blank_board[row][column] = self.solution_board[row][column]
            return True


def selectDifficulty():
    """Select the difficulty of the game."""
    print("Select the difficulty of the game:")
    print("1. Easy 9x9 (10 mines)")
    print("2. Medium 16x16 (40 mines)")
    print("3. Hard 30x16 (99 mines)")
    difficulty = input("Enter a difficulty: ")
    if difficulty == '1':
        return Difficulty(mines=10, rows=9, columns=9)
    elif difficulty == '2':
        return Difficulty(mines=40, rows=16, columns=16)
    elif difficulty == '3':
        return Difficulty(mines=99, rows=16, columns=30)
    else:
        print("Invalid input.")
        return selectDifficulty()


def createSolutionBoard(difficulty):
    """Create the board."""
    mines_placed = 0
    board = []
    for row in range(difficulty.rows):
        board.append([])
        for column in range(difficulty.columns):
            board[row].append('.')
    while mines_placed < difficulty.mines:
        row = random.randint(0, difficulty.rows - 1)
        column = random.randint(0, difficulty.columns - 1)
        if board[row][column] == '.':
            board[row][column] = '*'
            mines_placed += 1
    return board

def addCues(board):
    """Add the cues to the board."""
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == '.':
                board[row][column] = str(countMines(board, row, column))
    return board

def countMines(board, row, column):
    """Count the mines."""
    mines = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < len(board) and column + j >= 0 and column + j < len(board[row]):
                if board[row + i][column + j] == '*':
                    mines += 1
    return mines

def createBlankBoard(difficulty):
    """Create the blank board."""
    board = []
    for row in range(difficulty.rows):
        board.append([])
        for column in range(difficulty.columns):
            board[row].append('.')
    return board


def saveToCsv(board):
    """Save the board to a CSV file."""
    with open('board.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(board)



if (__name__ == '__main__'):
    difficulty = selectDifficulty()
    board = Board(difficulty)
    board.print()
