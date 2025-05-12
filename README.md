# Áp dụng thuật toán tìm kiếm vào bài toán 8-Puzzle

## 1. Mục tiêu
Thuật toán tìm kiếm là một trong những thuật toán nền tảng và cốt lõi trong lĩnh vực trí tuệ nhân tạo.
Để củng cố và vận dụng linh hoạt những kiến thức đã học. Với yêu cầu, xây dụng một chương trình giải bài toán 8-Puzzle.
Các mục tiêu đề ra:
Xây dựng một chương trình đầy đủ thuật toán

## 2. Nội dung
**Để giải quyết bài toán tìm kiếm cần xác định những yếu tố sau.**
- Không gian trạng thái: Vị trí các ô số trong bảng 3*3
- Các hành động: di chuyển ô trống: lên, xuống, trái, phải
- Trạng thái xuất phát: một trạng thái hợp lệ
- Trạng thái mục tiêu: [[1,2,3],[4,5,6],[7,8,0]]
- Chi phí: mỗi hành động có giá thành = 1
### 2.1. Các thuật toán tìm kiếm không có thông tin
- 2.1.1. BFS
![alt text](BFS.gif)
- 2.1.2. DFS
![alt text](DFS.gif)
- 2.1.3. UCS
![alt text](UCS.gif)
- 2.1.4. IDS
![alt text](IDS.gif)
- So sánh hiệu suất về thời gian:
![alt text](image.png)
### 2.2. Các thuật toán tìm kiếm  có thông tin
- 2.2.1. Simple hill climbing

- 2.2.2. Stochastic hill climbing

- 2.2.3. Steepest Ascent hill climbing

- 2.2.4. Beam Search

- 2.2.5. Generate Seach

### 2.3. Các thuật toán tìm kiếm cục bộ
- 2.3.1. Greedy

- 2.3.2. A*

- 2.3.3. IDA*

### 2.4. Các thuật toán tìm kiếm trong môi trường phức tạp
- 2.4.1. Non-Observe

- 2.4.2. Partial-Observe

- 2.4.3. AndOr

### 2.5. Các thuật toán tìm kiếm trong môi trường ràng buộc
- 2.5.1. Checked

- 2.5.2. BackTracking

- 2.5.3. AC-3

### 2.6. Q-Learning


## 3. Kết luận
Dự án đã thử nghiệm và so sánh hiệu suất của các thuật toán tìm kiếm không có thông tin và có thông tin trên trò chơi 8 ô chữ. Kết quả cho thấy thuật toán **A*** mang lại hiệu suất tốt nhất với thời gian trung bình 0.8 giây. Các thuật toán khác cũng cho thấy tiềm năng trong các trường hợp cụ thể, đặc biệt khi dữ liệu đã được sắp xếp hoặc có thông tin heuristic hỗ trợ. Dự án có thể được mở rộng bằng cách áp dụng thêm các thuật toán nâng cao hoặc tối ưu hóa hiệu suất trên các tập dữ liệu lớn hơn.
