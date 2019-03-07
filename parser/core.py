import copy
import json


class Parser:
    # Initializing strings used along the code
    TOTAL_KILLS = 'total_kills'
    PLAYERS = 'players'
    KILLS = 'kills'
    KILLS_BY_MEANS = 'kills_by_means'
    TOP_PLAYERS = 'top_player'

    # Initializing global variables
    game_json = {}
    current_game = 0
    game_info = {}
    # kills has to be a list in order to accept players with the same name
    base_dict = {
        TOTAL_KILLS: 0,
        PLAYERS: [],
        KILLS: [],
        KILLS_BY_MEANS: {}
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

    def log_splitter(self, log):
        time_position = log.find(':') + 3
        # time = log[:time_position]
        content = log[time_position:]
        action_position = content.find(':')

        # This '1:' excludes the white space before the action name
        action = content[1:action_position]

        # The '+ 2' excludes the ':' and the white space before the action info
        action_info = content[action_position + 2:]

        if action == 'InitGame':
            self.init_game()
        elif action == 'ShutdownGame':
            self.shutdown_game()
        elif action == 'Kill':
            self.score_kill(action_info)
        elif action == 'ClientUserinfoChanged':
            self.userinfo_changed(action_info)
        elif action == 'ClientDisconnect':
            self.client_disconnect(action_info)

    def init_game(self):
        new_dict = copy.deepcopy(self.base_dict)
        self.game_info.clear()
        self.game_info = new_dict

    def shutdown_game(self):
        for key in self.active_players:
            aux = {self.active_players[key][0]: self.active_players[key][1]}
            self.game_info[self.KILLS].append(aux)

        self.active_players.clear()
        self.current_game += 1
        self.print_game()

    def score_kill(self, kill_info):
        global active_players, current_game, game_info, death_causes

        raw_info = kill_info.split(':')[0].split(' ')
        # raw_info has the number of the user that score the kill,
        # the number of the player killed and the number of how he died
        killer = raw_info[0]
        killed = raw_info[1]
        cause_of_death = raw_info[2]

        # World kill
        if int(killer) == 1022:
            self.active_players[killed][1] -= 1
        # Player kill
        else:
            self.active_players[killer][1] += 1

        self.game_info[self.TOTAL_KILLS] += 1
        index = int(cause_of_death)
        for key in self.death_causes[index]:
            self.death_causes[index][key] += 1

    def userinfo_changed(self, userinfo):
        user_split_info = userinfo.split('\\')
        user_number = user_split_info[0].split(' ')[0]

        # Position 1 from user_split_info is the user name
        if (not (user_number in self.active_players.keys())) or (self.active_players[user_number] is None):
            self.game_info[self.PLAYERS].append(user_split_info[1])
            self.active_players[user_number] = [user_split_info[1], 0]

    def client_disconnect(self, userinfo):
        key = userinfo.split('\n')[0]
        disconnected_user = self.active_players.pop(key, None)

        if disconnected_user is not None:
            aux = {disconnected_user[0]: disconnected_user[1]}
            self.game_info[self.KILLS].append(aux)

    def print_game(self):
        top_player_name = None
        top_kills = 0

        # This loop gets the top player of the match
        for player_kills in self.game_info[self.KILLS]:
            for key in player_kills:
                if (player_kills[key] > top_kills) or (top_player_name is None):
                    top_kills = player_kills[key]
                    top_player_name = key
                elif player_kills[key] == top_kills:
                    aux = top_player_name
                    top_player_name = [aux, key]

        # This loop gets the number of deaths by cause, also cleans the array death_causes for next game
        for kills_means in self.death_causes:
            for key in kills_means:
                if kills_means[key] > 0:
                    self.game_info[self.KILLS_BY_MEANS][key] = kills_means[key]
                    kills_means[key] = 0

        game_name = 'game-' + str(self.current_game)
        self.game_json[game_name] = copy.deepcopy(self.game_info)
        self.game_json[game_name][self.TOP_PLAYERS] = top_player_name


if __name__ == "__main__":
    output_file = 'data.json'
    input_file = 'qgames.log'

    # This clear the output file
    open(output_file, 'w').close()

    parser = Parser()

    # Reads the log
    f = open(input_file, 'r')
    for line in f:
        parser.log_splitter(line)
    f.close()

    # Puts the output on a .json file
    with open(output_file, 'a+') as outfile:
        json.dump(Parser.game_json, outfile)

