import math
import time
import random


def count_inversions(state):
    """Đếm số cặp nghịch thế (inversions) trong danh sách"""
    flat_list = []  # Bỏ qua ô trống ''
    for i in state:
        if i != "":
            flat_list.append(i)
    inversions = 0
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inversions += 1
    return inversions

def is_solvable(state_start, state_goal):
    """Kiểm tra xem trạng thái đầu có thể biến đổi thành trạng thái đích không"""
    return count_inversions(state_start) % 2 == count_inversions(state_goal) % 2

class Node():
    def __init__(self, state_current, state_parent, cost=0, depth=0, heuristic=0):
        self.state_current = state_current
        self.state_parent = state_parent
        self.cost = cost
        self.depth = depth
        self.heuristic = heuristic
    def __lt__(self, other):
        return (self.heuristic, self.cost) < (other.heuristic, other.cost)
def Move(n_state):
    states_after_swap = []
    col_count, row_count = 3, 3
    loang = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # up, down, left, right
    pos_none = n_state.index('')
    col_none, row_none = Pos(pos_none)
    
    for x in loang:
        row_swap, col_swap = row_none + x[0], col_none + x[1]
        if 0 <= row_swap < row_count and 0 <= col_swap < col_count:
            pos_swap = row_swap * col_count + col_swap
            arr_swap = n_state.copy()
            arr_swap[pos_none], arr_swap[pos_swap] = arr_swap[pos_swap], arr_swap[pos_none]
            states_after_swap.append(arr_swap)
    return states_after_swap

def Pos(pos):
    return pos % 3, pos // 3

def FindPath(state_goal, visited):
    path = []
    state = tuple(state_goal)
    while state in visited:
        path.insert(0, list(state))
        state = tuple(visited[state])
    return path

def BFS(state_start, state_goal):
    visited = {}
    queue = [Node(state_start, [])]
    
    while queue:
        node_current = queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == state_goal:
            return FindPath(state_goal, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                queue.append(Node(state, state_current))
    return None

def DFS(state_start, state_goal):
    visited = {}
    stack = [Node(state_start, [])]
    
    while stack:
        node_current = stack.pop()
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == state_goal:
            return FindPath(state_goal, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                stack.append(Node(state, state_current))
    return "Không tìm thấy đường đi"

def UCS(state_start, state_goal):
    visited = {}
    priority_queue = [Node(state_start, [], 0)]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.cost)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == state_goal:
            return FindPath(state_goal, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, node_current.cost + 1))
    return "Không tìm thấy đường đi"

def IDS(state_start, state_goal, max_depth):
    for depth in range(max_depth + 1):
        visited = {}
        stack = [Node(state_start, [], depth=0)]
        while stack:
            node_current = stack.pop()
            state_current = node_current.state_current
            visited[tuple(state_current)] = node_current.state_parent
            
            if state_current == state_goal:
                return FindPath(state_goal, visited)
            
            if node_current.depth < depth:
                for state in Move(state_current):
                    if tuple(state) not in visited:
                        stack.append(Node(state, state_current, depth=node_current.depth + 1))
    return "Không tìm thấy đường đi"

def Heristic(n_state, goal_state):
    return sum(abs(Pos(n_state.index(i))[0] - Pos(goal_state.index(i))[0]) +
               abs(Pos(n_state.index(i))[1] - Pos(goal_state.index(i))[1])
               for i in n_state if i != '')

def AStar(state_start, state_goal):
    visited = {}
    priority_queue = [(Heristic(state_start, state_goal), Node(state_start, [], 0))]
    
    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        _, node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == state_goal:
            return FindPath(state_goal, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append((Heristic(state, state_goal) + node_current.cost + 1,
                                       Node(state, state_current, node_current.cost + 1)))
    return "Không tìm thấy đường đi"

def GreedySearch(state_start, state_goal):
    visited = {}
    priority_queue = [Node(state_start, [], Heristic(state_start, state_goal))]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.heuristic)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == state_goal:
            return FindPath(state_goal, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, heuristic=Heristic(state, state_goal)))
    return "Không tìm thấy đường đi"

def IDA(state_start, state_goal):
    def search(path, g, threshold):
        node = path[-1]
        f = g + Heristic(node, state_goal)
        if f > threshold:
            return f
        if node == state_goal:
            return path
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
    
    threshold = Heristic(state_start, state_goal)
    path = [state_start]
    while True:
        result = search(path, 0, threshold)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return "Không tìm thấy đường đi"
        threshold = result

# state_start = [1, 2, 3, 4, 5, 6, 7, 8, '']
# state_goal = [1, 2, 3, 4, 5, 6, '', 7, 8]


