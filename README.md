# Áp dụng thuật toán tìm kiếm vào bài toán 8-Puzzle

## 1. Mục tiêu
Thuật toán tìm kiếm là một trong những thuật toán nền tảng và cốt lõi trong lĩnh vực trí tuệ nhân tạo.
Để củng cố và vận dụng linh hoạt những kiến thức đã học. Với yêu cầu, xây dụng một chương trình giải bài toán 8-Puzzle.
Các mục tiêu đề ra:
Xây dựng một chương trình có giao diện dễ sử dụng
Áp dụng đầy đủ các thuật toán tìm kiếm
Hỗ trợ ghi kết qua ra file.

## 2. Nội dung
**Để giải quyết bài toán tìm kiếm cần xác định những yếu tố sau.**
- Không gian trạng thái: Vị trí các ô số trong bảng 3*3
- Các hành động: di chuyển ô trống: lên, xuống, trái, phải
- Trạng thái xuất phát: một trạng thái hợp lệ
- Trạng thái mục tiêu: [[1,2,3],[4,5,6],[7,8,0]]
- Chi phí: mỗi hành động có giá thành = 1
### 2.1. Các thuật toán tìm kiếm không có thông tin
- 2.1.1. BFS
![alt text](anh_gif/bfs.gif)
- 2.1.2. DFS
![alt text](anh_gif/dfs.gif)
- 2.1.3. UCS
![alt text](anh_gif/ucs.gif)
- 2.1.4. IDS
![alt text](anh_gif/iddfs.gif)
- So sánh hiệu suất về thời gian:
![alt text](anh_tinh/time_noninfor.png)
Phân tích:
- BFS phù hợp với tìm kiếm không có trọng số và thường tìm lời giải tối ưu nếu độ sâu nhỏ. Hiệu quả khá cao.
- DFS nếu không gặp lời giải sớm, càng đi sâu thời gian sẽ càng lớn.
- UCS đảm bảo tìm lời giải tối ưu, nhưng trong bài toán 8 puzzle chi phí mỗi bước đi đồng đều nên thời gian tìm kiếm chậm hơn BFS.
- IDDFS là sự kết hợp ưu điểm của BFS và DFS, nên tối ưu hơn về chi phí, thời gian lẫn không gian bộ nhớ.

### 2.2. Các thuật toán tìm kiếm có thông tin
- 2.2.1. Greedy
![alt text](anh_gif/greedy.gif)
- 2.2.2. A*
![alt text](anh_gif/astar.gif)
- 2.2.3. IDA*
![alt text](anh_gif/ida.gif)

- So sánh hiệu suất về thời gian:
![alt text](anh_tinh/time_hasInfo.png)
Phân tích:
- Greedy và A* đều rất nhanh, nhưng A* ưu việt hơn vì đảm bảo lời giải tốt.
- IDA* là phiên bản cải tiến về bộ nhớ của A*, IDA* chậm hơn do việc lặp lại, phù hợp khi bộ nhớ bị giới hạn.

### 2.3. Các thuật toán tìm kiếm cục bộ
- 2.3.1. Simple hill climbing
![alt text](anh_gif/shc.gif)
- 2.3.2. Stochastic hill climbing
![alt text](anh_gif/sthb.gif)
- 2.3.3. Steepest Ascent hill climbing
![alt text](anh_gif/sahc.gif)
- 2.3.4. Beam Search
TH1: 
![alt text](anh_gif/beam.gif)
TH2:
![alt text](anh_gif/beam2.gif)
- 2.3.5. Generate Seach
TH1:
![alt text](anh_gif/ga.gif)
TH2:
![alt text](anh_gif/ga2.gif)

- So sánh hiệu suất về thời gian:
![alt text](anh_tinh/time_local.png)
Phân tích:
- SHB,STHB,SAHC có ưu điểm tìm kiếm rất nhanh. Nhược điểm, nhiều trường hợp  không tìm được lời giải do tìm kiếm trên 1 vùng cục bộ, dễ bị kẹt ở điểm local maximum.
- Beam dùng để giải quyết nhược điểm trên bằng cách chọn 1 tập giới hạn trạng thái tối ưu. 
- GA là thuật toán tiến hóa mô phỏng tự nhiên, đòi hỏi nhiều vòng lặp (generation), nhiều phép lai ghép và đột biến.
### 2.4. Các thuật toán tìm kiếm trong môi trường phức tạp
- 2.4.1. Non-Observe
![alt text](anh_tinh/non_obsebve1.png)
![alt text](anh_tinh/non_observe2.png)
- 2.4.2. Partial-Observe
![alt text](anh_tinh/partial_observe.png)
![alt text](anh_tinh/partial_observe2.png)
- 2.4.3. AndOr
![alt text](anh_gif/andor.gif)

Phân tích:
- Không giống như các thuật toán ở trên, tìm kiếm trong môi trường phức tạp không có chính xác trạng thái ban đầu, trạng thái đích mà dựa vào tập trạng thái niềm tim, vì thế không gian trạng thái vô cùng lớn.

### 2.5. Các thuật toán tìm kiếm trong môi trường ràng buộc
- 2.5.1. Checked

![alt text](anh_tinh/check.png)
- 2.5.2. BackTracking

![alt text](anh_tinh/Backtracking.png)
- 2.5.3. AC-3

![alt text](anh_tinh/AC3.png)
### 2.6. Q-Learning
![alt text](anh_gif/qlearning.gif)

## 3. Kết luận
