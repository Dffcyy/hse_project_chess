import unittest

from chess import check_pawn
from chess import check_king
from chess import check_rook
from chess import check_queen
from chess import check_knight
from chess import check_bishop
from chess import turns



class ChessTest(unittest.TestCase):
    def test_check_pawnW(self):
        self.assertEqual(check_pawn((0, 1), 'white'), [(0, 2), (0, 3)])

    def test_check_pawnB(self):
        self.assertEqual(check_pawn((0, 6), 'black'), [(0, 5), (0, 4)])

    def test_check_knightW(self):
        self.assertEqual(check_knight((1, 0), 'white'), [(2, 2), (0, 2)])

    def test_check_knightB(self):
        self.assertEqual(check_knight((1, 7), 'black'), [(2, 5), (0, 5)])

    def test_check_kingW(self):
        self.assertEqual(check_king((3, 0), 'white'), [])

    def test_check_kingB(self):
        self.assertEqual(check_king((3, 7), 'black'), [])

    def test_check_rookW(self):
        self.assertEqual(check_rook((0, 0), 'white'), [])

    def test_check_rookB(self):
        self.assertEqual(check_rook((0, 7), 'black'), [])

    def test_check_queenW(self):
        self.assertEqual(check_queen((4, 0), 'white'), [])

    def test_check_queenB(self):
        self.assertEqual(check_queen((4, 7), 'black'), [])

    def test_check_bishopW(self):
        self.assertEqual(check_bishop((2, 0), 'white'), [])

    def test_check_bishopB(self):
        self.assertEqual(check_bishop((2, 7), 'black'), [])

    def test_turns(self):
        self.assertEqual(turns((4, 2), (1, 5), 'W', 'queen'), 'Wqueen: D3 - G6')

    def test_turns2(self):
        self.assertEqual(turns((2, 6), (4, 5), 'B', 'knight'), 'Bknight: F7 - D6')





