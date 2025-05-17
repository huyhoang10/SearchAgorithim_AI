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


# V(s'): giá trị manhatan khi di chuyển đến trạng thái mới
# P(s,a,s'): xác suất: gán 0.8
# R(s,a) :-1 cho mỗi bước, 100 khi đến đích
# gama: hệ số chiết khấu gán 0.5
# 

# def Q_value(new_state):
#     p = 0.8
#     gama = 0.5
#     r_sa = -1  # khi khong dung trang thai dich, moi buoc di them = -1
#     if new_state == GOAL_STATE:
#         r_sa = 100 # gia tri phan thuong khi di den dich
#     v_snew = -manhattan_distance(new_state)
#     return r_sa + gama*p*v_snew
# def Q_learning(state,path):
#     path.append(state)
#     if state == tuple(GOAL_STATE):
#         return path
#     set_new_state = {}
#     for new_state in Move(state):
#         if new_state in path:
#             continue
#         else:
#             set_new_state[tuple(new_state)] = Q_value(new_state)
#     state = max(set_new_state,key=set_new_state.get) # lay state co Q_value lon nhat
#     print(state)
#     return Q_learning(state,path)


def Q_value(new_state):
    p = 0.8
    gama = 0.5
    r_sa = -1  # phần thưởng mặc định cho mỗi bước
    if new_state == GOAL_STATE:
        r_sa = 100  # phần thưởng nếu đến đích
    v_snew = -manhattan_distance(new_state)
    return r_sa + gama * p * v_snew

def Q_learning(state, path, depth=0, max_depth=50, visited=None):
    if visited is None:
        visited = set()
    path.append(state)
    visited.add(tuple(state))  # lưu trạng thái đã đi

    if state == GOAL_STATE:
        return path,None
    if depth >= max_depth:
        return path,0
    set_new_state = {}
    for new_state in Move(state):
        if tuple(new_state) in visited:
            continue  # tránh lặp
        set_new_state[tuple(new_state)] = Q_value(new_state)

    if not set_new_state:
        return path,0
    best_state = max(set_new_state, key=set_new_state.get)
    return Q_learning(list(best_state), path, depth+1, max_depth, visited)
