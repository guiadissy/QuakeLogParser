import unittest
from unittest import mock
from core import Parser


class TestParser(unittest.TestCase):
    def test_log_splitter(self):
        """
        log_splitter should call the correct functions, with the
        correct arguments depending on what is passed by as argument
        """
        test_cases = [
            {
                'path_name': 'init_game',
                'log': '0:00 InitGame: the game has begun',
                'argument': None
            },
            {
                'path_name': 'shutdown_game',
                'log': '78:32 ShutdownGame: game over',
                'argument': None
            },
            {
                'path_name': 'score_kill',
                'log': '89:12 Kill: Somebody died!',
                'argument': 'Somebody died!'
            },
            {
                'path_name': 'userinfo_changed',
                'log': '34:45 ClientUserinfoChanged: Some info has changed',
                'argument': 'Some info has changed'
            },
            {
                'path_name': 'client_disconnect',
                'log': '58:62 ClientDisconnect: Fulano DC',
                'argument': 'Fulano DC'
            },
            {
                'path_name': 'client_begin',
                'log': '58:62 ClientBegin: Fulano begin',
                'argument': 'Fulano begin'
            }
        ]
        parser = Parser()
        for params in test_cases:
            with mock.patch('core.Parser.' + params['path_name']) as mockFunc:
                parser.log_splitter(params['log'])
                if params['argument'] is None:
                    mockFunc.assert_called_with()
                else:
                    mockFunc.assert_called_once_with(params['argument'])

    def test_log_splitter_wrong_log(self):
        """
        log_splitter should not call any other function
        if the received log is not on the correct format or
        if the log does not match any of the predicted logs
        """
        with mock.patch('core.Parser.init_game') as mockFunc1:
            with mock.patch('core.Parser.shutdown_game') as mockFunc2:
                with mock.patch('core.Parser.score_kill') as mockFunc3:
                    with mock.patch('core.Parser.userinfo_changed') as mockFunc4:
                        with mock.patch('core.Parser.client_begin') as mockFunc5:
                            with mock.patch('core.Parser.client_disconnect') as mockFunc6:
                                parser = Parser()
                                parser.log_splitter('blablabla anything')
                                parser.log_splitter('21:32 Item: whatever')

                                mockFunc1.assert_not_called()
                                mockFunc2.assert_not_called()
                                mockFunc3.assert_not_called()
                                mockFunc4.assert_not_called()
                                mockFunc5.assert_not_called()
                                mockFunc6.assert_not_called()

    def test_init_game(self):
        """
        init_game should rest game_info to be equal base_dict
        """
        game_info_mock = {
            'item': 'some item',
            'action': 'a random action'
        }
        base_dict_mock = {
            'word': 'the corresponding word',
            'something': [],
            'anotherThing': {}
        }

        parser = Parser()

        parser.game_info = game_info_mock
        parser.base_dict = base_dict_mock
        parser.init_game()
        assert parser.game_info == base_dict_mock

    def test_shutdown_game(self):
        """
        shutdown_game should put the list active_players on game_info['kills']
        should also clear the list active_players
        should add one to the count of current_game
        should call print_game()
        """
        intersection = [
            {'Fulano': 56},
            {'Deltrano': 1},
            {'Jack': 0}
        ]
        active_players_mock = {
            '2': ['Fulano', 56],
            '6': ['Deltrano', 1],
            '12': ['Jack', 0]
        }
        kills_mock = [
            {'Player1': 3},
            {'Player2': 987}
        ]

        parser = Parser()

        with mock.patch('core.Parser.print_game') as mockFunc:
            parser.active_players = active_players_mock
            parser.game_info['kills'] = kills_mock
            parser.current_game = 11
            parser.shutdown_game()

            assert parser.current_game == 12
            mockFunc.assert_called_once_with()
            self.assertDictEqual(parser.game_info['kills'][2], intersection[0])
            self.assertDictEqual(parser.game_info['kills'][3], intersection[1])
            self.assertDictEqual(parser.game_info['kills'][4], intersection[2])

    def test_score_kill(self):
        """
        score_kill should give points to the player that killed
        should take out one point if the player died from <world>
        should increase the count of total kills
        should increase the kill count of that death cause
        """
        death_causes = [
            {'death_cause': 0},
            {'death_cause': 0},
            {'death_cause': 0}
        ]

        active_players_mock = {
            '2': ['Fulano', 5],
            '6': ['Deltrano', 1],
            '12': ['Jack', 0]
        }

        parser = Parser()
        parser.death_causes = death_causes
        parser.active_players = active_players_mock
        parser.game_info['total_kills'] = 6

        # World kill
        parser.score_kill('1022 2 0: something something')
        assert parser.game_info['total_kills'] == 7
        assert parser.active_players['2'][1] == 4
        assert parser.death_causes[0]['death_cause'] == 1

        # Player kill
        parser.score_kill('6 12 2: something something')
        assert parser.game_info['total_kills'] == 8
        assert parser.active_players['6'][1] == 2
        assert parser.death_causes[2]['death_cause'] == 1

    def test_userinfo_changed(self):
        """
        userinfo_changed should update the list of active players
        """
        active_players_mock = {
            '2': ['Fulano', 5],
            '6': ['Deltrano', 1],
            '12': ['Jack', 0]
        }

        game_info_players = ['Fulano', 'Deltrano', 'Jack']

        parser = Parser()

        parser.active_players = active_players_mock
        parser.game_info['players'] = game_info_players

        parser.userinfo_changed('4 n\\New Player\\whatever')
        assert parser.active_players['4'] == ['New Player', 0]

    def test_client_begin(self):
        """
        client_begin should pass the confirmed active player to the list of players
        """
        active_players_mock = {
            '2': ['New Player', 0],
            '6': ['Deltrano', 1],
            '12': ['Jack', 0]
        }

        game_info_players = ['Fulano', 'Deltrano', 'Jack']

        parser = Parser()

        parser.active_players = active_players_mock
        parser.game_info['players'] = game_info_players

        parser.client_begin('2')
        assert parser.game_info['players'][3] == 'New Player'

    def test_client_disconnect(self):
        """
        client_disconnect should pass the info from active_players to game_info['kills'] from the DC player
        """
        kills_mock = [
            {'Player1': 3},
            {'Player2': 987}
        ]
        active_players_mock = {
            '2': ['New Player', 67],
            '6': ['Deltrano', 1],
            '12': ['Jack', 0]
        }

        parser = Parser()

        parser.game_info['kills'] = kills_mock
        parser.active_players = active_players_mock

        parser.client_disconnect('6')

        if '6' in parser.active_players:
            assert False
        else:
            assert True
        assert parser.game_info['kills'][2] == {'Deltrano': 1}

    def test_print_game(self):
        """
        print_game should get the top player of the match
        should get the deaths by cause
        should dump all the game info into game_json
        """
        game_info_mock = {
            'total_kills': 34,
            'players': ['Fulano', 'Player1', 'Player2'],
            'kills': [
                {'Player1': 3},
                {'Player2': 12},
                {'Fulano': 6}
            ],
            'kills_by_means': {}
        }

        death_causes_mock = [
            {'death_cause0': 6},
            {'death_cause1': 0},
            {'death_cause2': 28}
        ]

        death_causes_base_mock = [
            {'death_cause0': 0},
            {'death_cause1': 0},
            {'death_cause2': 0}
        ]

        cheat_sheet = {
            'total_kills': 34,
            'players': ['Fulano', 'Player1', 'Player2'],
            'kills': [
                {'Player1': 3},
                {'Player2': 12},
                {'Fulano': 6}
            ],
            'kills_by_means': {
                'death_cause0': 6,
                'death_cause2': 28
            },
            'top_player': 'Player2'
        }

        parser = Parser()

        parser.game_info = game_info_mock
        parser.death_causes = death_causes_mock
        parser.current_game = 15

        parser.print_game()

        assert parser.death_causes == death_causes_base_mock
        assert parser.game_json['game-15'] == cheat_sheet

if __name__ == '__main__':
    unittest.main()
