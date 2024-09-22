# Param Gattupalli
# Triple Threat: A basketball tic-tac-toe game inspired by Tiki-Taka-Toe
# Created 09/16/2023
# Last modified: 09/16/2023
import random
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
import ast

app = Flask(__name__)
def get_team_all_time(team_code):
    """returns a set of all players that played for a given team"""
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
    else:#if the request fails
        print(url)
        return set()

def get_image(player_name):
    """Returns an image address for the given player"""
    player_lower = player_name.lower()
    space_index = player_lower.find(' ')
    last_name_first_letter = player_lower[space_index + 1]
    i = 1
    while i < 5:
        url = 'https://basketball-reference.com/players/' + last_name_first_letter + '/' + player_lower[space_index + 1: space_index + 6] + player_lower[:2] + '0' + str(i) + '.html'
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            name = soup.find('h1')
            if name.text.strip().lower() != player_lower: #go to the next page if there is another player with the same name
                i += 1
                continue
            picture = soup.find('img', attrs={'itemscope':'image'})
            if picture is not None:
                image_link = picture['src']
                return image_link
            else:
                i = 5

    # Randomly return Tim Duncan or Kobe Bryant if the player is missing their headshot
    return "https://www.basketball-reference.com/req/202106291/images/headshots/duncati01.jpg" if (random.randint(0,1) == 0) else "https://www.basketball-reference.com/req/202106291/images/headshots/bryanko01.jpg"
# Generates 6 random, non-repeating teams from list of NBA teams
def generate_teams():
    """Returns a list of image addresses for 6 unique teams' logos"""
    team_list = ['ATL', 'BOS', 'NJN', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOH', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
    return_list = []
    index_set = set()
    while len(return_list) < 6:
        rand_index = random.randint(0,29)
        if rand_index not in index_set: #ensure that the index hasn't already been used
            index_set.add(rand_index)
            return_list.append("https://cdn.ssref.net/req/202408212/tlogo/bbr/" + team_list[rand_index] + ".png")
    return return_list

# Determine whether the game is over or not, returns True if game is over
def check_game_status(board):
    """Checks if game is over. Returns the winner if finished, None otherwise."""
    # Check each column & row
    for i in range(3):
        if board[i][0][0] == board[i][1][0] == board[i][2][0] or board[0][i][0] == board[1][i][0] == board[2][i][0]:
            return board[i][i][0]
    # Check the diagonals
    if board[0][0][0] == board[1][1][0] == board[2][2][0] or board[0][2][0] == board[1][1][0] == board[2][0][0]:
        return board[1][1][0]
    return None


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


@app.route('/', methods=['GET', 'POST'])
def game():
    if request.method == "GET": #For the first time
        t_list = generate_teams()
        columns = t_list[:3]
        rows = t_list[3:]

        # Create arrays of players from each team
        col0players = get_team_all_time(columns[0][46:49])
        col1players = get_team_all_time(columns[1][46:49])
        col2players = get_team_all_time(columns[2][46:49])
        column_players = [col0players, col1players, col2players]

        row0players = get_team_all_time(rows[0][46:49])
        row1players = get_team_all_time(rows[1][46:49])
        row2players = get_team_all_time(rows[2][46:49])
        row_players = [row0players, row1players, row2players]

        #create a list of lists that contains correct answers for each square
        players = []
        for row in range(3):
            for col in range(3):
                players.append(list(row_players[row].intersection(column_players[col])))

        del col0players, col1players, col2players, row0players, row1players, row2players, row_players, column_players

        game_data = {
            'columns': columns,
            'rows': rows,
            'answers': [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']],
            'players': players,
            'xturn': True,
            'filled_boxes': [],
            'winner': None
        }

        print(game_data)
        return render_template('game.html', game_data=game_data)
    else: #name was submitted
        box = int(request.form['box'])
        player = request.form['player'].upper().strip()
        row, col = get_indices(box)

        #retrieve the game state from the form
        game_data = {
            'columns': ast.literal_eval(request.form.getlist('columns')[0]),
            'rows': ast.literal_eval(request.form.getlist('rows')[0]),
            'answers': ast.literal_eval(request.form.getlist('answers')[0]),
            'players': ast.literal_eval(request.form.getlist('players')[0]),
            'xturn': request.form.get('xturn'),
            'filled_boxes': ast.literal_eval(request.form.getlist('filled_boxes')[0]),
            'winner': request.form.get('winner')
        }

        #handle the user's guess for the given box
        if box not in game_data['filled_boxes']:
            if player in game_data['players'][box - 1]:
                game_data['answers'][row][col] = 'X' if game_data['xturn'] == 'True' else 'O'
                game_data['answers'][row][col] += get_image(player)
                game_data['filled_boxes'].append(box)

                #check if the game is over or not
                winner = check_game_status(game_data['answers'])
                if winner:
                    game_data['winner'] = winner
                elif len(game_data['filled_boxes']) >= 9:
                    game_data['winner'] = 'Draw'
            #change turns
            game_data['xturn'] = 'False' if game_data['xturn'] == 'True' else 'True'


        print(game_data)
        return render_template('game.html', game_data=game_data)




if __name__ == '__main__':
    app.run(debug=True)
