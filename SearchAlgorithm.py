import math
import time
import random

GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, ""]

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

def is_solvable(state_start):
    """Kiểm tra xem trạng thái đầu có thể biến đổi thành trạng thái đích không"""
    return count_inversions(state_start) % 2 == 0

class Node():
    def __init__(self, state_current, state_parent, cost=0, depth=0, Heristic=0):
        self.state_current = state_current
        self.state_parent = state_parent
        self.cost = cost
        self.depth = depth
        self.Heristic = Heristic
    def __lt__(self, other):
        return (self.Heristic, self.cost) < (other.Heristic, other.cost)
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

def FindPath(GOAL_STATE, visited):
    path = []
    state = tuple(GOAL_STATE)
    while state in visited:
        path.insert(0, list(state))
        state = tuple(visited[state])
    return path

def BFS(state_start, GOAL_STATE):
    visited = {}
    queue = [Node(state_start, [])]
    
    while queue:
        node_current = queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            return FindPath(GOAL_STATE, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                queue.append(Node(state, state_current))
    return None

def DFS(state_start, GOAL_STATE):
    visited = {}
    stack = [Node(state_start, [])]
    
    while stack:
        node_current = stack.pop()
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            return FindPath(GOAL_STATE, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                stack.append(Node(state, state_current))
    return "Không tìm thấy đường đi"

def UCS(state_start, GOAL_STATE):
    visited = {}
    priority_queue = [Node(state_start, [], 0)]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.cost)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            return FindPath(GOAL_STATE, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, node_current.cost + 1))
    return "Không tìm thấy đường đi"

def IDS(state_start, GOAL_STATE, max_depth):
    for depth in range(max_depth + 1):
        visited = {}
        stack = [Node(state_start, [], depth=0)]
        while stack:
            node_current = stack.pop()
            state_current = node_current.state_current
            visited[tuple(state_current)] = node_current.state_parent
            
            if state_current == GOAL_STATE:
                return FindPath(GOAL_STATE, visited)
            
            if node_current.depth < depth:
                for state in Move(state_current):
                    if tuple(state) not in visited:
                        stack.append(Node(state, state_current, depth=node_current.depth + 1))
    return "Không tìm thấy đường đi"

def Heristic(n_state):
    return sum(abs(Pos(n_state.index(i))[0] - Pos(GOAL_STATE.index(i))[0]) +
               abs(Pos(n_state.index(i))[1] - Pos(GOAL_STATE.index(i))[1])
               for i in n_state if i != '')

