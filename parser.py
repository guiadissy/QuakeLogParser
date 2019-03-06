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
    global game_info
    global base_dict
    new_dict = copy.deepcopy(base_dict)
    game_info.clear()
    game_info = new_dict


def shutdown_game():
    global current_game
    global game_info
    global active_players

    for key in active_players:
        aux = {active_players[key][0]: active_players[key][1]}
        game_info['kills'].append(aux)

    active_players.clear()
    current_game += 1
    print_game()


def score_kill(kill_info):
    global current_game
    global game_info
    global active_players
    global death_causes

    raw_info = kill_info.split(':')[0].split(' ')
    # raw_info has the number of the user that score the kill,
    # the number of the player killed and the number of how he died
    killer = raw_info[0]
    killed = raw_info[1]
    cause_of_death = raw_info[2]

    # World kill
    if int(killer) == 1022:
        active_players[killed][1] -= 1
    # Player kill
    else:
        active_players[killer][1] += 1

    game_info['total_kills'] += 1
    index = int(cause_of_death)
    for key in death_causes[index]:
        death_causes[index][key] += 1


def userinfo_changed(userinfo):
    user_split_info = userinfo.split('\\')
    user_number = user_split_info[0].split(' ')[0]
    global current_game
    global game_info
    global active_players
    # Position 1 from user_split_info is the user name
    if (not (user_number in active_players.keys())) or (active_players[user_number] is None):
        game_info['players'].append(user_split_info[1])
        active_players[user_number] = [user_split_info[1], 0]


def client_disconnect(userinfo):
    global active_players
    global current_game
    global game_info
    key = userinfo.split('\n')[0]
    disconnected_user = active_players.pop(key, None)
    if disconnected_user is not None:
        aux = {disconnected_user[0]: disconnected_user[1]}
        game_info['kills'].append(aux)


def print_game():
    global current_game
    global game_info
    global game_json
    global death_causes
    top_player = None
    top_kills = 0

    # This loop gets the top player of the match
    for player_kills in game_info['kills']:
        for key in player_kills:
            if (player_kills[key] > top_kills) or (top_player is None):
                top_kills = player_kills[key]
                top_player = key
            elif player_kills[key] == top_kills:
                aux = top_player
                top_player = [aux, key]

    # This loop gets the number of deaths by cause, also cleans the array death_causes for next game
    for kills_by_means in death_causes:
        for key in kills_by_means:
            if kills_by_means[key] > 0:
                game_info['kills_by_means'][key] = kills_by_means[key]
                kills_by_means[key] = 0

    game_name = 'game-' + str(current_game)
    game_json[game_name] = copy.deepcopy(game_info)
    game_json[game_name]['top_player'] = top_player


# Initializing global variables
game_json = {}
current_game = 0
game_info = {
    "total_kills": 0,
    "players": [],
    "kills": [],
    "kills_by_means": {}
}
# kills has to be a list in order to accept players with the same name
base_dict = {
    "total_kills": 0,
    "players": [],
    "kills": [],
    "kills_by_means": {}
}
active_players = {}
death_causes = [
    {'MOD_UNKNOWN': 0},
    {'MOD_SHOTGUN': 0},
    {'MOD_GAUNTLET': 0},
    {'MOD_MACHINEGUN': 0},
    {'MOD_GRENADE': 0},
    {'MOD_GRENADE_SPLASH': 0},
    {'MOD_ROCKET': 0},
    {'MOD_ROCKET_SPLASH': 0},
    {'MOD_PLASMA': 0},
    {'MOD_PLASMA_SPLASH': 0},
    {'MOD_RAILGUN': 0},
    {'MOD_LIGHTNING': 0},
    {'MOD_BFG': 0},
    {'MOD_BFG_SPLASH': 0},
    {'MOD_WATER': 0},
    {'MOD_SLIME': 0},
    {'MOD_LAVA': 0},
    {'MOD_CRUSH': 0},
    {'MOD_TELEFRAG': 0},
    {'MOD_FALLING': 0},
    {'MOD_SUICIDE': 0},
    {'MOD_TARGET_LASER': 0},
    {'MOD_TRIGGER_HURT': 0},
    {'MOD_NAIL': 0},
    {'MOD_CHAINGUN': 0},
    {'MOD_PROXIMITY_MINE': 0},
    {'MOD_KAMIKAZE': 0},
    {'MOD_JUICED': 0},
    {'MOD_GRAPPLE': 0}
]

# This clear the output file
open('data.json', 'w').close()

# Reads the log
f = open('qgames.log', 'r')
for line in f:
    log_splitter(line)
f.close()

# Puts the output on a .json file
with open('data.json', 'a+') as outfile:
    json.dump(game_json, outfile)

