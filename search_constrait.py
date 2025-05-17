import random
import time
def random_list(count_random):
    original_list = [1, 2, 3, 4, 5, 6, 7, 8, ""]
    random_list = set()

    while(len(random_list)<count_random):
        shuffled = original_list.copy()
        random.shuffle(shuffled)
        random_list.add(tuple(shuffled))
    return random_list
def Constraint(array,i):
    if(i==8 and array[i] != ''):
        return False
    if i < 8 :
        if array[i] == '':
            return False

        elif (i > 0) and (array[i] != (array[i-1] + 1)):
            return False
    return True

def Check():
    time_start = time.time()
    list_state = random_list(362880)
    for k in range(len(list_state)):
        state = list_state[k]
        for i in range(len(state)-1):
            if Constraint(state,i)==False:
                break
            if i == 7:
                time_execute = round(time.time() - time_start,4)
                print(f'So lan thu de thanh cong:{k}')
                print(f"thoi gian den lan thu thanh cong: {time_execute}")
                return 1
    return None


start_state = [None]*9
set_value = [1,5,4,3,2,"",7,6,8]
def Backtracking(i, set_value, state):
    if i > 8:
        with open("cps.txt","a") as f:
                f.write(f"{state}\n")
        return state
    
    for value in list(set_value):  # tạo bản sao để duyệt an toàn
        state[i] = value
        if Constraint(state, i):
            set_value.remove(value)
            result = Backtracking(i + 1, set_value, state)
            if result:
                return result
            set_value.add(value)  # backtrack
        with open("cps.txt","a") as f:
                f.write(f"{state}\n") 
        state[i] = None  # reset vị trí i khi không hợp lệ
    return None 

#Backtracking(0,set_value,start_state)
# start_state = [None]*9
set_value = tuple([5,4,3,2,"",7,6,1,8])
def AC3(xi,state,tried,set_value):
    #new_tried = tried
    if xi>8:
        with open("cps.txt","a") as f:
                f.write(f"{state}\n")
        return state
    for value in list(set_value):
        if xi == 0:
            if value in tried:
                continue
            else: tried.append(value)
                #new_tried += [value]
        state[xi] = value
        #print(state)
        if Constraint(state,xi):
            return AC3(xi+1,state,tried,set_value)
    state[xi] = None
    with open("cps.txt","a") as f:
                f.write(f"{state}\n")
    return AC3(xi=0,state=[None]*9,tried=tried,set_value=set_value)

AC3(0,start_state,[],set_value)