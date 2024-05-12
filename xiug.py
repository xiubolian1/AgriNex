from PIL import Image

# 打开图像
image = Image.open(r"C:\Users\xbla\Desktop\Computer_design\static\img\header.png")

# 设置新的大小
new_size = (1450, 760)  # 设置新的宽度和高度

# 修改图像大小
resized_image = image.resize(new_size)

# 保存修改后的图像
resized_image.save(r"C:\Users\xbla\Desktop\Computer_design\static\img\header.png")