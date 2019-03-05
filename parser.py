

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
    elif action == 'Exit':
        exit_action()
    elif action == 'ClientConnect':
        client_connect()
    elif action == 'ClientUserinfoChanged':
        userinfo_changed()
    elif action == 'ClientBegin':
        client_begin()
    elif action == 'ClientDisconnect':
        client_disconnect()


def init_game():
    global current_game
    global games_list
    global base_dict
    games_list.append(base_dict)


def shutdown_game():
    global current_game
    current_game += 1


def score_kill(kill_info):
    print(kill_info)




f = open('qgames.log', 'r')

current_game = 0
games_list = []
base_dict = {
    "total_kills": 0,
    "players": [],
    "kills": {}
}

for line in f:
    # print(line)
    log_splitter(line)

