# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part B: Game Playing Agent

from __future__ import annotations
import math #Are we allowed to do that?
import numpy as np

from referee.game import PlayerColor, Coord, Direction, \
    Action, PlaceAction, MoveAction, EatAction, CascadeAction, CellState, BOARD_N
"""
Import ApplyActions - Chris
PlaceAction - Chris
placing logic (towards centre)
__init__
action (minimax decision)
minimax value (max calls min)
update - Dan
cutoff/terminal (depth or terminal state)
utility
"""


# Node class (modified from part A)
class Node:
    def __init__(self, state: dict[Coord, CellState], parent: Node, action: Action, height: int, next_turn_color: PlayerColor):
        self.state = state
        self.parent = parent
        self.action = action            #last applied action
        self.height = height            #height in tree
        self.next_turn_color = next_turn_color

def apply_action(action, node, player_color):       #apply_action from part A with new Node structure and player_color
    pass                

#imported from part A, modified for color
def is_valid_move(action, node, player_color, opponent_color) -> bool:
    if action.direction == Direction.Down:
        if action.coord.r >= 7:
            return False
        if (action.coord + Direction.Down) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Down)
            if move_to_cellstate.color == opponent_color:
                return False
    elif action.direction == Direction.Up:
        if action.coord.r <= 0:
            return False
        if (action.coord + Direction.Up) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Up)
            if move_to_cellstate.color == opponent_color:
                return False
    elif action.direction == Direction.Left:
        if action.coord.c <= 0:
            return False
        if (action.coord + Direction.Left) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Left)
            if move_to_cellstate.color == opponent_color:
                return False
    if action.direction == Direction.Right:
        if action.coord.c >= 7:
            return False
        if (action.coord + Direction.Right) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Right)
            if move_to_cellstate.color == opponent_color:
                return False
    return True

def is_valid_eat(action, node, player_color, opponent_color) -> bool: 
    if action.direction == Direction.Down:
        if action.coord.r >= 7:
            return False
        if (action.coord + Direction.Down) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Down)
        if move_to_cellstate.color == player_color:
            return False
        if move_to_cellstate.color == opponent_color and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Up:
        if action.coord.r <= 0:
            return False
        if (action.coord + Direction.Up) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Up)
        if move_to_cellstate.color == player_color:
            return False
        if move_to_cellstate.color == opponent_color and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Left:
        if action.coord.c <= 0:
            return False
        if (action.coord + Direction.Left) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Left)
        if move_to_cellstate.color == player_color:
            return False
        if move_to_cellstate.color == opponent_color and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Right:
        if action.coord.c >= 7:
            return False
        if (action.coord + Direction.Right) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Right)
        if move_to_cellstate.color == player_color:
            return False
        if move_to_cellstate.color == opponent_color and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    return True

def is_valid_cascade(action, node, player_color, opponent_color):
    dr = action.direction.r
    dc = action.direction.c
    if node.state.get(action.coord).height >= 2 and \
        0<=action.coord.r+dr<BOARD_N and 0<=action.coord.c+dc<BOARD_N:
        return True
    else:
        return False         

#player_color is color that makes next move
def generate_possible_actions(node, player_color) -> list[Action]:
    opponent_color = PlayerColor.RED
    if player_color == PlayerColor.RED:
        opponent_color = PlayerColor.BLUE
    actions = []
    for coord in node.state.keys():
        if node.state[coord].color == player_color and node.state[coord].height > 0:
            for direction in Direction:
                if is_valid_eat(EatAction(coord, direction), node, player_color, opponent_color):
                    actions.append(EatAction(coord,direction))
                if is_valid_cascade(CascadeAction(coord, direction), node, player_color, opponent_color):
                    actions.append(CascadeAction(coord,direction))
                if is_valid_move(MoveAction(coord, direction), node, player_color, opponent_color):
                    actions.append(MoveAction(coord,direction))
    return actions

def cutoff_test(node):
    no_reds_left = True
    no_blues_left = True
    for cell in node.state.values():
        if cell.color == PlayerColor.BLUE:
            no_blues_left = False
        if cell.color == PlayerColor.RED:
            no_reds_left = False
    if no_blues_left | no_reds_left | node.height > 5:      #True if terminal state or nodes height is bigger than 5 (to be improved)
        return True
    else:
        return False

