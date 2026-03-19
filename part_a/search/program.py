# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from __future__ import annotations
from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor
from .utils import render_board



class Node:
    def __init__(self, state: dict[Coord, CellState], parent: Node, children: list[Node], path: Action):
        self.state = state
        self.parent = parent
        self.children = children
        self.path = path

def create_root(init_state: dict[Coord, CellState]) -> Node:
    return Node(init_state, None, [], None)

def goal_test(board_state: dict) -> bool:
    for cell in dict.values:
        if cell.color == PlayerColor.BLUE:
            return False
    return True

def apply_action(action, node) -> Node:
    pass

def is_valid_move(action, node) -> bool:
    if action.direction == Direction.Down:
        if action.coord.r >= 7:
            return False
        if node.state.get(action.coord + Direction.Down) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Down)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    elif action.direction == Direction.Up:
        if action.coord.r <= 0:
            return False
        if node.state.get(action.coord + Direction.Up) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Up)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    elif action.direction == Direction.Left:
        if action.coord.c <= 0:
            return False
        if node.state.get(action.coord + Direction.Left) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Left)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    if action.direction == Direction.Right:
        if action.coord.c >= 7:
            return False
        if node.state.get(action.coord + Direction.Right) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Right)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    return True

def is_valid_eat(action, node) -> bool: 
    if is_valid_move(MoveAction(action.coord, action.direction), node) is False:
        return False
    if action.direction == Direction.Down:
        if node.state.get(action.coord + Direction.Down) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Down)
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord):
            return False
    if action.direction == Direction.Up:
        if node.state.get(action.coord + Direction.Up) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Up)
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord):
            return False
    if action.direction == Direction.Left:
        if node.state.get(action.coord.add(Direction.Left)) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord.add(Direction.Left))
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord):
            return False
    if action.direction == Direction.Right:
        if node.state.get(action.coord.add(Direction.Right)) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord.add(Direction.Right))
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord):
            return False
    return True

def is_valid_cascade(action, node):
    if node.state.get(action.coord).height >= 2:
        return True
    return False

    
        

def get_path(goal: Node) -> list[Action]:
    pass


def search(
    board: dict[Coord, CellState]
) -> list[Action] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to `CellState` instances (each with a `.color` and
            `.height` attribute).

    Returns:
        A list of actions (MoveAction, EatAction, or CascadeAction), or `None`
        if no solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    print(render_board(board, ansi=True))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...
    root = create_root(board)
    print(is_valid_move(MoveAction(Coord(3, 3), Direction.Down), root))
    print(is_valid_eat(EatAction(Coord(4, 3), Direction.Down), root))

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        MoveAction(Coord(3, 3), Direction.Down),
        EatAction(Coord(4, 3), Direction.Down),
    ]
