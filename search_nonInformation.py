import time
class Node():
    def __init__(self, state_current, state_parent, cost=0, depth=0, Heristic=0):
        self.state_current = state_current
        self.state_parent = state_parent
        self.cost = cost
        self.depth = depth
        self.Heristic = Heristic
    def __lt__(self, other):
        return (self.Heristic, self.cost) < (other.Heristic, other.cost)
def Pos(pos):
    return pos % 3, pos // 3

def Move(state):
    state = list(state)
    states_after_swap = []
    col_count, row_count = 3, 3
    loang = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # up, down, left, right
    pos_none = state.index('')
    col_none, row_none = Pos(pos_none)
    
    for x in loang:
        row_swap, col_swap = row_none + x[0], col_none + x[1]
        if 0 <= row_swap < row_count and 0 <= col_swap < col_count:
            pos_swap = row_swap * col_count + col_swap
            arr_swap = state.copy()
            arr_swap[pos_none], arr_swap[pos_swap] = arr_swap[pos_swap], arr_swap[pos_none]
            states_after_swap.append(arr_swap)
    return states_after_swap

def FindPath(GOAL_STATE, visited):
    path = []
    state = tuple(GOAL_STATE)
    while state in visited:
        path.insert(0, list(state))
        state = tuple(visited[state])
    return path

def BFS(state_start, GOAL_STATE):
    time_start = time.time()
    visited = {}
    queue = [Node(state_start, ())]
    while queue:
        node_current = queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = tuple(node_current.state_parent)
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return FindPath(GOAL_STATE, visited),time_execute
        for state in Move(state_current):
            if tuple(state) not in visited:
                queue.append(Node(state, state_current))
    return None,None
               


def DFS(state_start, GOAL_STATE):
    time_start = time.time()
    visited = {}
    stack = [Node(state_start, [])]
    while stack:
        node_current = stack.pop()
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return FindPath(GOAL_STATE, visited),time_execute
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                stack.append(Node(state, state_current))
    return None,None

def UCS(state_start, GOAL_STATE):
    time_start = time.time()
    visited = {}
    priority_queue = [Node(state_start, [], 0)]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.cost)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return FindPath(GOAL_STATE, visited),time_execute
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, node_current.cost + 1))
    return None,None

def IDS(state_start, GOAL_STATE, max_depth):
    time_start = time.time()
    for depth in range(max_depth + 1):
        visited = {}
        stack = [Node(state_start, [], depth=0)]
        while stack:
            node_current = stack.pop()
            state_current = node_current.state_current
            visited[tuple(state_current)] = node_current.state_parent
            
            if state_current == GOAL_STATE:
                time_execute = round(time.time() - time_start,4)
                return FindPath(GOAL_STATE, visited),time_execute
            
            if node_current.depth < depth:
                for state in Move(state_current):
                    if tuple(state) not in visited:
                        stack.append(Node(state, state_current, depth=node_current.depth + 1))
    return None,None