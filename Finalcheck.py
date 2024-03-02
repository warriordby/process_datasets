from scipy.io import loadmat


mat_file_path = r"C:\Users\86156\Desktop\program\Git\test\DUTLF-FS\TestSet\FS(mat)\0018.mat"
mat_data = loadmat(mat_file_path)

for key, value in mat_data.items():
    if '__' not in key: 
        print(f"Key: {key}")
        print(f"Value: {value.shape}\n")

from PIL import Image
import numpy as np

first_image = mat_data['images'][9]
first_image = Image.fromarray(np.uint8(first_image))
image_file_path = r'C:\Users\86156\Desktop\program\Git\test.jpg'
first_image.save(image_file_path)
