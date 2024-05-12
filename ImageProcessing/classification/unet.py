# import torch
# import torch.nn as nn
#
# from nets.resnet import resnet50
# from nets.vgg import VGG16
#
#
# class unetUp(nn.Module):
#     def __init__(self, in_size, out_size):
#         super(unetUp, self).__init__()
#         self.conv1 = nn.Conv2d(in_size, out_size, kernel_size=3, padding = 1)
#         self.conv2 = nn.Conv2d(out_size, out_size, kernel_size=3, padding = 1)
#         self.up = nn.UpsamplingBilinear2d(scale_factor=2)
#         self.relu = nn.ReLU(inplace=True)
#
#     def forward(self, inputs1, inputs2):
#         outputs = torch.cat([inputs1, self.up(inputs2)], 1)
#         outputs = self.conv1(outputs)
#         outputs = self.relu(outputs)
#         outputs = self.conv2(outputs)
#         outputs = self.relu(outputs)
#         return outputs
#
#
# class Unet(nn.Module):
#     def __init__(self, num_classes = 21, pretrained = False, backbone = 'vgg'):
#         super(Unet, self).__init__()
#         if backbone == 'vgg':
#             self.vgg = VGG16(pretrained = pretrained)
#             in_filters = [192, 384, 768, 1024]
#         elif backbone == "resnet50":
#             self.resnet = resnet50(pretrained = pretrained)
#             in_filters = [192, 512, 1024, 3072]
#         else:
#             raise ValueError('Unsupported backbone - `{}`, Use vgg, resnet50.'.format(backbone))
#         out_filters = [64, 128, 256, 512]
#
#         # upsampling
#         # 64,64,512
#         self.up_concat4 = unetUp(in_filters[3], out_filters[3])
#         # 128,128,256
#         self.up_concat3 = unetUp(in_filters[2], out_filters[2])
#         # 256,256,128
#         self.up_concat2 = unetUp(in_filters[1], out_filters[1])
#         # 512,512,64
#         self.up_concat1 = unetUp(in_filters[0], out_filters[0])
#
#         if backbone == 'resnet50':
#             self.up_conv = nn.Sequential(
#                 nn.UpsamplingBilinear2d(scale_factor = 2),
#                 nn.Conv2d(out_filters[0], out_filters[0], kernel_size = 3, padding = 1),
#                 nn.ReLU(),
#                 nn.Conv2d(out_filters[0], out_filters[0], kernel_size = 3, padding = 1),
#                 nn.ReLU(),
#             )
#         else:
#             self.up_conv = None
#
#         self.final = nn.Conv2d(out_filters[0], num_classes, 1)
#
#         self.backbone = backbone
#
#     def forward(self, inputs):
#         if self.backbone == "vgg":
#             [feat1, feat2, feat3, feat4, feat5] = self.vgg.forward(inputs)
#         elif self.backbone == "resnet50":
#             [feat1, feat2, feat3, feat4, feat5] = self.resnet.forward(inputs)
#
#         up4 = self.up_concat4(feat4, feat5)
#         up3 = self.up_concat3(feat3, up4)
#         up2 = self.up_concat2(feat2, up3)
#         up1 = self.up_concat1(feat1, up2)
#
#         if self.up_conv != None:
#             up1 = self.up_conv(up1)
#
#         final = self.final(up1)
#
#         return final
#
#     def freeze_backbone(self):
#         if self.backbone == "vgg":
#             for param in self.vgg.parameters():
#                 param.requires_grad = False
#         elif self.backbone == "resnet50":
#             for param in self.resnet.parameters():
#                 param.requires_grad = False
#
#     def unfreeze_backbone(self):
#         if self.backbone == "vgg":
#             for param in self.vgg.parameters():
#                 param.requires_grad = True
#         elif self.backbone == "resnet50":
#             for param in self.resnet.parameters():
#                 param.requires_grad = True

from typing import Dict  # 导入 Dict 类型用于指定函数返回类型
import torch  # 导入 PyTorch 库
import torch.nn as nn  # 导入 PyTorch 的神经网络模块
import torch.nn.functional as F  # 导入 PyTorch 的函数模块


class DoubleConv(nn.Sequential):
    def __init__(self, in_channels, out_channels, mid_channels=None):
        """
        定义一个双卷积块的辅助类。

        Args:
            in_channels (int): 输入通道数。
            out_channels (int): 输出通道数。
            mid_channels (int, optional): 中间通道数。默认为 None。
        """
        if mid_channels is None:
            mid_channels = out_channels
        super(DoubleConv, self).__init__(
            nn.Conv2d(in_channels, mid_channels, kernel_size=3, padding=1, bias=False),  # 第一个卷积层
            nn.BatchNorm2d(mid_channels),  # 批标准化层
            nn.ReLU(inplace=True),  # ReLU 激活函数
            nn.Conv2d(mid_channels, out_channels, kernel_size=3, padding=1, bias=False),  # 第二个卷积层
            nn.BatchNorm2d(out_channels),  # 批标准化层
            nn.ReLU(inplace=True)  # ReLU 激活函数
        )


