# ----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
# ----------------------------------------------------#
import time
import os
import cv2
import numpy as np
from PIL import Image
from ImageProcessing.classification.unet import Unet
from ImageProcessing.classification.unet_way import *
from flask import Blueprint, request, render_template, session, send_from_directory, jsonify


def pred_1(img_path, name):
    mode = "predict"

    count = True
    name_classes = ["background", "Rust", "curl", "slug"]
    dir_save_path = r"C:\Users\xbla\Desktop\Computer_design\uploads"

    unet = Unet()
    img = img_path

    image = Image.open(img)
    img_name = os.path.splitext(name)[0] + '_out.jpg'
    image, pred_name = unet.detect_image(image, count=count, name_classes=name_classes)
    if not os.path.exists(dir_save_path):
        os.makedirs(dir_save_path)
    image.save(os.path.join(dir_save_path, img_name))
    return img_name, pred_name


if __name__ == "__main__":
    img_path = r"D:\something\Code\run\net\分割\unet\VOCdevkit\VOC2007\JPEGImages\randomGaussian_0_randomGaussian_slug_73_0.jpg"
    out_path, pred_name = pred_1(img_path)

    print(out_path, pred_name)
