import os
from PIL import Image
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

def split_image_with_overlap(image_path, rows, cols, overlap_percent):
    """
    将图像拆分为带有重叠的多块。

    Args:
        image_path (str): 输入图像文件的路径
        rows (int): 行数
        cols (int): 列数
        overlap_percent (float): 重叠的百分比（0-100）
    
    Returns:
        list: 包含拆分图像块的列表
    """
    img = Image.open(image_path)
    img_width, img_height = img.size
    tile_width = img_width // cols
    tile_height = img_height // rows
    overlap_x = int(tile_width * (overlap_percent / 100))
    overlap_y = int(tile_height * (overlap_percent / 100))
    tiles = []

    for row in range(rows):
        for col in range(cols):
            left = max(col * tile_width - overlap_x, 0)
            upper = max(row * tile_height - overlap_y, 0)
            right = min((col + 1) * tile_width + overlap_x, img_width)
            lower = min((row + 1) * tile_height + overlap_y, img_height)
            tile = img.crop((left, upper, right, lower))
            tiles.append(tile)

    return tiles

def combine_images_with_overlap(tiles, rows, cols, overlap_percent, img_width, img_height):
    """
    将带有重叠的多块图像合并成一个图像。

    Args:
        tiles (list): 包含图像块的列表
        rows (int): 行数
        cols (int): 列数
        overlap_percent (float): 重叠的百分比（0-100）
        img_width (int): 原图宽度
        img_height (int): 原图高度
    
    Returns:
        Image: 合并后的图像
    """
    tile_width = img_width // cols
    tile_height = img_height // rows
    overlap_x = int(tile_width * (overlap_percent / 100))
    overlap_y = int(tile_height * (overlap_percent / 100))
    combined_img = Image.new('RGB', (img_width, img_height))

    for row in range(rows):
        for col in range(cols):
            left = col * tile_width
            upper = row * tile_height
            tile = tiles[row * cols + col]
            crop_left = overlap_x if col != 0 else 0
            crop_upper = overlap_y if row != 0 else 0
            crop_right = tile.width - overlap_x if col != cols - 1 else tile.width
            crop_lower = tile.height - overlap_y if row != rows - 1 else tile.height
            cropped_tile = tile.crop((crop_left, crop_upper, crop_right, crop_lower))
            combined_img.paste(cropped_tile, (left, upper))

    return combined_img

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully.")
    except Exception as e:
        print(f"Failed to create folder '{folder_path}'. Error: {e}")


if __name__ == "__main__":
    # 用户指定文件夹GUI
    # app = QApplication(sys.argv)
    
    # # 创建一个无界面的窗口
    # widget = QWidget()
    # widget.setWindowTitle('Select Folder')
    
    # # 选择输入文件夹      
    # # 弹出文件夹选择对话框
    # filepath_in = QFileDialog.getExistingDirectory(widget, 'Select Input Folder')
        
    # # 输出选择的文件夹路径
    # if filepath_in:
    #     print(f'Selected folder: {filepath_in}')
    # else:
    #     print('No folder selected')
    
    # 图片分割参数
    rows_split = 7
    cols_split = 10
    overlap_percent = 0
    
    # 代码指定输入输出文件夹
    filepath_in = r"G:\CV\hekou yihdao"
    filepath_out = filepath_in + " split"
    file_ext = r".jpg"
    new_folder = create_folder(filepath_out) 
    # filenames=os.listdir(filepath_in)
    # print(filenames,len(filenames))
    
    # 分割文件夹中图片
    for filepath,dirnames,filenames in os.walk(filepath_in):
        for filename in filenames:
            temp_filename = os.path.join(filepath,filename)
            # with Image.open(temp_filename) as img:
            #     print(temp_filename)
            #     print(img.size)
            temp_tiles = split_image_with_overlap(temp_filename, rows_split, cols_split, overlap_percent)
            # print(temp_tiles)
            file_without_ext = os.path.splitext(filename)[0]
            new_folder = create_folder(filepath_out + "/" + file_without_ext)
            for i, tile in enumerate(temp_tiles):
                # print(i, filepath_out + filename[:-4] + f'_tile_{i}.jpg')
                tile.save(filepath_out + "/" + file_without_ext + f'_tile_{i}' + file_ext)
                tile.save(filepath_out + "/" + file_without_ext + "/" + file_without_ext + f'_tile_{i}' + file_ext)
    
    # 合并文件夹中图片
    new_folder = create_folder(filepath_in + "/combine")        
    for filepath,dirnames,filenames in os.walk(filepath_out):
        if filepath == filepath_out:
            continue
        else:
            print(filepath)
            file_without_ext = os.path.split(filepath)[1]
            imgfile_old = filepath_in + "/" + file_without_ext + file_ext
            # print(imgfile_old)
            img = Image.open(imgfile_old)
            img_width, img_height = img.size
            tiles = [Image.open(filepath + "/" + file_without_ext + f'_tile_{i}' + file_ext) for i in range(rows_split * cols_split)]
            combined_img = combine_images_with_overlap(tiles, rows_split, cols_split, overlap_percent, img_width, img_height)
            combined_img.save(filepath_in + "/combine/"+ file_without_ext + file_ext)