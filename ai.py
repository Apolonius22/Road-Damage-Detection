import matplotlib.pyplot as plt
import torch
import cv2
import yaml
from torchvision import transforms
import numpy as np

from yolov7.utils.datasets import letterbox
from yolov7.utils.general import non_max_suppression_mask_conf

#from yolov7.detectron2.modeling.poolers import ROIPooler
#from yolov7.detectron2.structures import Boxes
#from yolov7.detectron2.utils.memory import retry_if_cuda_oom
#from yolov7.detectron2.layers import paste_masks_in_image