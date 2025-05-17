import math
import random
import time
from heapq import heappush, heappop

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


def SHC(state_start, GOAL_STATE):  # Simple Hill Climbing
    time_start = time.time()
    path = []
    state_current = state_start
    path.append(state_current)

    while True:
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start, 10)
            return path, time_execute

        neighbors = Move(state_current)
        better_state = None
        for state in neighbors:
            if Heristic(state) < Heristic(state_current):
                if better_state is None or Heristic(state) < Heristic(better_state):
                    better_state = state
    
        if better_state is None:  # no better neighbor
            time_execute = round((time.time() - time_start), 10)
            return [], time_execute

        state_current = better_state
        path.append(state_current)

def SAHC(state_start, GOAL_STATE): #Steepest-Ascent hill climbing
    time_start = time.time()
    path = []
    state_current = state_start
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,10)
            return path,time_execute
        else:
            new_state = min(Move(state_current), key=lambda state: Heristic(state))
            if Heristic(new_state) < Heristic(state_current):
                state_current = new_state
                path.append(new_state)
            else: 
                time_execute = round(time.time() - time_start,10)
                return [],time_execute
            
            
def STHB(state_start,GOAL_STATE): # leo doi ngau nhien
    time_start = time.time()
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,10)
            return path,time_execute
        else:
            neighbord = Move(state_current)
            while True:
                if len(neighbord) == 0:
                    time_execute = round(time.time() - time_start,10)
                    return [],time_execute  
                new_state = neighbord.pop(random.randint(0,len(neighbord)-1))
                if Heristic(new_state) < Heristic(state_current):
                    state_current = new_state
                    path.append(state_current)
                    break
                
def Probability(state_current,state,t):
    return math.exp((Heristic(state)-Heristic(state_current))/t)
    
def SA(state_start,GOAL_STATE): # luyện kim
    time_start = time.time()
    t = 10**4
    alpha = 0.99
    state_current = state_start
    path = []
    path.append(state_current)
    while True:
        if state_current == GOAL_STATE:
            time_execute = round(time.time() - time_start,4)
            return path,time_execute
        else:
            neighbords = Move(state_current)
            while True:
                if not neighbords:
                    if(t<0.01):
                        return None,None
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
    time_start = time.time()
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
                time_execute = round(time.time() - time_start,5)
                return path,time_execute
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

    return None,None

# Genetic Search Algorithm
MOVES = ["up", "down", "left", "right"]
POP_SIZE = 100
MAX_GENERATIONS = 1000
MOVE_SEQ_LENGTH = 30  # Độ dài chuỗi hành động
MUTATION_RATE = 0.2
ELITE_RATE = 0.05

#  Áp dụng chuỗi di chuyển lên trạng thái ban đầu 
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

#  Tính khoảng cách manhattan 
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

#  Hàm fitness 
def fitness(moves, initial_state):
    result_state = apply_moves(initial_state, moves)
    dist = manhattan_distance(result_state)
    return 100 - dist  # fitness càng cao càng tốt

#  Tạo chuỗi hành động ngẫu nhiên 
def generate_individual():
    return [random.choice(MOVES) for _ in range(MOVE_SEQ_LENGTH)]

#  Lai ghép chuỗi hành động 
def crossover(parent1, parent2):
    idx = random.randint(1, MOVE_SEQ_LENGTH - 2)
    return parent1[:idx] + parent2[idx:]

#  Đột biến 
def mutate(moves):
    new_moves = moves[:]
    for i in range(len(new_moves)):
        if random.random() < MUTATION_RATE:
            new_moves[i] = random.choice(MOVES)
    return new_moves

#  In trạng thái 3x3 
def print_state(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])

#  GA chính 
def genetic_algorithm(start_state,GOAL_STATE):
    time_start = time.time()
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
            time_execute = round(time.time() - time_start,4)
            return path,time_execute

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
    return None,None
