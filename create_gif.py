from PIL import Image
import os

# Đường dẫn thư mục nguồn và đích
source_folder = "ga"
output_folder = "anh_gif"
output_path = os.path.join(output_folder, "ga2.gif")

# Tạo thư mục lưu GIF nếu chưa có
os.makedirs(output_folder, exist_ok=True)

# Lấy danh sách ảnh
image_files = sorted([f for f in os.listdir(source_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
images = [Image.open(os.path.join(source_folder, f)) for f in image_files]

# Lưu GIF
images[0].save(output_path, save_all=True, append_images=images[1:], duration=300, loop=0)
