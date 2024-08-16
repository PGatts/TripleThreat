# Param Gattupalli
# Triple Threat: A basketball tic-tac-toe game inspired by Tiki-Taka-Toe
# Created 09/16/2023
# Last modified: 09/16/2023
import random
import pandas as pd
from tabulate import tabulate
import requests
from bs4 import BeautifulSoup

def get_team_all_time(team_code): #returns a set of all players that played for a given team
    url="https://www.basketball-reference.com/teams/" + team_code + "/players.html"
    page= requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('table', attrs={'id':'franchise_register'})
        rows = table.find_all('tr')
        rows = rows[2:] #remove the first 2 header rows

        player_list = set()
        for row in rows:
            cols = row.find_all(['th','td'])#get all elements in row
            if cols[0].text.strip().isdigit():#skips rows that aren't players
                player_list.add(cols[1].text.strip().upper())
        return player_list
    else:
        return set()

# Generates 6 random, non-repeating teams from list of NBA teams
def generate_teams():
    """Returns a list of 6 unique teams"""
    team_list = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    return_list = []
    while len(return_list) < 6:
        rand_index = random.randint(0,29)
        if team_list[rand_index] not in return_list:
            return_list.append(team_list[rand_index])
    return return_list

# Determine whether the game is over or not, returns True if game is over
def check_game_status(board):
    """Checks if game is over. Returns True if finished, False otherwise."""
    # Check each column & row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] or board[0][i] == board[1][i] == board[2][i]:
            print(board[i][i], "WINS!")
            return True
    # Check the diagonals
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        print(board[1][1], "WINS!")
        return True
    return False

# Get array indices based on selected box
def get_indices(box_number):
    """Returns a tuple of indices based on selected box number."""
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
end, xturn = False, True

# Create arrays of players from each team
col0players= get_team_all_time(columns[0])
col1players= get_team_all_time(columns[1])
col2players= get_team_all_time(columns[2])
column_players = [col0players,col1players,col2players]

row0players= get_team_all_time(rows[0])
row1players= get_team_all_time(rows[1])
row2players= get_team_all_time(rows[2])
row_players = [row0players,row1players,row2players]

players = []
for row in range(3):
    for col in range(3):
        players.append(row_players[row].intersection(column_players[col]))

del col0players, col1players, col2players, row0players, row1players, row2players, column_players, row_players

def print_board():
    table_headers = ['',columns[0],columns[1],columns[2]]
    table = [[rows[0], answers[0][0],answers[0][1],answers[0][2]], [rows[1],answers[1][0],answers[1][1],answers[1][2]], [rows[2],answers[2][0],answers[2][1],answers[2][2]]]

    print(tabulate(table,headers = table_headers,numalign='center',stralign='center'))



filled_boxes = set()
while not end and len(filled_boxes) < 9:
    # Print current board
    print_board()
    box = input("Which square would you like to fill in? (Enter -999 to exit): ")

    # Check that the selection is valid
    try:
        # Convert to int, raises ValueError if unable to
        box = int(box)
        available_spot = True
        if box == -999:
            break
        # Ensure that box is 1-9
        if not 0 < box < 10:
            raise ValueError
        # Ensure that selected box hasn't been replaced already
        if box in filled_boxes:
            available_spot = False
        # Print error and retry if invalid input
        if not available_spot:
            print("That square has already been filled. Try Again!\n")
            continue
    # Print error and retry if invalid input
    except ValueError:
        print('Please enter an integer 1-9.\n')
        continue

    row, col = get_indices(box)
    player = input("Name a player who played for both " + rows[row] + " and " + columns[col] + ": ")

    #check if valid answer
    if player.upper() in players[box - 1]:
        if xturn:
            answers[row][col] = 'x'
        else:
            answers[row][col] = 'o'
        print("You got one. Next player's turn.")
        filled_boxes.add(box)
    else:
        print(player.capitalize(), "did not play for both teams. Next player's turn.")

    #change player turn after guess
    xturn = not xturn
    end = check_game_status(answers)

if len(filled_boxes) > 8:
    print("IT'S A DRAW!")
print("GAME OVER!")