import time
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, ""]
class Node():
    def __init__(self, state_current, state_parent, cost=0, depth=0, Heristic=0):
        self.state_current = state_current
        self.state_parent = state_parent
        self.cost = cost
        self.depth = depth
        self.Heristic = Heristic
    def __lt__(self, other):
        return (self.Heristic, self.cost) < (other.Heristic, other.cost)
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

def Pos(pos):
    return pos % 3, pos // 3
def Heristic(n_state):
    return sum(abs(Pos(n_state.index(i))[0] - Pos(GOAL_STATE.index(i))[0]) +
               abs(Pos(n_state.index(i))[1] - Pos(GOAL_STATE.index(i))[1])
               for i in n_state if i != '')

def AStar(state_start, GOAL_STATE):
    time_start = time.time()
    visited = {}
    priority_queue = [(Heristic(state_start), Node(state_start, [], 0))]
    
    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        _, node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return FindPath(GOAL_STATE, visited),time_execute
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append((Heristic(state) + node_current.cost + 1,
                                       Node(state, state_current, node_current.cost + 1)))
    return None,None

def GreedySearch(state_start, GOAL_STATE):
    time_start = time.time()
    visited = {}
    priority_queue = [Node(state_start, [], Heristic(state_start))]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.Heristic)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return FindPath(GOAL_STATE, visited),time_execute
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, Heristic=Heristic(state)))
    return None,None

def IDA(state_start, GOAL_STATE):
    time_start = time.time()
    def search(path, g, threshold):
        node = path[-1]
        if node == GOAL_STATE:
            return path#,time_execute
        f = g + Heristic(node)
        if f > threshold:
            return f
        min_threshold = float('inf')
        for state in Move(node):
            if state not in path:
                path.append(state)
                result = search(path, g + 1, threshold)
                if isinstance(result, list):
                    return result
                if result < min_threshold:
                    min_threshold = result
                path.pop()
        return min_threshold
    
    threshold = Heristic(state_start)
    path = [state_start]
    while True:
        result = search(path, 0, threshold)
        if isinstance(result, list):
            time_execute = round(time.time() - time_start,4)
            return result,time_execute
        if result == float('inf'):
            return None,None
        threshold = result