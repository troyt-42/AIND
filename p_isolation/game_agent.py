"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import math

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def score_heuristic_1(game, player):
    # This heuristic expand the legal moves to one level further
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = game.get_legal_moves(player)
    own_moves_num = len(own_moves)
    for move in own_moves:
        own_moves_num += len(game.forecast_move(move).get_legal_moves(player))

    opp = game.get_opponent(player)
    opp_moves = game.get_legal_moves()
    opp_moves_num = len(opp_moves)
    for move in opp_moves:
        opp_moves_num += len(game.forecast_move(move).get_legal_moves(opp))

    return float(own_moves_num - opp_moves_num)

def score_heuristic_2(game, player):
    # This heuristic tries to stick to the center of the board while pushing
    # the opponent away from the center
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp = game.get_opponent(player)

    player_location = game.get_player_location(player)
    opp_location = game.get_player_location(opp)

    player_distance_to_center = math.sqrt(((player_location[0] - 3) ** 2 + (player_location[1] - 3) ** 2))
    opp_distance_to_center = math.sqrt(((opp_location[0] - 3) ** 2 + (opp_location[1] - 3) ** 2))

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(opp))

    return own_moves - player_distance_to_center - opp_moves + opp_distance_to_center

def count_helper(blank_p, moves, depth):
    count = 0
    if depth > 0:
        for move in moves:
            if move in blank_p:
                count += 1
                new_blank_p = [x for x in blank_p if x != move]
                if move[0] - 2 >= 0 and move[1] + 1 <= 6:
                    count += count_helper(new_blank_p, (move[0] - 2, move[1] + 1), depth - 1)
                if move[0] - 2 >= 0 and move[1] - 1 >= 0:
                    count += count_helper(new_blank_p, (move[0] - 2, move[1] - 1), depth - 1)
                if move[0] + 2 <= 6 and move[1] + 1 <= 6:
                    count += count_helper(new_blank_p, (move[0] + 2, move[1] + 1), depth - 1)
                if move[0] + 2 <= 6 and move[1] - 1 >= 0:
                    count += count_helper(new_blank_p, (move[0] + 2, move[1] - 1), depth - 1)

                if move[0] - 1 >= 0 and move[1] + 2 <= 6:
                    count += count_helper(new_blank_p, (move[0] - 1, move[1] + 2), depth - 1)
                if move[0] - 1 >= 0 and move[1] - 2 >= 0:
                    count += count_helper(new_blank_p, (move[0] - 1, move[1] - 2), depth - 1)
                if move[0] + 1 <= 6 and move[1] + 2 <= 6:
                    count += count_helper(new_blank_p, (move[0] + 1, move[1] + 2), depth - 1)
                if move[0] + 1 <= 6 and move[1] - 2 >= 0:
                    count += count_helper(new_blank_p, (move[0] + 1, move[1] - 2), depth - 1)
    return count

