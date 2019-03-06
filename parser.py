import copy
import json

def log_splitter(log):
    time_position = log.find(':') + 3
    # time = log[:time_position]
    content = log[time_position:]
    action_position = content.find(':')

    # This '1:' excludes the white space before the action name
    action = content[1:action_position]

    # The '+ 2' excludes the ':' and the white space before the action info
    action_info = content[action_position + 2:]

    if action == 'InitGame':
        init_game()
    elif action == 'ShutdownGame':
        shutdown_game()
    elif action == 'Kill':
        score_kill(action_info)
    elif action == 'ClientUserinfoChanged':
        userinfo_changed(action_info)
    elif action == 'ClientDisconnect':
        client_disconnect(action_info)


def init_game():
    global current_game
    global games_list
    global base_dict
    new_dict = copy.deepcopy(base_dict)
    games_list.append(new_dict)


def shutdown_game():
    global current_game
    global games_list
    global active_players

    for key in active_players:
        aux = {active_players[key][0]: active_players[key][1]}
        games_list[current_game]['kills'].append(aux)

    active_players.clear()
    current_game += 1


def score_kill(kill_info):
    global current_game
    global games_list
    global active_players

    raw_info = kill_info.split(':')[0].split(' ')
    # raw_info has the number of the user that score the kill,
    # the number of the player killed and the number of how he died
    killer = raw_info[0]
    killed = raw_info[1]

    # World kill
    if int(killer) == 1022:
        active_players[killed][1] -= 1
    # Player kill
    else:
        active_players[killer][1] += 1
    games_list[current_game]['total_kills'] += 1


def userinfo_changed(userinfo):
    user_split_info = userinfo.split('\\')
    user_number = user_split_info[0].split(' ')[0]
    global current_game
    global games_list
    global active_players
    # Position 1 from user_split_info is the user name
    if (not (user_number in active_players.keys())) or (active_players[user_number] is None):
        games_list[current_game]['players'].append(user_split_info[1])
        active_players[user_number] = [user_split_info[1], 0]


def client_disconnect(userinfo):
    global active_players
    global current_game
    global games_list
    key = userinfo.split('\n')[0]
    disconnected_user = active_players.pop(key, None)
    if disconnected_user is not None:
        aux = {disconnected_user[0]: disconnected_user[1]}
        games_list[current_game]['kills'].append(aux)


f = open('qgames.log', 'r')

current_game = 0
games_list = []
# kills has to be a list in order to accept players with the same name
base_dict = {
    "total_kills": 0,
    "players": [],
    "kills": []
}
active_players = {}

for line in f:
    log_splitter(line)

print(games_list)

