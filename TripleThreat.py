# Param Gattupalli
# Triple Threat: A basketball tic-tac-toe game inspired by Tiki-Taka-Toe
# Created 09/16/2023
# Last modified: 09/16/2023
import random
import pandas as pd
from tabulate import tabulate

# Generates 6 random, non-repeating teams from list of NBA teams
def generate_teams():
    team_list = ['76ers','Bucks','Bulls','Cavaliers','Celtics','Clippers','Grizzlies','Hawks','Heat','Hornets','Jazz','Kings','Knicks','Lakers','Magic','Mavericks','Nets','Nuggets','Pacers','Pelicans','Pistons','Raptors','Rockets','Spurs','Suns','Thunder','Timberwolves','Trail Blazers','Warriors','Wizards']
    return_list = []
    while len(return_list) < 6:
        rand_index = random.randint(0,29)
        if team_list[rand_index] not in return_list:
            return_list.append(team_list[rand_index])
    return return_list

# Determine whether the game is over or not, returns True if game is over
def check_game_status(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] or board[0][i] == board[1][i] == board[2][i]:
            print(board[i][i], "WINS!")
            return True
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        print(board[1][1], "WINS!")
        return True
    for row in board:
        for cell in row:
            if type(cell) is int:
                print("IT'S A DRAW!")
                return True
    return False

# Get array indices based on selected box
def get_indices(box_number):
    row,col = 0, (box_number + 2) % 3
    # Get row index
    if box_number <= 3:
        row = 0
    elif box_number <= 6:
        row = 1
    elif box_number <=9:
        row = 2
    return row,col


t_list = generate_teams()
columns  = [t_list[0],t_list[1],t_list[2]]
rows = [t_list[3],t_list[4],t_list[5]]
answers = [['1','2','3'],['4','5','6'],['7','8','9']]
end, xturn= False, True

# Create arrays of players from each team
col0players = pd.read_excel('Rosters.xlsx', columns[0], usecols= 'B',index_col=0).index.array
col1players = pd.read_excel('Rosters.xlsx', columns[1], usecols= 'B',index_col=0).index.array
col2players = pd.read_excel('Rosters.xlsx', columns[2], usecols= 'B',index_col=0).index.array
column_players = [col0players,col1players,col2players]

row0players = pd.read_excel('Rosters.xlsx', rows[0], usecols= 'B',index_col=0).index.array
row1players = pd.read_excel('Rosters.xlsx', rows[1], usecols= 'B',index_col=0).index.array
row2players = pd.read_excel('Rosters.xlsx', rows[2], usecols= 'B',index_col=0).index.array
row_players = [row0players,row1players,row2players]

def print_board():
    table_headers = ['',columns[0],columns[1],columns[2]]
    table = [[rows[0], answers[0][0],answers[0][1],answers[0][2]], [rows[1],answers[1][0],answers[1][1],answers[1][2]], [rows[2],answers[2][0],answers[2][1],answers[2][2]]]

    print(tabulate(table,headers = table_headers,numalign='center',stralign='center'))


num_players = 0
while not end and num_players < 9:
    # Print current board
    print_board()
    box = input("Which square would you like to fill in? (Enter -999 to exit): ")

    # Check that the selection is valid
    try:
        # Convert to int, raises ValueError if unable to
        box = int(box)
        available_spot = False
        if box == -999:
            break
        # Ensure that box is 1-9
        if not 0 < box < 10:
            raise ValueError
        # Ensure that selected box hasn't been replaced already
        for i in range(3):
            if str(box) in answers[i]:
                available_spot = True
                break
        # Print error and retry if invalid input
        if not available_spot:
            print("That square has already been filled. Try Again!\n")
            continue
    # Print error and retry if invalid input
    except ValueError:
        print('Please enter an integer 1-9.\n')
        continue

    row, col = get_indices(box)
    player = input("Name a player who played for both the " + rows[row] + " and the " + columns[col] + ": ")

    if player.upper() in row_players[row] and player.upper() in column_players[col]:
        if xturn:
            answers[row][col] = 'x'
        else:
            answers[row][col] = 'o'
        print("You got one. Next player's turn.")
        num_players += 1
    else:
        print(player, "did not play for both teams. Next player's turn.")
    xturn = not xturn

    end = check_game_status(answers)

if num_players > 8:
    print("IT'S A DRAW!")
print("GAME OVER!")