def utility(node):
    return 0                            #to be implemented

def max_value(node : Node, alpha, beta):
    new_alpha = alpha
    if cutoff_test(node):
        return utility(node)
    for action in generate_possible_actions(node):
        new_node = apply_action(action, node, node.next_turn_color)
        new_alpha = max(new_alpha, min_value(new_node, new_alpha, beta))
        if new_alpha >= beta:
            return beta
    return new_alpha

def min_value(node : Node, alpha, beta):
    new_beta = beta
    if cutoff_test(node):
        return utility(node)
    for action in generate_possible_actions(node):
        new_node = apply_action(action, node, node.next_turn_color)
        new_beta = min(new_beta, max_value(new_node, alpha, new_beta))
        if new_beta >= alpha:
            return alpha
    return new_beta

def minimax_decision(state, color):
    root = Node(state, None, None, 0, color)
    value = {}
    for action in generate_possible_actions(root, color):
        value[action] = min_value(apply_action(root), -math.inf, math.inf)
    return max(value, key=value.get)

class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Cascade game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        self._turn_count = 0
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED (first player)")
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")

        self.state = dict() #Coord: CellState 

    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object.
        """

        # Below we have hardcoded actions to be played depending on whether
        # the agent is playing as BLUE or RED. Obviously this won't work beyond
        # the initial moves of the game, so you should use some game playing
        # technique(s) to determine the best action to take.

        # During placement phase (first 8 turns total, 4 per player)
        if self._turn_count < 4:
            match self._color:
                case PlayerColor.RED:
                    print("Testing: RED is playing a PLACE action")
                    return PlaceAction(Coord(0, self._turn_count))
                case PlayerColor.BLUE:
                    print("Testing: BLUE is playing a PLACE action")
                    return PlaceAction(Coord(7, self._turn_count))

        # During play phase
        return minimax_decision(self.state, self._color)

    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state.
        """
        if color == self._color:
            self._turn_count += 1

        # There are four possible action types: PLACE, MOVE, EAT, and CASCADE.
        # Below we check which type of action was played and print out the
        # details of the action for demonstration purposes. You should replace
        # this with your own logic to update your agent's internal game state.
        match action:
            case PlaceAction(coord):
                print(f"Testing: {color} played PLACE action at {coord}")
                self.state[coord] = CellState(color, 3)

            case MoveAction(coord, direction):
                print(f"Testing: {color} played MOVE action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
                target = action.coord + action.direction

                src_cell = self.state.pop(coord)
                target_cell = self.state.get(target)

                if target_cell:
                    self.state[target] = CellState(color, target_cell.height + src_cell.height)
                else:
                    self.state[target] = CellState(color, src_cell.height)

            case EatAction(coord, direction):
                print(f"Testing: {color} played EAT action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
                curr_cell = self.state.pop(action.coord)
                self.state[action.coord+action.direction] = curr_cell

            case CascadeAction(coord, direction):
                print(f"Testing: {color} played CASCADE action:")
                print(f"  Coord: {coord}")
                print(f"  Direction: {direction}")
                curr_cell = self.state.pop(action.coord)
                shift = curr_cell.height

                line = []   # list of coords in line with cascade direction
                cells = [] # value of cells in line with cascade direction
                r = action.coord.r
                c = action.coord.c
                dr = action.direction.r
                dc = action.direction.c
                while 0 <= r+dr < BOARD_N and 0 <= c+dc < BOARD_N:
                    r += dr
                    c += dc
                    coord = Coord(r, c)
                    line.append(coord)
                    cells.append(self.state.get(coord))
                
                new_cells = []
                count = 0
                for cell in cells:
                    if count < shift and cell is None:
                        count += 1
                    else:
                        # rest of cells will be pushed off edge
                        if len(new_cells) + shift >= len(cells):
                            break
                        new_cells.append(cell)
                new_cells = shift*[1] + new_cells

                for coord, cell in zip(line, new_cells):
                    if isinstance(cell, CellState):
                        self.state[coord] = cell
                    elif cell == 1:
                        self.state[coord] = CellState(PlayerColor.RED, 1)

            case _:
                raise ValueError(f"Unknown action type: {action}")