def SHC(state_start, state_goal): #simple Hill climbing
    path = []
    state_current = state_start
    path.append(state_current)
    while True:
        if state_start == state_goal:
            return path
        else:
            new_state = state_current.copy()
            for state in Move(state_current):
                if Heristic(state,state_goal) < Heristic(state_current,state_goal):
                    new_state = state
                    path.append(state)
            if new_state == state_current:
                return path
            state_current = new_state

def SAHC(state_start, state_goal): #Steepest-Ascent hill climbing
    path = []
    state_current = state_start
    path.append(state_current)
    while True:
        if state_current == state_goal:
            return path
        else:
            new_state = min(Move(state_current), key=lambda state: Heristic(state, state_goal))
            if Heristic(new_state,state_goal) < Heristic(state_current,state_goal):
                state_current = new_state
                path.append(new_state)
            else: 
                return path
            
#print(SAHC(state_start,state_goal))
            
def STHB(state_start,state_goal): # leo doi ngau nhien
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == state_goal:
            return path
        else:
            neighbord = Move(state_current)
            while True:
                if len(neighbord) == 0:
                    return path
                new_state = neighbord.pop(random.randint(0,len(neighbord)-1))
                if Heristic(new_state,state_goal) < Heristic(state_current,state_goal):
                    state_current = new_state
                    path.append(state_current)
                    break
                
def Probability(state_current,state,t):
    return math.exp((Heristic(state)-Heristic(state_current))/t)
    
def SA(state_start,state_goal): # luyện kim
    t = 10**4
    alpha = 0.99
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == state_goal:
            return path
        else:
            neighbords = Move(state_current)
            while True:
                if not neighbords:
                    new_state = min(Move(state_current), key = lambda state: Probability(state_current,state,t))
                    state_current = new_state
                    path.append(state_current)
                    t *= alpha
                    break
                new_state = neighbords.pop(random.randint(0,len(neighbords)-1))
                if Heristic(new_state,state_goal) < Heristic(state_current,state_goal):
                    state_current = new_state
                    path.append(state_current)
                    break         

def BeamSearch(state_start, state_goal, beam_width=3):
    from heapq import heappush, heappop
    
    def heuristic(state):
        return Heristic(state, state_goal)

    visited = set()
    visited_dic = {}
    beam = [(heuristic(state_start), Node(state_start, [], 0))]
    path = []
    while beam:
        # Chọn các node hiện tại trong beam
        new_beam = []
        for _, node in beam:
            state_current = node.state_current
            if state_current == state_goal:
                path.append(state_goal)
                state_parent = visited_dic[tuple(state_goal)]
                while state_parent != tuple(state_start):
                    path.insert(0,state_parent)
                    state_parent = visited_dic[tuple(state_parent)]
                path.insert(0,tuple(state_start))
                return path
            visited.add(tuple(state_current))
            for state in Move(state_current):
                if tuple(state) not in visited:
                    new_node = Node(state, state_current, cost=node.cost + 1, heuristic=heuristic(state))
                    visited_dic[tuple(state)] = tuple(state_current)
                    heappush(new_beam, (new_node.heuristic, new_node))

        # Lấy beam_width trạng thái tốt nhất
        beam = []
        count = 0
        while new_beam and count < beam_width:
            beam.append(heappop(new_beam))
            count += 1

    return None


def AndOrSearch(state_start, state_goal):
    def or_search(state, path):
        if state == state_goal:
            return []
        if tuple(state) in path:
            return None
        plans = []
        for action in Move(state):
            result_plan = and_search([action], path + [tuple(state)])
            if result_plan is not None:
                plans.append((action, result_plan))
        if plans:
            return plans
        return None

    def and_search(states, path):
        plans = []
        for state in states:
            plan = or_search(state, path)
            if plan is None:
                return None
            plans.append(plan)
        return plans

    plan = or_search(state_start, [])
    return plan if plan else None

def Excute_algorithm(name_algorithm, state_start, state_goal):
    time_start = time.time()
    global stop_execution
    stop_execution = False  # Clear trạng thái khi bắt đầu thuật toán
    
    if name_algorithm == '':
        return None
    elif not is_solvable(state_start, state_goal):
        return None

    algorithms = {
        'BFS': BFS,
        'DFS': DFS,
        'UCS': UCS,
        'GREEDY': GreedySearch,
        'A*': AStar,
        'IDS': lambda s, g: IDS(s, g, max_depth=1000),
        'IDA*': IDA,
        'SHC': SHC,
        'SAHC': SAHC,
        'STHB': STHB,
        'SA': SA,
        'BEAM': lambda s, g: BeamSearch(s, g, beam_width=3),
        'And-Or':AndOrSearch
    }

    path = algorithms[name_algorithm](state_start, state_goal)
    time_execute = round(time.time() - time_start,4)
    step = len(path)
    cost = 0
    return path,time_execute,step,cost
