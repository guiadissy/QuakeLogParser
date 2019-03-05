import copy

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
    elif action == 'Item':
        item()
    elif action == 'Kill':
        score_kill(action_info)
    elif action == 'Exit':
        exit_action()
    elif action == 'ClientConnect':
        client_connect()
    elif action == 'ClientUserinfoChanged':
        userinfo_changed(action_info)
    elif action == 'ClientBegin':
        client_begin()
    elif action == 'ClientDisconnect':
        client_disconnect()


def init_game():
    global current_game
    global games_list
    global base_dict
    new_dict = copy.deepcopy(base_dict)
    games_list.append(new_dict)


def shutdown_game():
    global current_game
    global active_players
    active_players.clear()
    current_game += 1


def score_kill(kill_info):
    # print(kill_info)
    print()


def exit_action():
    print()


def client_connect():
    print()


def userinfo_changed(userinfo):
    user_split_info = userinfo.split('\\')
    user_number = user_split_info[0].split(' ')[0]
    global current_game
    global games_list
    global active_players
    # Position 1 from user_split_info is the user name
    if not (user_number in active_players.keys()):
        games_list[current_game]['players'].append(user_split_info[1])
        active_players[user_number] = user_split_info[1]
    elif active_players[user_number] is None:
        games_list[current_game]['players'].append(user_split_info[1])
        active_players[user_number] = user_split_info[1]


def client_begin():
    print()


def client_disconnect():
    print()


def item():
    print()


f = open('qgames.log', 'r')

current_game = 0
games_list = []
base_dict = {
    "total_kills": 0,
    "players": [],
    "kills": {}
}
active_players = {}

for line in f:
    # print(line)
    log_splitter(line)

print(games_list)

