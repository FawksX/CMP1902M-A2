#
# Minesweeper - V1.0
# Author: Oliver Whitehead (26345141)
# Date: 18/12/2022
#

import random
import time


# A Simple Wrapper for Difficulty Information
# As the program is designed to accept any number of mines, rows and columns, this allows for
# future expansion of the project. For our use-case, we have three pre-defined settings which are
# defined in the class `Difficulties`.
class Difficulty:

    def __init__(self, name, mines, rows, columns):
        self.name = name
        self.mines = mines
        self.rows = rows
        self.columns = columns


# A class which holds our pre-defined difficulties. These include:
# Easy: 9x9 board with 10 mines
# Medium: 16x16 board with 40 mines
# Hard: 30x16 board with 99 mines
# Should the criteria of the program change, this class can be easily modified to include new difficulties
# Note: function selectDifficulty will also need to be updated alongside this class.
class Difficulties:
    EASY = Difficulty(name="Easy", mines=10, rows=9, columns=9)
    MEDIUM = Difficulty(name="Medium", mines=40, rows=16, columns=16)
    HARD = Difficulty(name="Hard", mines=99, rows=16, columns=30)


# A holder class to prevent having None values in the initialisation of a variable. It can be True, False or Undefined
class TriState:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value


# A class which holds our three TriState values.
class TriStates:
    TRUE = TriState(True)
    FALSE = TriState(False)
    UNDEFINED = TriState(None)


# A class which holds the data required for the game to run. It includes:
# - The solution board
# - The player board
# - The difficulty
# The name of the player is not included in the board, as this data is processed after the game has finished
# to put it into the player_data file - so this logic remains in main().
# The class also includes methods which allow the player to interact with the board, such as flagging a cell or
# giving hints
class Board:
    wonGame = TriStates.UNDEFINED

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.solution_board = createSolutionBoard(difficulty)
        self.blank_board = createBlankBoard(difficulty)

    # Prints the board which the player sees/interacts with
    def print(self):
        self.printBoard(self.blank_board)

    # Prints the solution board, used for printing if the player has lost, so they can see what they hit
    # and debugging purposes.
    def printSolution(self):
        self.printBoard(self.solution_board)

    # prints one of the boards, this iterates over each row and column and prints the value at that position
    # this also implements spacers between each row and column to create a "grid".
    def printBoard(self, board):
        currentRow = 0
        header = "    "
        for row in range(self.difficulty.columns):
            header += str(row + 1) + "   "
        print(header)
        for row in board:
            currentRow += 1
            self.printSpacer()
            print(currentRow, end=" ")
            for cell in row:
                print('| ' + cell, end=' ')
            print("|", end=' ')
            print(" ")
        self.printSpacer()
        print("\n")

    # Prints a spacer between the rows of the board to create the horizontal lines
    def printSpacer(self):
        print("  " + "—" * (self.difficulty.columns * 4 + 1))

    # This method performs all the checks for each "move" of the player, It checks if the player has won, hit a mine
    # or if neither opens all cells surrounding the selected cell which are not mines and do not have mines in the
    # vicinity (these cells are marked by a a value > 0).
    def check(self, row, column) -> bool:
        game_continues = True
        if self.solution_board[row][column] == '*':
            print("You hit a mine! Game over.")
            game_continues = False
            self.wonGame = TriStates.FALSE
        else:
            self.openAroundRecursively(row, column)
            game_continues = True

        if self.allMinesFound():
            print("You found all the mines! You win!")
            game_continues = False
            self.wonGame = TriStates.TRUE

        return game_continues

    # Checks cells around the cell at the given row and column and opens all until a cell with a clue is opened
    def openAroundRecursively(self, row, column):
        if self.blank_board[row][column] != '.':  # If the cell is already open, do nothing
            return
        self.blank_board[row][column] = self.solution_board[row][column]
        if self.solution_board[row][column] == '0':  # If the cell was >0 no cells should open as they are on a boundary
            self.blank_board[row][column] = self.solution_board[row][column]
            if row > 0:
                self.openAroundRecursively(row - 1, column)
            if row < self.difficulty.rows - 1:
                self.openAroundRecursively(row + 1, column)
            if column > 0:
                self.openAroundRecursively(row, column - 1)
            if column < self.difficulty.columns - 1:
                self.openAroundRecursively(row, column + 1)

    # Randomly give a mine to the player board as a hint, if requested. This is done by randomly selecting cells
    # and re-running the method until one is found.
    def giveMineHint(self):
        row = random.randint(0, self.difficulty.rows - 1)
        column = random.randint(0, self.difficulty.columns - 1)
        if self.solution_board[row][column] == '*' and self.blank_board[row][column] != '*':
            print("We have revealed a mine at " + str(row + 1) + ", " + str(column + 1))
            self.blank_board[row][column] = '*'  # This will not mess up the game as we check for . and not *
        else:
            self.giveMineHint()

    # Checks if all mines are found by ensuring all cells are opened which are not mines
    def allMinesFound(self) -> bool:
        for row in range(self.difficulty.rows):
            for column in range(self.difficulty.columns):
                # If it is not a mine and is still marked by a ., then the game is not over. We won't require
                # all mines to be flagged to win.
                if self.solution_board[row][column] != '*' and self.blank_board[row][column] == '.':
                    return False
        return True

    # Simply toggles the flag on a cell, if it is already flagged, it is unflagged and vice-versa
    def flag(self, row, column):
        if self.blank_board[row][column] == 'F':
            self.blank_board[row][column] = '.'
        else:
            self.blank_board[row][column] = 'F'

    # Finds out how many mines have not been flagged by the player to provide a counter on the inputLoop
    def countUnflaggedMines(self):
        count = 0
        for row in range(self.difficulty.rows):
            for column in range(self.difficulty.columns):
                if self.solution_board[row][column] == '*' and self.blank_board[row][column] == '.':
                    count += 1
        return count


