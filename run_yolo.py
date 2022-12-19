import os
import subprocess 
import runpy
import config as config

def run_rdd(source_file_path, detection_mode = None):

    current_path = os.path.dirname(__file__) 
    #print(current_path)
    

    path_to_Yolo_folder = f'{current_path}\\yolov7'

    weights = config.weights
    imgagesize = config.imgagesize
    confidence = config.confidence

    detect_file_path = f'{path_to_Yolo_folder}\detect.py'
    

    if detection_mode == 'Live mode':
        source_file_path = 0
    os.chdir(path_to_Yolo_folder)
    command = f'python "{detect_file_path}" --weights "{weights}"  --conf {confidence} --source "{source_file_path}" --save-txt'#f'python "{detect_file_path}" --weights "{weights}" --img {imgagesize} --conf {confidence} --source "{source_file_path}" --save-txt --project RDD --view-img'
    #print("python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source 1.jpg")
    print(command)
    #os.system("python detect.py --weights yolov7.pt --conf 0.25 --img-size 640 --source 1.jpg")
    os.system(command)

#run_rdd(r"C:\Users\tobia\Documents\GitHub\Road-Damage-Detection\Dashboard\1.jpg")