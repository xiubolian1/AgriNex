import json
import os

import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from ImageProcessing.classification.unet_model import unet as create_model


def pred(img_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"using {device} device.")
    num_classes = 4
    img_size = 512
    data_transform = transforms.Compose(
        [transforms.Resize(int(img_size * 1.14)),
         transforms.CenterCrop(img_size),
         transforms.ToTensor(),
         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    img = Image.open(img_path)
    # [N, C, H, W]
    img = data_transform(img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)


    # create model
    model = create_model(num_classes=num_classes).to(device)
    # load model weights
    model_weight_path = r"C:\Users\xbla\Desktop\Computer_design\ImageProcessing\classification\bestmodel.pth"
    model.load_state_dict(torch.load(model_weight_path, map_location=device))
    model.eval()
    with torch.no_grad():
        # predict class
        output = torch.squeeze(model(img.to(device))).cpu()
        predict = torch.softmax(output, dim=0)
        predict_cla = torch.argmax(predict).numpy()

    class_prob = predict[predict_cla].numpy()
    return class_prob


if __name__ == "__main__":
    img_path = r"C:\Users\xbla\Desktop\flask_potato_class22\uploads\20240312221459.jpg"
    class_prob = pred(img_path)

    print( class_prob)
