import math
import time
import random
from search_nonInformation import *
from search_Information import *
from search_local import *
from search_complexEnveroment import *
from search_constrait import *
from q_learning import Q_learning
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, ""]

def Excute_algorithm(name_algorithm, start_state, goal_state):
    global stop_execution
    stop_execution = False  # Clear trạng thái khi bắt đầu thuật toán
    if name_algorithm == '':
        return None
    elif not is_solvable(start_state):
        return None
    algorithms = {
    'BFS': BFS(start_state, goal_state),               # Breadth-First Search
    'DFS': DFS(start_state, goal_state),               # Depth-First Search
    'UCS': UCS(start_state, goal_state),  
    'IDS': IDS(start_state, goal_state, max_depth=1000), # Iterative Deepening Search             # Uniform Cost Search
    'GREEDY': GreedySearch(start_state, goal_state),   # Greedy Best-First Search
    'A*': AStar(start_state, goal_state),              # A* Search
    'IDA*': IDA(start_state, goal_state),              # Iterative Deepening A*
    'SHC': SHC(start_state, goal_state),               # Steepest Hill Climbing
    'SAHC': SAHC(start_state, goal_state),             # Stochastic Steepest-Ascent Hill Climbing
    'STHB': STHB(start_state, goal_state),             # Simulated Threshold Beam (hoặc có thể là Stochastic Hill Beam - cần xem định nghĩa)          # Simulated Annealing
    'BEAM': BeamSearch(start_state, goal_state, beam_width=3), # Beam Search
    'GA': genetic_algorithm(start_state, goal_state),  # Genetic Algorithm
    'And-Or': AndOrSearch(start_state, goal_state),    # And-Or Graph Search
    'QLearning':Q_learning(start_state,[],0,100)
    }
    path,time_execute = algorithms[name_algorithm]
    return path,time_execute


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

def Pos(pos):
    return pos % 3, pos // 3

def FindPath(GOAL_STATE, visited):
    path = []
    state = tuple(GOAL_STATE)
    while state in visited:
        path.insert(0, list(state))
        state = tuple(visited[state])
    return path

def Heristic(n_state):
    return sum(abs(Pos(n_state.index(i))[0] - Pos(GOAL_STATE.index(i))[0]) +
               abs(Pos(n_state.index(i))[1] - Pos(GOAL_STATE.index(i))[1])
               for i in n_state if i != '')

# V(s'): giá trị manhatan khi di chuyển đến trạng thái mới
# P(s,a,s'): xác suất: gán 0.8
# R(s,a) :-1 cho mỗi bước, 100 khi đến đích
# gama: hệ số chiết khấu gán 0.5
# 