# This method creates a loop which asks the player for the difficulty they want to play with. Once a valid input
# is given, the difficulty from the Difficulties class is returned.
def selectDifficulty() -> Difficulty:
    print("Select the difficulty of the game:")
    print("1. Easy 9x9 (10 mines)")
    print("2. Medium 16x16 (40 mines)")
    print("3. Hard 30x16 (99 mines)")
    difficulty = input("Enter a difficulty: ")
    if difficulty == '1':
        return Difficulties.EASY
    elif difficulty == '2':
        return Difficulties.MEDIUM
    elif difficulty == '3':
        return Difficulties.HARD
    else:
        print("Invalid input.")
        return selectDifficulty()


# This method creates a 2D Array and creates a board to the specifications of the difficulty given. This is done
# by randomly placing mines in the array.
# Once the mines have been added, the method addCues is called.
def createSolutionBoard(difficulty) -> list:
    mines_placed = 0
    board = []
    for row in range(difficulty.rows):
        board.append([])
        for column in range(difficulty.columns):
            board[row].append('.')
    while mines_placed < difficulty.mines:
        # Keep choosing random rows and columns to place mines, make sure not to override another mine by accident
        row = random.randint(0, difficulty.rows - 1)
        column = random.randint(0, difficulty.columns - 1)
        if board[row][column] == '.':
            board[row][column] = '*'
            mines_placed += 1
    addCues(board)
    return board


# Adds the numbers to the board - This tells the player how many mines are in the vicinity of the cell. For example, if
# There is a "1" in the cell, this means within the 8 cells surrounding it, there is 1 mine.
def addCues(board) -> list:
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == '.':
                board[row][column] = str(countMines(board, row, column))  # put in how many mines there are
    return board


# Counts how many mines are in the 8 cells surrounding the given cell
def countMines(board, row, column) -> int:
    mines = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < len(board) and 0 <= column + j < len(board[row]):
                if board[row + i][column + j] == '*':
                    mines += 1
    return mines


# This method works similarly to the solution board but instead creates the playing board - which starts completely
# blank and is updated as the player plays the game.
def createBlankBoard(difficulty) -> list:
    board = []
    for row in range(difficulty.rows):
        board.append([])
        for column in range(difficulty.columns):
            board[row].append('.')
    return board


# Gives the player the option to flag a cell, check a cell or unflag a cell.
# It should then ask for x,y coordinates and perform the action on the board.
# We -1 from the coordinates because the board is 0 indexed.
def inputLoop(board):
    while True:
        try:
            board.print()
            print("There is currently " + str(board.countUnflaggedMines()) + " mines left to find.")
            action = input("Enter an action (Flag (F), Open (O), Hint (H)): ")
            if action == 'F':
                row = int(input("Enter a row: "))
                column = int(input("Enter a column: "))
                board.flag(row - 1, column - 1)
            elif action == 'O':
                row = int(input("Enter a row: "))
                column = int(input("Enter a column: "))
                if not board.check(row - 1, column - 1):
                    board.printSolution()
                    break
            elif action == 'H':
                board.giveMineHint()
            else:
                print("Invalid input.")
        except (ValueError, TypeError):
            print("Invalid input.")


# Saves the players name, difficulty and time to win to the player_data.txt file. This is used to create the scoreboard
# later.
def saveDataToFile(name, difficulty, time):
    with open('player_data.txt', 'a') as file:
        file.write(name + ',' + difficulty + ',' + time + '\n')
        file.close()


# Loads the file into a list of strings, which stores the name, difficulty and time taken for each game. The top 10
# players are then printed onto the screen.
def generateLeaderboard(difficulty):
    with open('player_data.txt', 'r') as file:
        player_data = file.readlines()
        filtered = list(filter(lambda x: x.split(',')[1] == difficulty.name, player_data))
        filtered.sort(key=lambda x: int(x.split(",")[2]))
        printLeaderboard(filtered)


# Prints the sorted data from the generateLeaderboard method to the screen. We want to print (max) the top 10 players.
def printLeaderboard(data):
    print("Leaderboard:")
    if len(data) <= 9:  # Prevent index out of bounds
        for i in range(len(data)):
            print(data[i])
    else:
        for i in range(10):
            print(data[i])


# Main method for the program. This provides the initial difficulty logic, creates the board and starts the input loop
# Once the input loop has completed, it will find the time taken to win and save the data to the file and display the
# leaderboard.
def main():
    name = input("Input your name: ")
    difficulty = selectDifficulty()
    board = Board(difficulty)
    start_time = int(round(time.time() * 1000))
    inputLoop(board)
    end_time = int(round(time.time() * 1000))

    if board.wonGame == TriStates.TRUE:
        saveDataToFile(name, difficulty.name, str(end_time - start_time))
    generateLeaderboard(difficulty)


if __name__ == '__main__':
    main()
