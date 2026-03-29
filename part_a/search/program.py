# COMP30024 Artificial Intelligence, Semester 1 2026
# Project Part A: Single Player Cascade

from __future__ import annotations
from .core import CellState, Coord, Direction, Action, MoveAction, EatAction, CascadeAction, PlayerColor, BOARD_N
from .utils import render_board
from copy import copy
import heapq



class Node:
    def __init__(self, state: dict[Coord, CellState], parent: Node, children: list[Node], action: Action, cost: int):
        self.state = state
        self.parent = parent
        self.children = children
        self.action = action
        self.cost = cost # added cost so that we dont have to compute the complete path every time
        #maybe add score and nstacks and stack height

def create_root(init_state: dict[Coord, CellState]) -> Node:
    return Node(init_state, parent=None, children=[], action=None, cost=0)

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
    return None

def apply_move(action: MoveAction, node: Node) -> Node:
    target = action.coord + action.direction

    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    src_cell = new_state.pop(action.coord)
    target_cell = new_state.get(target)

    if target_cell:
        new_state[target] = CellState(PlayerColor.RED, target_cell.height + src_cell.height)
    else:
        new_state[target] = CellState(PlayerColor.RED, src_cell.height)

    new_node = Node(new_state, node, [], action, node.cost + 1)
    node.children.append(new_node)
    return new_node

def apply_eat(action: EatAction, node: Node) -> Node:
    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    curr_cell = new_state.pop(action.coord)
    new_state[action.coord+action.direction] = curr_cell
    new_node = Node(new_state, node, [], action, node.cost + 1)
    node.children.append(new_node)
    return new_node

def apply_cascade(action: CascadeAction, node: Node) -> Node:
    new_state = copy(node.state)    # not sure if need to copy/deepcopy
    curr_cell = new_state.pop(action.coord)
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
        cells.append(node.state.get(coord))
    
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
            new_state[coord] = cell
        elif cell == 1:
            new_state[coord] = CellState(PlayerColor.RED, 1)

    return Node(state=new_state, parent=node, children=[], action=action, cost = node.cost + 1)

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
                if is_valid_eat(EatAction(coord, direction), node):
                    actions.append(EatAction(coord,direction))
                if is_valid_cascade(CascadeAction(coord, direction), node):
                    actions.append(CascadeAction(coord,direction))
                if is_valid_move(MoveAction(coord, direction), node):
                    actions.append(MoveAction(coord,direction))
    return actions


def dist_h(state, blue_coords, red_coords):
    if not blue_coords or not red_coords:
        return 0

    num_reds = sum(state[coord].height for coord in red_coords)

    min_dist = min(abs(r.r - b.r) + abs(r.c - b.c) 
        for r in red_coords 
        for b in blue_coords)
    
    return min_dist / num_reds

def line_h(state, blue_coords, red_coords):
    rows = {b.r for b in blue_coords}
    cols = {b.c for b in blue_coords}

    return min(len(rows), min(cols))

def heuristic(state):
    blue_coords = [c for c, s in state.items() if s.color == PlayerColor.BLUE]
    red_coords = [c for c, s in state.items() if s.color == PlayerColor.RED]

    if not blue_coords:
        return 0
    
    h_dist = dist_h(state, blue_coords, red_coords)
    h_line = line_h(state, blue_coords, red_coords)

    return max(h_dist, h_line)

def search(board: dict[Coord, CellState]
) -> list[Action] | None:
    
    heap = []
    counter = 0         # counter for tiebreak
    weight = 1
    priority = weight * heuristic(board)
    heapq.heappush(heap, (priority,counter,create_root(board)))
    expanded = set()
    costs = {frozenset(board.items()): 0}

    while True: 
        if heap == []:
        # no more possible states
            return None
        # expand next node in queue
        _, _, curr_node = heapq.heappop(heap)
        state_key = frozenset(curr_node.state.items())

        if state_key in expanded:
            continue

        if goal_test(curr_node.state):
            return get_path(curr_node)
        
        expanded.add(state_key)
        
        # create a new node for each valid action applied to next_node
        for action in generate_possible_actions(curr_node):
            next_node = apply_action(action, curr_node)
            next_state_key = frozenset(next_node.state.items())

            next_cost = next_node.cost
            
            if next_state_key not in costs or next_cost < costs[next_state_key]:
                costs[next_state_key] = next_cost

                priority = next_cost + weight*heuristic(next_node.state)

                counter += 1
                heapq.heappush(heap, (priority, counter, next_node))

            # print("For action ", action, " we get:")
            # print(render_board(next_node.state, ansi=True))
