import pygame as pg
from SearchAlgorithm import Excute_algorithm
import os

pg.init()
clock = pg.time.Clock()

# Tạo thư mục 'bfs' nếu chưa tồn tại
if not os.path.exists("sthb"):
    os.makedirs("sthb")
frame_count = 0

width_screen,height_screen = 1020,700
screen = pg.display.set_mode([width_screen,height_screen])
screen.fill('white')
running = True
color_frame = (249,212,212)
color_button = (152,112,112)
# setup begin
state_start = [1,8,2,'',4,3,7,6,5]#[1,2,3,4,5,6,'',7,8]
state_goal = [1,2,3,4,5,6,7,8,'']
num_start_state = 0
num_goal_state = 0
name_algorithm = ['BFS','DFS','UCS','IDS','GREEDY','A*','IDA*','SHC','SAHC','STHB','BEAM','GA','And-Or','Par_Obs','Non_Obs','Check','Backtrack','AC3','QLearning']#,'non_observe','partial_observe']
name_button_system = ['Clear','Reset','Export']
x_button_algorithm,y_button_algorithm = 50,400
x_button_system,y_button_system = 550,574
x_start_state,y_start_state = 70,100
x_goal_state,y_goal_state = 690,100
x_current_state,y_current_state = 380,100
width_button, height_button = 80,40
edge_cell = 80
size_frame_info = [70,550,400,100]

def Pos(pos):
    col = pos % 3
    row = pos // 3
    return col,row

def draw_text_on_cel(x,y,wight,height,text):
    text = str(text)
    font = pg.font.SysFont('Arial',30)
    text_surface = font.render(text,True,'black')
    text_wight,text_height = text_surface.get_size()
    text_x = x+(wight-text_wight)//2
    text_y = y+(height-text_height)//2
    screen.blit(text_surface,(text_x,text_y))
    

def draw_frame(x,y,text,state = ['','','','','','','','','']):
    width_edge = 80
    #khung vien
    pg.draw.rect(screen,color_frame,[x,y,260,260])

    for i in range(9):
        pos_x = i % 3
        pos_y = i // 3
        # draw cell + value of cell
        if state[i] == '':
            pg.draw.rect(screen,color_button,[x+5+(pos_x*width_edge)+(pos_x*5),y+5+(pos_y*width_edge)+(pos_y*5),width_edge,width_edge])
        else:
            pg.draw.rect(screen,'white',[x+5+(pos_x*width_edge)+(pos_x*5),y+5+(pos_y*width_edge)+(pos_y*5),width_edge,width_edge])
            draw_text_on_cel(x+5+(pos_x*width_edge)+(pos_x*5),y+5+(pos_y*width_edge)+(pos_y*5),width_edge,width_edge,state[i])
    font = pg.font.SysFont("Arial", 30)
    text_surface = font.render(text,True,"Black")
    text_width,text_height = text_surface.get_size()   
    text_x = x+(260-text_width)//2
    text_y = y-40
    screen.blit(text_surface,(text_x,text_y))

def draw_button(x,y,text):
    pg.draw.rect(screen,color_button,[x,y,width_button,height_button])
    font = pg.font.SysFont('Arial',20)
    text_surface = font.render(text,True,'White')
    text_width,text_height = text_surface.get_size() 
    text_x = x+(width_button-text_width)//2
    text_y = y+(height_button-text_height)//2
    screen.blit(text_surface,(text_x,text_y))

def draw_all_button(x,y,name_button,count_row = 2):
    for i in range(len(name_button)):
        row_i, col_i = i%count_row,i//count_row
        draw_button(x+(col_i*width_button)+(col_i*15),y+(row_i*height_button)+(row_i*15),name_button[i])     # 15 distance two button

# frame time,cost
def Draw_Frame_Info(name_algorithm = "Algorithm",time=0,cost=0):
    x,y,width,height = size_frame_info
    pg.draw.rect(screen,color_frame,[x,y,width,height])
    font_1 = pg.font.SysFont('Arial',30)
    font_2 = pg.font.SysFont('Arial',25)
    text_algorithm = font_1.render(name_algorithm,True,'Black')
    x_text_algorithm = x+(width-text_algorithm.get_width())//2
    y_text_algorithm = y+5
    screen.blit(text_algorithm,(x_text_algorithm,y_text_algorithm))
    text_detail = font_2.render(f'time: {time},cost: {cost}',True,'Black')
    x_text_detail = x+(width-text_detail.get_width())//2
    y_text_detail = y+50
    screen.blit(text_detail,(x_text_detail,y_text_detail))


# DRAW UI BEGIN

