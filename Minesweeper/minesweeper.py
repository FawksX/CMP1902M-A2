import random
import time


class Difficulty:

    def __init__(self, name, mines, rows, columns):
        self.name = name
        self.mines = mines
        self.rows = rows
        self.columns = columns


class Difficulties:
    EASY = Difficulty(name="Easy", mines=10, rows=9, columns=9)
    MEDIUM = Difficulty(name="Medium", mines=40, rows=16, columns=16)
    HARD = Difficulty(name="Hard", mines=99, rows=16, columns=30)


class Board:

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.solution_board = createSolutionBoard(difficulty)
        self.blank_board = createBlankBoard(difficulty)

    def print(self):
        self.printBoard(self.blank_board)

    def printSolution(self):
        self.printBoard(self.solution_board)

    def printBoard(self, board):
        """Print the board."""
        for row in board:
            self.printSpacer()
            for cell in row:
                print('| ' + cell, end=' ')
            print("|", end=' ')
            print(" ")
        self.printSpacer()
        print("\n")

    def printSpacer(self):
        print("-" * (board.difficulty.columns * 4 + 1))

    def check(self, row, column) -> bool:
        game_continues = True
        if self.solution_board[row][column] == '*':
            print("You hit a mine! Game over.")
            game_continues = False
        else:
            self.openAroundRecursively(row, column)
            game_continues = True

        if self.allMinesFound():
            print("You found all the mines! You win!")
            game_continues = False

        return game_continues

    # Checks cells around the cell at the given row and column and opens all until a cell with a clue is opened
    def openAroundRecursively(self, row, column):
        if self.blank_board[row][column] != '.':
            return
        if self.solution_board[row][column] == '0':
            self.blank_board[row][column] = self.solution_board[row][column]
            if row > 0:
                self.openAroundRecursively(row - 1, column)
            if row < self.difficulty.rows - 1:
                self.openAroundRecursively(row + 1, column)
            if column > 0:
                self.openAroundRecursively(row, column - 1)
            if column < self.difficulty.columns - 1:
                self.openAroundRecursively(row, column + 1)

    # Randomly give a mine to the player board as a hint, if requested
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
                if self.solution_board[row][column] != '*' and self.blank_board[row][column] == '.':
                    return False
        return True

    def flag(self, row, column):
        if self.blank_board[row][column] == 'F':
            self.blank_board[row][column] = '.'
        else:
            self.blank_board[row][column] = 'F'

    def countUnflaggedMines(self):
        count = 0
        for row in range(self.difficulty.rows):
            for column in range(self.difficulty.columns):
                if self.solution_board[row][column] == '*' and self.blank_board[row][column] == '.':
                    count += 1
        return count


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


def createSolutionBoard(difficulty) -> list:
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
    addCues(board)
    return board


def addCues(board) -> list:
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == '.':
                board[row][column] = str(countMines(board, row, column))
    return board


def countMines(board, row, column) -> int:
    mines = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < len(board) and 0 <= column + j < len(board[row]):
                if board[row + i][column + j] == '*':
                    mines += 1
    return mines


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


def printLeaderboard(data):
    print("Leaderboard:")
    if len(data) <= 9:
        for i in range(len(data)):
            print(data[i])
    else:
        for i in range(10):
            print(data[i])


if __name__ == '__main__':
    name = input("Input your name: ")
    difficulty = selectDifficulty()
    board = Board(difficulty)
    board.printSolution()
    start_time = int(round(time.time() * 1000))
    inputLoop(board)
    end_time = int(round(time.time() * 1000))
    saveDataToFile(name, difficulty.name, str(end_time - start_time))
    generateLeaderboard(difficulty)