def AStar(state_start, GOAL_STATE):
    visited = {}
    priority_queue = [(Heristic(state_start), Node(state_start, [], 0))]
    
    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        _, node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            return FindPath(GOAL_STATE, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append((Heristic(state) + node_current.cost + 1,
                                       Node(state, state_current, node_current.cost + 1)))
    return "Không tìm thấy đường đi"

def GreedySearch(state_start, GOAL_STATE):
    visited = {}
    priority_queue = [Node(state_start, [], Heristic(state_start))]
    
    while priority_queue:
        priority_queue.sort(key=lambda node: node.Heristic)
        node_current = priority_queue.pop(0)
        state_current = node_current.state_current
        visited[tuple(state_current)] = node_current.state_parent
        
        if state_current == GOAL_STATE:
            return FindPath(GOAL_STATE, visited)
        
        for state in Move(state_current):
            if tuple(state) not in visited:
                priority_queue.append(Node(state, state_current, Heristic=Heristic(state)))
    return "Không tìm thấy đường đi"

def IDA(state_start, GOAL_STATE):
    def search(path, g, threshold):
        node = path[-1]
        f = g + Heristic(node)
        if f > threshold:
            return f
        if node == GOAL_STATE:
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
    
    threshold = Heristic(state_start)
    path = [state_start]
    while True:
        result = search(path, 0, threshold)
        if isinstance(result, list):
            return result
        if result == float('inf'):
            return "Không tìm thấy đường đi"
        threshold = result

# state_start = [1, 2, 3, 4, 5, 6, 7, 8, '']
# GOAL_STATE = [1, 2, 3, 4, 5, 6, '', 7, 8]


def SHC(state_start, GOAL_STATE): #simple Hill climbing
    path = []
    state_current = state_start
    path.append(state_current)
    while True:
        if state_start == GOAL_STATE:
            return path
        else:
            new_state = state_current.copy()
            for state in Move(state_current):
                if Heristic(state) < Heristic(state_current):
                    new_state = state
                    path.append(state)
            if new_state == state_current:
                return path
            state_current = new_state

def SAHC(state_start, GOAL_STATE): #Steepest-Ascent hill climbing
    path = []
    state_current = state_start
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            return path
        else:
            new_state = min(Move(state_current), key=lambda state: Heristic(state))
            if Heristic(new_state) < Heristic(state_current):
                state_current = new_state
                path.append(new_state)
            else: 
                return path
            
            
def STHB(state_start,GOAL_STATE): # leo doi ngau nhien
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            return path
        else:
            neighbord = Move(state_current)
            while True:
                if len(neighbord) == 0:
                    return path
                new_state = neighbord.pop(random.randint(0,len(neighbord)-1))
                if Heristic(new_state) < Heristic(state_current):
                    state_current = new_state
                    path.append(state_current)
                    break
                
def Probability(state_current,state,t):
    return math.exp((Heristic(state)-Heristic(state_current))/t)
    
def SA(state_start,GOAL_STATE): # luyện kim
    t = 10**4
    alpha = 0.99
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            return path
        else:
            neighbords = Move(state_current)
            while True:
                if not neighbords:
                    if(t<0.01):
                        return None
                    new_state = min(Move(state_current), key = lambda state: Probability(state_current,state,t))
                    state_current = new_state
                    path.append(state_current)
                    t *= alpha
                    break
                new_state = neighbords.pop(random.randint(0,len(neighbords)-1))
                if Heristic(new_state) < Heristic(state_current):
                    state_current = new_state
                    path.append(state_current)
                    break         

def BeamSearch(state_start, GOAL_STATE, beam_width=3):
    from heapq import heappush, heappop

    visited = set()
    visited_dic = {}
    beam = [(Heristic(state_start), Node(state_start, [], 0))]
    path = []
    while beam:
        # Chọn các node hiện tại trong beam
        new_beam = []
        for _, node in beam:
            state_current = node.state_current
            if state_current == GOAL_STATE:
                path.append(GOAL_STATE)
                state_parent = visited_dic[tuple(GOAL_STATE)]
                while state_parent != tuple(state_start):
                    path.insert(0,state_parent)
                    state_parent = visited_dic[tuple(state_parent)]
                path.insert(0,tuple(state_start))
                return path
            visited.add(tuple(state_current))
            for state in Move(state_current):
                if tuple(state) not in visited:
                    new_node = Node(state, state_current, cost=node.cost + 1, Heristic=Heristic(state))
                    visited_dic[tuple(state)] = tuple(state_current)
                    heappush(new_beam, (new_node.Heristic, new_node))

        # Lấy beam_width trạng thái tốt nhất
        beam = []
        count = 0
        while new_beam and count < beam_width:
            beam.append(heappop(new_beam))
            count += 1

    return None


def AndOrSearch(state_start, GOAL_STATE):
    MAX_DEPTH = 30
    visited = set()

    def or_search(state, path, depth=0):
        if state == GOAL_STATE:
            return []
        if tuple(state) in path or depth > MAX_DEPTH:
            return None
        visited.add(tuple(state))
        for action in Move(state):
            result = and_search([action], path + [tuple(state)], depth + 1)
            if result is not None:
                return [action] + result
        return None

    def and_search(states, path, depth):
        plan = []
        for state in states:
            subplan = or_search(state, path, depth)
            if subplan is None:
                return None
            plan.extend(subplan)
        return plan

    plan = or_search(state_start, [])
    if plan:
        # Dựng lại đường đi theo kế hoạch đã tìm được
        path = [state_start]
        current = state_start[:]
        for next_state in plan:
            current = next_state
            path.append(current)
        return path
    else:
        return None


# Genetic Search Algorithm
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, ""]
MOVES = ["up", "down", "left", "right"]
POP_SIZE = 100
MAX_GENERATIONS = 1000
MOVE_SEQ_LENGTH = 30  # Độ dài chuỗi hành động
MUTATION_RATE = 0.2
ELITE_RATE = 0.05

# ==== Áp dụng chuỗi di chuyển lên trạng thái ban đầu ====
def apply_moves(state, moves):
    state = state[:]
    for move in moves:
        state = move_tile(state, move)
    return state

def move_tile(state, move):
    state = state[:]
    idx = state.index("")
    row, col = idx // 3, idx % 3

    if move == "up" and row > 0:
        swap_idx = idx - 3
    elif move == "down" and row < 2:
        swap_idx = idx + 3
    elif move == "left" and col > 0:
        swap_idx = idx - 1
    elif move == "right" and col < 2:
        swap_idx = idx + 1
    else:
        return state  # Không hợp lệ, giữ nguyên

    state[idx], state[swap_idx] = state[swap_idx], state[idx]
    return state

# ==== Tính khoảng cách manhattan ====
def manhattan_distance(state):
    dist = 0
    for i, tile in enumerate(state):
        if tile == "":
            continue
        goal_idx = GOAL_STATE.index(tile)
        x1, y1 = i % 3, i // 3
        x2, y2 = goal_idx % 3, goal_idx // 3
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist

# ==== Hàm fitness ====
def fitness(moves, initial_state):
    result_state = apply_moves(initial_state, moves)
    dist = manhattan_distance(result_state)
    return 100 - dist  # fitness càng cao càng tốt