class Down(nn.Sequential):
    def __init__(self, in_channels, out_channels):
        """
        定义一个下采样块的辅助类。

        Args:
            in_channels (int): 输入通道数。
            out_channels (int): 输出通道数。
        """
        super(Down, self).__init__(
            nn.MaxPool2d(2, stride=2),  # 最大池化层进行下采样
            DoubleConv(in_channels, out_channels)  # 双卷积块
        )


class Up(nn.Module):
    def __init__(self, in_channels, out_channels, bilinear=True):
        """
        定义一个上采样块的辅助类。

        Args:
            in_channels (int): 输入通道数。
            out_channels (int): 输出通道数。
            bilinear (bool, optional): 是否使用双线性插值进行上采样。默认为 True。
        """
        super(Up, self).__init__()
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)  # 双线性插值上采样
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)  # 双卷积块
        else:
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)  # 转置卷积进行上采样
            self.conv = DoubleConv(in_channels, out_channels)  # 双卷积块

    def forward(self, x1: torch.Tensor, x2: torch.Tensor) -> torch.Tensor:
        """
        上采样块的前向传播函数。

        Args:
            x1 (torch.Tensor): 来自低分辨率路径的输入张量。
            x2 (torch.Tensor): 来自跳跃连接的输入张量。

        Returns:
            torch.Tensor: 输出张量。
        """
        x1 = self.up(x1)
        # [N, C, H, W]
        diff_y = x2.size()[2] - x1.size()[2]
        diff_x = x2.size()[3] - x1.size()[3]

        # padding_left, padding_right, padding_top, padding_bottom
        x1 = F.pad(x1, [diff_x // 2, diff_x - diff_x // 2,
                        diff_y // 2, diff_y - diff_y // 2])

        x = torch.cat([x2, x1], dim=1)  # 在通道维度上拼接张量
        x = self.conv(x)  # 经过双卷积块
        return x


class OutConv(nn.Sequential):
    def __init__(self, in_channels, num_classes):
        """
        定义最终输出卷积层的辅助类。

        Args:
            in_channels (int): 输入通道数。
            num_classes (int): 输出类别数。
        """
        super(OutConv, self).__init__(
            nn.Conv2d(in_channels, num_classes, kernel_size=1)  # 1x1 卷积层
        )


class Unet(nn.Module):
    def __init__(self,
                 in_channels: int = 3,
                 num_classes: int = 4,
                 bilinear: bool = True,
                 base_c: int = 64):
        """
        U-Net 模型架构。

        Args:
            in_channels (int, optional): 输入通道数。默认为 3。
            num_classes (int, optional): 输出类别数。默认为 4。
            bilinear (bool, optional): 是否使用双线性插值进行上采样。默认为 True。
            base_c (int, optional): 基础通道数。默认为 64。
        """
        super(Unet, self).__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.bilinear = bilinear

        self.in_conv = DoubleConv(in_channels, base_c)  # 输入的双卷积块
        self.down1 = Down(base_c, base_c * 2)  # 下采样层 1
        self.down2 = Down(base_c * 2, base_c * 4)  # 下采样层 2
        self.down3 = Down(base_c * 4, base_c * 8)  # 下采样层 3
        factor = 2 if bilinear else 1
        self.down4 = Down(base_c * 8, base_c * 16 // factor)  # 下采样层 4
        self.up1 = Up(base_c * 16, base_c * 8 // factor, bilinear)  # 上采样层 1
        self.up2 = Up(base_c * 8, base_c * 4 // factor, bilinear)  # 上采样层 2
        self.up3 = Up(base_c * 4, base_c * 2 // factor, bilinear)  # 上采样层 3
        self.up4 = Up(base_c * 2, base_c, bilinear)  # 上采样层 4
        self.out_conv = OutConv(base_c, num_classes)  # 输出卷积层

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        U-Net 模型的前向传播函数。

        Args:
            x (torch.Tensor): 输入张量。

        Returns:
            Dict[str, torch.Tensor]: 包含输出 logits 的字典。
        """
        x1 = self.in_conv(x)  # 输入双卷积块
        x2 = self.down1(x1)  # 下采样层 1
        x3 = self.down2(x2)  # 下采样层 2
        x4 = self.down3(x3)  # 下采样层 3
        x5 = self.down4(x4)  # 下采样层 4
        x = self.up1(x5, x4)  # 上采样层 1
        x = self.up2(x, x3)  # 上采样层 2
        x = self.up3(x, x2)  # 上采样层 3
        x = self.up4(x, x1)  # 上采样层 4
        logits = self.out_conv(x)  # 输出卷积层

        return logits

    def freeze_backbone(self):
        """
        冻结 U-Net 模型的主干网络参数。
        """
        for param in self.parameters():
            param.requires_grad = False

    def unfreeze_backbone(self):
        """
        解冻 U-Net 模型的主干网络参数。
        """
        for param in self.parameters():
            param.requires_grad = True
