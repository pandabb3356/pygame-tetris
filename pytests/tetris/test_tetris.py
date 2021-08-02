from unittest import TestCase, mock

import pygame as pg

import tetris


@mock.patch.object(tetris, "pg")
class TestGame(TestCase):
    def setUp(self) -> None:
        pass

    def _setup_pygame(self, mock_pg):
        self.surface = mock.MagicMock()

        mock_pg.QUIT = pg.QUIT
        mock_pg.KEYUP = pg.KEYUP
        mock_pg.K_ESCAPE = pg.K_ESCAPE

        mock_pg.display.set_mode.return_value = self.surface

    def test_init(self, mock_pg):
        self._setup_pygame(mock_pg)

        game = tetris.Game()

        mock_pg.display.set_mode.assert_called_with(tetris.Game.WIN_SIZE)
        assert game._surface == self.surface

    def test_game_init(self, mock_pg):
        self._setup_pygame(mock_pg)

        game = tetris.Game()

        game.init()

    def test_game_run(self, mock_pg):
        self._setup_pygame(mock_pg)

        game = tetris.Game()

        mock_events = [
            mock.MagicMock(
                type=pg.KEYUP,
                key=pg.K_ESCAPE,
            )
        ]
        mock_pg.event.get.return_value = mock_events

        game.run()

        assert mock_pg.quit.call_count == 1