# ==== Tạo chuỗi hành động ngẫu nhiên ====
def generate_individual():
    return [random.choice(MOVES) for _ in range(MOVE_SEQ_LENGTH)]

# ==== Lai ghép chuỗi hành động ====
def crossover(parent1, parent2):
    idx = random.randint(1, MOVE_SEQ_LENGTH - 2)
    return parent1[:idx] + parent2[idx:]

# ==== Đột biến ====
def mutate(moves):
    new_moves = moves[:]
    for i in range(len(new_moves)):
        if random.random() < MUTATION_RATE:
            new_moves[i] = random.choice(MOVES)
    return new_moves

# ==== In trạng thái 3x3 ====
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

# ==== GA chính ====
def genetic_algorithm(start_state,GOAL_STATE):
    population = [generate_individual() for _ in range(POP_SIZE)]

    for generation in range(MAX_GENERATIONS):
        scored = [(fitness(ind, start_state), ind) for ind in population]
        scored.sort(reverse=True)
        best_fitness, best_moves = scored[0]
        best_state = apply_moves(start_state, best_moves)
        if best_state == GOAL_STATE:
            path = [start_state]
            current_state = start_state
            for move in best_moves:
                current_state = move_tile(current_state,move)
                path.append(current_state)
            return path

        # Elitism
        elite_count = int(POP_SIZE * ELITE_RATE)
        new_population = [ind for _, ind in scored[:elite_count]]

        # Sinh cá thể mới
        while len(new_population) < POP_SIZE:
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population
    return None

# end GA

def random_list(count_random):
    original_list = [1, 2, 3, 4, 5, 6, 7, 8, ""]
    random_lists = []

    for _ in range(count_random):
        shuffled = original_list.copy()
        random.shuffle(shuffled)
        random_lists.append(shuffled)
    return random_lists


def Filter(state):
    for i in range(0,3):
        if state[i] != i+1:
            return False
    return True

def partial_observe():
    start_state_belive = random_list(1000)
    queue = []
    for state in start_state_belive:
        if Filter(state): 
            queue.append([state,[]])
    visited = set()
    while queue:
        state_current,path = queue.pop(0)
        visited.add(tuple(state_current))
        if state_current == GOAL_STATE:
            path.append(state_current)
            return path
        for new_state in Move(state_current):
            if Filter(new_state) and (tuple(new_state) not in visited):
                queue.append([new_state, path + [state_current]])
    return None


def non_observe():
    start_state_belive = random_list(1000)
    queue = [[state,[]] for state in start_state_belive]
    visited = set()
    while queue:
        state_current,path = queue.pop(0)
        visited.add(tuple(state_current))
        if state_current == GOAL_STATE:
            path.append(state_current)
            return path
        for new_state in Move(state_current):
            if tuple(new_state) not in visited:
                queue.append([new_state, path + [state_current]])
    return None

def Excute_algorithm(name_algorithm, state_start, GOAL_STATE):
    time_start = time.time()
    global stop_execution
    stop_execution = False  # Clear trạng thái khi bắt đầu thuật toán
    
    if name_algorithm == '':
        return None
    elif not is_solvable(state_start):
        return None
    algorithms = {
    'BFS': BFS(state_start, GOAL_STATE),               # Breadth-First Search
    'DFS': DFS(state_start, GOAL_STATE),               # Depth-First Search
    'UCS': UCS(state_start, GOAL_STATE),               # Uniform Cost Search
    'GREEDY': GreedySearch(state_start, GOAL_STATE),   # Greedy Best-First Search
    'A*': AStar(state_start, GOAL_STATE),              # A* Search
    'IDS': IDS(state_start, GOAL_STATE, max_depth=1000), # Iterative Deepening Search
    'IDA*': IDA(state_start, GOAL_STATE),              # Iterative Deepening A*
    'SHC': SHC(state_start, GOAL_STATE),               # Steepest Hill Climbing
    'SAHC': SAHC(state_start, GOAL_STATE),             # Stochastic Steepest-Ascent Hill Climbing
    'STHB': STHB(state_start, GOAL_STATE),             # Simulated Threshold Beam (hoặc có thể là Stochastic Hill Beam - cần xem định nghĩa)
    'SA': SA(state_start, GOAL_STATE),                 # Simulated Annealing
    'BEAM': BeamSearch(state_start, GOAL_STATE, beam_width=3), # Beam Search
    'GA': genetic_algorithm(state_start, GOAL_STATE),  # Genetic Algorithm
    'And-Or': AndOrSearch(state_start, GOAL_STATE),    # And-Or Graph Search
    'non_observe': non_observe(),                      # Search in Fully Observable Environment
    'partial_observe': partial_observe()              # Search in Partially Observable Environment
    }
    
    path = algorithms[name_algorithm]
    time_execute = round(time.time() - time_start,4)
    return path,time_execute
