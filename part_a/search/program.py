# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from __future__ import annotations
from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor, BOARD_N
from .utils import render_board
from copy import copy



class Node:
    def __init__(self, state: dict[Coord, CellState], parent: Node, children: list[Node], action: Action):
        self.state = state
        self.parent = parent
        self.children = children
        self.action = action # renamed path to action, thought it was more clear
        #maybe add score and nstacks and stack height

def create_root(init_state: dict[Coord, CellState]) -> Node:
    return Node(init_state, parent=None, children=[], action=None)

def goal_test(board_state: dict) -> bool:
    for cell in board_state.values():
        if cell.color == PlayerColor.BLUE:
            return False
    return True

def apply_action(action, node) -> Node:
    if isinstance(action, MoveAction):
        return apply_move(action, node)
    if isinstance(action, EatAction):
        return apply_eat(action, node)
    if isinstance(action, CascadeAction):
        return apply_cascade(action, node)
    return Node                       #Not sure if this is necessary just a base case type thing for empty action

def apply_move(action: MoveAction, node: Node) -> Node:
    target = action.coord + action.direction

    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    src_cell = new_state.pop(action.coord)
    target_cell = new_state.get[target]

    if target_cell:
        new_state[target] = CellState(PlayerColor.RED, target_cell.height + src_cell.height)
    else:
        new_state[target] = CellState(PlayerColor.RED, src_cell.height)

    new_node = Node(new_state, node, [], action)
    node.children.append(new_node)
    return new_node ## change

def apply_eat(action: EatAction, node: Node) -> Node:
    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    curr_cell = new_state.pop(action.coord)
    new_state[action.coord+action.direction] = curr_cell
    new_node = Node(new_state, node, [], action)
    node.children.append(new_node)
    return new_node

def apply_cascade(action: CascadeAction, node: Node) -> Node:
    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    curr_cell = new_state.pop(action.coord)
    shift = curr_cell.height

    line = []   # list of relevant coords to be shifted
    r = action.coord.r
    c = action.coord.c
    dr = action.direction.r
    dc = action.direction.c
    while 0 <= r+dr < BOARD_N and 0 <= c+dc < BOARD_N-1:
        r += dr
        c += dc
        line.append(Coord(r, c))
        
    #for i, coord in list(enumerate(list, start=0))[::-1]
    for i in range(len(line)-1, -1, -1):
        # Within range of cascade
        if i < shift:
            new_state[line[i]] = CellState(PlayerColor.RED, 1)
        # if something will be pushed to coord
        elif line[i-shift] in node.state:
            new_state[line[i]] = node.state[line[i-shift]]
        # if something needs to be removed
        elif line[i] in node.state:
            del new_state[line[i]]

def is_valid(action, node) -> bool:
    if isinstance(action, MoveAction):
        return is_valid_move(action, node)
    elif isinstance(action, EatAction):
        return is_valid_eat(action, node)
    elif isinstance(action, CascadeAction):
        return is_valid_cascade(action,node)

def is_valid_move(action, node) -> bool:
    if action.direction == Direction.Down:
        if action.coord.r >= 7:
            return False
        if (action.coord + Direction.Down) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Down)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    elif action.direction == Direction.Up:
        if action.coord.r <= 0:
            return False
        if (action.coord + Direction.Up) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Up)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    elif action.direction == Direction.Left:
        if action.coord.c <= 0:
            return False
        if (action.coord + Direction.Left) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Left)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    if action.direction == Direction.Right:
        if action.coord.c >= 7:
            return False
        if (action.coord + Direction.Right) in node.state:
            move_to_cellstate = node.state.get(action.coord + Direction.Right)
            if move_to_cellstate.color == PlayerColor.BLUE:
                return False
    return True

def is_valid_eat(action, node) -> bool: 
    if action.direction == Direction.Down:
        if action.coord.r >= 7:
            return False
        if (action.coord + Direction.Down) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Down)
        if move_to_cellstate.color == PlayerColor.RED:
            return False
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Up:
        if action.coord.r <= 0:
            return False
        if (action.coord + Direction.Up) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Up)
        if move_to_cellstate.color == PlayerColor.RED:
            return False
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Left:
        if action.coord.c <= 0:
            return False
        if (action.coord + Direction.Left) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Left)
        if move_to_cellstate.color == PlayerColor.RED:
            return False
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    if action.direction == Direction.Right:
        if action.coord.c >= 7:
            return False
        if (action.coord + Direction.Right) not in node.state:
            return False
        move_to_cellstate = node.state.get(action.coord + Direction.Right)
        if move_to_cellstate.color == PlayerColor.RED:
            return False
        if move_to_cellstate.color == PlayerColor.BLUE and move_to_cellstate.height > node.state.get(action.coord).height:
            return False
    return True

def is_valid_cascade(action, node):
    if node.state.get(action.coord).height >= 2:
        return True
    else:
        return False      

def get_path(goal: Node) -> list[Action]:
    curr = goal
    path = []
    while curr.parent:
        path.append(curr.action)
        curr = curr.parent
    return reversed(path)

def generate_possible_actions(node) -> list[Action]:
    actions = []
    for coord in node.state.keys():
        if node.state[coord].color == PlayerColor.RED and node.state[coord].height > 0:
            for direction in Direction:
                if is_valid_move(MoveAction(coord, direction), node):
                    actions.append(MoveAction(coord,direction))
                if is_valid_eat(EatAction(coord, direction), node):
                    actions.append(EatAction(coord,direction))
                if is_valid_cascade(CascadeAction(coord, direction), node):
                    actions.append(CascadeAction(coord,direction))
    return actions



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
    queue = [create_root(board)]

    while True: 
        if queue == []:
        # no more possible states
            return None
        # expand next node in queue
        next_node = queue.pop(0)
        if goal_test(next_node.state):
            return next_node
        # create a new node for each valid action applied to next_node
        for action in generate_possible_actions(next_node):
            new_node = apply_action(action, next_node)
            # check if action is valid from current state
            next_node.children.append(new_node)
            queue = queue + [new_node]
            print("For action ", action, " we get:")
            print(render_board(new_node.state, ansi=True))

    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return [
        MoveAction(Coord(3, 3), Direction.Down),
        EatAction(Coord(4, 3), Direction.Down),
    ]