def score_heuristic_3(game, player):
    # transposition_table = {
    #     (3, 3): [(1,4), (2,5), (1,2), (2,1), (4,1), (5,2), (5,4), (4,5)],
    #
    #     (1, 4): [(0,6), (2,6), (0,2), (2,2), (3,5), (3,3)],
    #     (2, 5): [(0,6), (0,4), (4,6), (4,4), (1,3), (3,3)],
    #     (1, 2): [(0,0), (0,4), (2,4), (2,0), (3,1), (3,3)],
    #     (2, 1): [(0,0), (0,2), (4,0), (4,2), (1,3), (3,3)],
    #     (4, 1): [(6,0), (6,2), (2,0), (2,2), (5,3), (3,3)],
    #     (5, 2): [(6,0), (4,0), (6,4), (4,4), (3,1), (3,3)],
    #     (5, 4): [(6,6), (6,2), (4,6), (4,2), (3,5), (3,3)],
    #     (4, 5): [(6,6), (6,4), (2,6), (2,4), (5,3), (3,3)],
    #
    #     (0, 6): [(1,4), (2,5)],
    #     (0, 4): [(1,6), (1,4), (2,3), (2,5)],
    #     (0, 2): [(1,4), (1,0), (2,1), (2,3)],
    #     (0, 0): [(1,2), (2,2)],
    #     (2, 0): [(1,2), (3,2), (4,1), (0,1)],
    #     (4, 0): [(3,2), (5,2), (6,1), (2,1)],
    #     (6, 0): [(4,1), (5,2)],
    #     (6, 2): [(4,1), (4,3), (5,4), (5,0)],
    #     (6, 4): [(4,3), (4,5), (5,6), (5,2)],
    #     (6, 6): [(5,4), (4,5)],
    #     (4, 6): [(6,5), (2,5), (5,4), (3,4)],
    #     (2, 6): [(4,5), (0,5), (3,4), (1,4)],
    #
    # }
    opp = game.get_opponent(player)

    own_legal_moves = game.get_legal_moves(player)
    opp_legal_moves = game.get_legal_moves(opp)
    blank_p = game.get_blank_spaces()
    return count_helper(blank_p, own_legal_moves, 3) - count_helper(blank_p, opp_legal_moves, 3)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    ----------
    float
        The heuristic value of the current game state to the specified player.
    """
    return score_heuristic_3(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10., is_student=False):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.num_moves = 0
        self.is_student = is_student
        # self.reflection = {
        #     (0, 6): (6, 0),
        #     (1, 5): (5, 1),
        #     (2, 4): (4, 2),
        #     (0, 0): (6, 6),
        #     (1, 1): (5, 5),
        #     (2, 2): (4, 4),
        #     (0, 3): (6, 3),
        #     (1, 3): (5, 3),
        #     (2, 3): (4, 3),
        #     (3, 0): (3, 6),
        #     (3, 1): (3, 5),
        #     (3, 2): (3, 4)
        # }
    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        ----------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        best_score = float("-inf")
        best_move = (-1, -1)
        if len(legal_moves) == 0: return best_move
        if (self.is_student):
            # Always try to occupy the center position
            if (3,3) in legal_moves: return (3,3)
        # self.num_moves += 1
        # if (self.is_student and self.num_moves < 4):
        #     # Always try to occupy the center position
        #     if (game.move_is_legal((3,3))): return (3,3)
        #     # Try to move the reflection position
        #     opponent_p = game.get_player_location(game.inactive_player)
        #     if opponent_p in self.reflection.keys() and game.move_is_legal(self.reflection[opponent_p]): return self.reflection[opponent_p]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                d = 1
                while True:
                    if self.method == "minimax":
                        v, _ = self.minimax(game, d)
                    if self.method == "alphabeta":
                        v, _ = self.alphabeta(game, d)
                    if (v > best_score):
                        best_score = v
                        best_move = _
                    d += 1
            elif not self.iterative:
                if self.method == "minimax":
                    best_score, best_move = self.minimax(game, self.search_depth)
                if self.method == "alphabeta":
                    best_score, best_move = self.alphabeta(game, self.search_depth)
            return best_move
        except Timeout:
            # Handle any actions required at timeout, if necessary
            return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)
        visited_p = []
        if depth > 0:
            for legal_move in game.get_legal_moves():
                # Generate the new board state with the legal_move applied
                new_state = game.forecast_move(legal_move)
                v, _ = self.minimax(new_state, depth - 1, not maximizing_player)
                if ((maximizing_player and v > best_score) or
                   ((not maximizing_player) and v < best_score)):
                    best_score = v
                    best_move = legal_move
        elif depth == 0:
            # reached leaf, return score value;
            best_score = self.score(game, game.inactive_player if not maximizing_player else game.active_player)
        return best_score, best_move

    def find_symmetry(self, game, current_move, visited_p):
        blank_p = game.get_blank_spaces()

        h_flip = [(move[0], 3 + (3 - move[1])) for move in blank_p]
        if (h_flip == blank_p):
            if (current_move[0], 3 + (3 - current_move[1])) in visited_p:
                return True

        v_flip = [(3 + (3 - move[0]), move[1]) for move in blank_p]
        if (v_flip == blank_p):
            if (3 + (3 - current_move[0]), current_move[1]) in visited_p:
                return True

        d_flip_1 = [(move[1], move[0]) for move in blank_p]
        if (d_flip_1 == blank_p):
            if (current_move[1], current_move[0]) in visited_p:
                return True

        d_flip_2 = [(6 - move[1], 6 - move[0]) for move in blank_p]
        if (d_flip_2 == blank_p):
            if (6 - current_move[1], 6 - current_move[0]) in visited_p:
                return True

        return False

    def find_rotation(self, game, current_move, visited_p):
        blank_p = game.get_blank_spaces()

        rotate_90 = [(move[1], 6 - move[0]) for move in blank_p]
        if (rotate_90 == blank_p):
            if (current_move[1], 6 - current_move[0]) in visited_p:
                return True

        rotate_180 = [(move[1], move[0]) for move in blank_p]
        if (rotate_180 == blank_p):
            if (current_move[1], current_move[0]) in visited_p:
                return True

        rotate_270 = [(6 - move[1], move[0]) for move in blank_p]
        if (rotate_180 == blank_p):
            if (6 - current_move[1], current_move[0]) in visited_p:
                return True

        return False

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        ----------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_score = float("-inf") if maximizing_player else float("inf")
        best_move = (-1, -1)
        visited_p = []

        if depth > 0:
            for legal_move in game.get_legal_moves():
                if self.is_student and len(visited_p) > 0 and depth > 1 and self.num_moves <= 3 and (self.find_symmetry(game, legal_move, visited_p)):
                    visited_p.append(legal_move)
                    continue
                # Generate the new board state with the legal_move applied
                new_state = game.forecast_move(legal_move)
                v, _ = self.alphabeta(new_state, depth - 1, alpha, beta, not maximizing_player)
                if maximizing_player:
                    if v > best_score:
                        best_score = v
                        best_move = legal_move
                    if best_score >= beta:
                        return best_score, best_move
                    if best_score > alpha:
                        alpha = best_score
                elif not maximizing_player:
                    if v < best_score:
                        best_score = v
                        best_move = legal_move
                    if best_score <= alpha:
                        return best_score, best_move
                    if best_score < beta:
                        beta = best_score
                if self.is_student and self.num_moves <= 3:
                    visited_p.append(legal_move)
        elif depth == 0:
            # reached leaf, return score value;
            best_score = self.score(game, game.inactive_player if not maximizing_player else game.active_player)
        return best_score, best_move
