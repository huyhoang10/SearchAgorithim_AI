import random
import time
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, ""]
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

def random_list(count_random):
    original_list = [1, 2, 3, 4, 5, 6, 7, 8, ""]
    random_list = set()

    while(len(random_list)<count_random):
        shuffled = original_list.copy()
        random.shuffle(shuffled)
        random_list.add(tuple(shuffled))
    return random_list

def AndOrSearch(state_start, GOAL_STATE):
    time_start = time.time()
    MAX_DEPTH = 30
    visited = set()

    def or_search(state, path, depth=0):
        if state == GOAL_STATE:
            return []
        if tuple(state) in path or depth > MAX_DEPTH:
            return None
        visited.add(tuple(state))
        for new_state in Move(state):
            result = and_search([new_state], path + [tuple(state)], depth + 1)
            if result is not None:
                return [new_state] + result
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
        time_execute = round(time.time() - time_start,4)
        return path,time_execute
    else:
        return None,None

def Filter(state):
    for i in range(0,3):
        if state[i] != i+1:
            return False
    return True

def partial_observe():
    with open("partial_observe.txt","w") as f:
        f.write("Partial observe\n")
    start_state_belive = random_list(1000)
    with open("partial_observe.txt","a") as f:
        f.write("start_state:\n")
        f.write(f"{start_state_belive}")
        f.write("\n")
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
            with open("partial_observe.txt","a") as f:
                f.write(f"So lan duyet: {len(visited)}\n")
                f.write(f"Path: {path}")
                f.write("\n")
            return 1
        for new_state in Move(state_current):
            if Filter(new_state) and (tuple(new_state) not in visited):
                queue.append([new_state, path + [state_current]])
    return None

#partial_observe()

def non_observe():
    with open("non_observe.txt","w") as f:
        f.write("Non observe\n")
    start_state_belive = random_list(500)
    with open("non_observe.txt","a") as f:
        f.write("start_state:\n")
        f.write(f"{start_state_belive}")
        f.write("\n")
    queue = [[state,[]] for state in start_state_belive]
    visited = set()
    while queue:
        state_current,path = queue.pop(0)
        visited.add(tuple(state_current))
        if state_current == GOAL_STATE:
            path.append(state_current)
            with open("non_observe.txt","a") as f:
                f.write(f"So lan duyet: {len(visited)}\n")
                f.write(f"Path: {path}")
                f.write("\n")
            return 1
        for new_state in Move(state_current):
            if tuple(new_state) not in visited:
                queue.append([new_state, path + [state_current]])
    return None


non_observe()