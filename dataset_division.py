""""
@author: dengbuyin@HuNan University
@software: Visual Studio Code
@file: dataset_division.py
@time: 2024/3/1 

"""


import os
from scipy.io import savemat
from PIL import Image
import numpy as np


Datasets_name=("DUTLF-FS\TestSet", "DUTLF-FS\TrainingSet", "LFSD", "Lytro Illum", "HFUT-Lytro")
FS_dir=('focalstack', 'Focal stack', 'Focal_stack','Focus_stack')
AF_dir=('allfocus', 'All-in-focus', 'all-in-focus')
GT_dir=('GT', 'GT(all-in-focus)', 'GT(center-view)')
CV_dir=('Center view' , 'Center-view')

#可调整图片的目标类型和原类型筛选
file_format=('png', 'PNG', 'jpg', 'JPEG', 'bmp')
target_format='JPEG'


def conversion_to_mat(current_root_path, target_path):      
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    groups = {}
    for file in os.listdir(current_root_path):
        file_path=os.path.join(current_root_path, file)
        if os.path.isdir(file_path):
            conversion_to_mat(file_path, target_path)
            return
        elif '__refocus_' in file :
            group_id = file.split('__')[0]  # 获取组ID
            if group_id not in groups:
                groups[group_id] = []
            groups[group_id].append(file)

    #他是一个字典套List，group包含【group1，group2，。。】。这其中group1包含【1__refocus_00.jpg,..】
    #        
    for group_id, filenames in groups.items():  #group_id父级迭代，filenames子迭代
        images_data = []
        for filename in filenames:
            img_path = os.path.join(current_root_path, filename)
            img = Image.open(img_path)
            img_data = np.array(img)
            images_data.append(img_data)
        
        mat_filepath = os.path.join(target_path, f"{group_id}.mat")
        savemat(mat_filepath, {'images': images_data})
    print(f'convert {source_path} to {target_path}')
    return len(os.listdir(target_path))

def convert_to_jpg(current_root_path, target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # 获取输入路径下的所有文件
    for file_name in os.listdir(current_root_path):
        # 拼接完整的文件路径
        file_path = os.path.join(current_root_path, file_name)
        # 检查文件是否是指定的图片格式
        if file_name.lower().endswith(file_format) and not os.path.isdir(file_path):
            try:
                # 打开图片文件
                img = Image.open(file_path)
                # 构建输出文件路径
                output_file_path = os.path.join(target_path, os.path.splitext(file_name)[0] + '.jpg')
                # 将图片保存为JPEG格式
                img.convert('RGB').save(output_file_path, format=target_format)
                print(f"Converted: {file_path} -> {output_file_path}")
            except Exception as e:
                print(f"Error converting {file_path}: {str(e)}")
        if os.path.isdir(file_path):
            convert_to_jpg(file_path, target_path)


#寻找到目标文件夹路径，拆分AF和CV
def process_path(current_root_path, target_path):
    for current_filename in os.listdir(current_root_path):
        current_filepath = os.path.join(current_root_path, current_filename)
        if not os.path.isdir(current_filepath):
            continue
        else:
            if current_filename in AF_dir:
                convert_to_jpg(current_filepath, os.path.join(target_path, 'AF'))
                process_folder(current_root_path, target_path)
            elif current_filename in CV_dir:  
                convert_to_jpg(current_filepath, os.path.join(target_path, 'CV'))
                process_folder(current_root_path, target_path, IS_AF=False)
            else:
                process_path(current_filepath, target_path)

#对对GT、FS文件夹分别处理
def process_folder(current_root_path, target_path, IS_AF=True):
        f=os.listdir(current_root_path)
        for current_filename in f:
            current_filepath = os.path.join(current_root_path, current_filename)
            if not os.path.isdir(current_filepath):
                continue
            else:
                if current_filename in FS_dir:
                    convert_to_jpg(current_filepath, os.path.join(target_path, 'FS'))
                    conversion_to_mat(os.path.join(target_path, 'FS'), os.path.join(target_path, 'FS(mat)'))
                elif current_filename in GT_dir:
                    if not IS_AF:
                        convert_to_jpg(current_filepath, os.path.join(target_path, 'GT(center-view)'))
                    else:
                        convert_to_jpg(current_filepath, os.path.join(target_path, 'GT(all-in-focus)'))
                else:
                    continue

if __name__=='__main__':

    source_root_path = r"C:\Users\86156\Desktop\program\Git"
    target_root_path= r'C:\Users\86156\Desktop\program\Git\test'

    for dataset_name in Datasets_name:
        source_path=os.path.join(source_root_path, dataset_name)
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"路径不存在: {source_path}")
        
        target_path=os.path.join(target_root_path, dataset_name)
        if not os.path.exists(target_path):
            os.makedirs(target_path, exist_ok=True)
            
        process_path(source_path, target_path)