# draw state
def Draw_UI():
    draw_frame(x_start_state,y_start_state,"Start State",state_start)
    draw_frame(x_goal_state,y_goal_state,"Goal State",state_goal)
    draw_all_button(x_button_algorithm,y_button_algorithm,name_algorithm)
    draw_all_button(x_button_system,y_button_system,name_button_system,1)
    pg.draw.rect(screen,'white',size_frame_info)
    Draw_Frame_Info()
    pg.display.update()

Draw_UI()

def is_valuable(state_start,state_goal):
    if(None in state_start or None in state_goal):
        return False
    return True

# DRAW UI END
state_i = 0
choose_algorithm = ""
time = 0
cost = 0
index_state = 0
stop_execution = False
path = []

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            
            mouse_x, mouse_y = event.pos
            
            # for i in range(9):  # Duyệt qua 9 ô trong mỗi bảng
            #     col, row = Pos(i)
            #     x, y = x_start_state + 5 + col * (edge_cell + 5), y_start_state + 5 + row * (edge_cell + 5)  # Tọa độ trong "Start State", 5 is distance 2 cell
                
            #     # Kiểm tra nếu chuột nằm trong ô
            #     if x <= mouse_x <= x + edge_cell and y <= mouse_y <= y + edge_cell:
            #         if state_start[i] == None:
            #             num_start_state += 1
            #             pg.draw.rect(screen,'White',[x,y,edge_cell,edge_cell])
            #             draw_text_on_cel(x,y,edge_cell,edge_cell,num_start_state)
            #             state_start[i] = num_start_state
            #             if num_start_state == 8:    
            #                 state_start[state_start.index(None)] = ''

            # choose algorithm
            for i in range(len(name_algorithm)):
                row_i, col_i = i%2,i//2
                x,y = x_button_algorithm +(col_i*width_button)+(col_i*15),y_button_algorithm+(row_i*height_button)+(row_i*15)       # 15 is distance 2 button
                if x <= mouse_x <= x + width_button and y <= mouse_y <= y + height_button:
                    if is_valuable(state_start,state_goal):
                        choose_algorithm = name_algorithm[i]
                        stop_execution = False
                        draw_all_button(x_button_algorithm,y_button_algorithm,name_algorithm,2)
                        pg.draw.rect(screen,'black',[x,y,width_button,height_button],5)
                        Draw_Frame_Info(choose_algorithm)
                        pg.display.update()
                        path,time = Excute_algorithm(choose_algorithm, state_start, state_goal)
                        
                        if(path == None):
                            font = pg.font.SysFont('Arial', 30)
                            txt_surface = font.render("No Path", True, 'black')
                            screen.blit(txt_surface, ((width_screen - txt_surface.get_width()) // 2, 10))
                        else:
                            cost = len(path)
                            Draw_Frame_Info(choose_algorithm,time,cost)
                            export_algorithm = choose_algorithm
                            choose_algorithm = ''
                            index_state = 0
            # button system (Clear, Reset, Export)
            for i in range(len(name_button_system)):
                row_i, col_i = i%1,i//1
                x,y = x_button_system+(col_i*width_button)+(col_i*15),y_button_system+(row_i*height_button)+(row_i*15)  # 15 is distance 2 button
                if x <= mouse_x <= x + width_button and y <= mouse_y <= y + height_button:
                    choose_button_system = name_button_system[i]
                    if choose_button_system == 'Clear':
                        stop_execution = True  # Dừng thuật toán ngay lập tức
                        screen.fill('White')
                        state_start = [None] * 9
                        num_start_state = 0
                        num_goal_state = 0
                        Draw_UI()
                    elif choose_button_system == 'Reset':
                        stop_execution = True
                        screen.fill('White')
                        Draw_UI()
                        draw_frame(x_start_state,y_start_state,'Start State',state_start)
                        draw_frame(x_goal_state,y_goal_state,'Goal State',state_goal)
                        choose_algorithm = ""
                        path = []
                    elif choose_button_system == 'Export':
                        with open('ketqua.txt','a',encoding="utf-8") as f:
                            f.write(export_algorithm+'\n')
                            f.write(f'{state_start} -> {state_goal}\n')
                            for state in path:
                                f.write(str(state)+'\n')
    
    if (path != None) and (index_state < len(path)):
        state_current = path[index_state]
        draw_frame(x_current_state,y_current_state,'State Current',state_current) 
        index_state += 1
    pg.display.update()
    frame_count += 1
    filename = f"sthb/frame_{frame_count:03d}.png"  # frame_000.png, frame_001.png, ...
    #pg.image.save(screen, filename)
    pg.time.wait(300)
pg.display.quit()


