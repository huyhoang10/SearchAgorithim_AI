for i in range(9):  # Duyệt qua 9 ô trong mỗi bảng
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