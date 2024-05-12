import torch  # 导入 PyTorch 库
from torch import nn  # 导入 PyTorch 中的神经网络模块
import torch  # 再次导入 PyTorch 库，此处可能是多余的
import torchvision  # 导入 torchvision 库，用于图像处理任务
from torch import nn  # 再次导入 PyTorch 中的神经网络模块，可能是多余的
from torch.autograd import Variable  # 导入 PyTorch 中的自动求导模块
from torch.utils.data import DataLoader  # 导入 PyTorch 中用于数据加载的模块
from torchvision import transforms  # 导入 torchvision 中的数据转换模块
from torchvision.utils import save_image  # 导入 torchvision 中用于保存图像的模块
import torch.nn.functional as F  # 导入 PyTorch 中的函数式接口模块，并简化为 F
import os  # 导入操作系统相关的模块
import matplotlib.pyplot as plt  # 导入用于绘图的模块，并简化为 plt
from utils import *  # 从自定义模块 utils 中导入所有内容
from nets.DJHY import WJHY  # 从自定义模块 nets.DJHY 中导入模块 WJHY

# __all__ = ['UNext']  # 定义可以被导出的模块成员，可能是用于模块导入的特殊标记

import timm  # 导入图像模型库 timm
from timm.models.layers import DropPath, to_2tuple, trunc_normal_  # 从 timm 中导入一些模块
import types  # 导入 types 模块，用于操作类型相关的工具
import math  # 导入数学相关的模块
from abc import ABCMeta, abstractmethod  # 导入抽象基类相关的模块
from mmcv.cnn import ConvModule  # 从 mmcv.cnn 模块导入 ConvModule 类
import pdb  # 导入 Python 调试器 pdb 模块
from attention import AttentionLePE, BiLevelRoutingAttention  # 从自定义模块 attention 中导入一些注意力机制相关的模块


# 定义一个函数，用于创建 1x1 卷积
def conv1x1(in_planes: int, out_planes: int, stride: int = 1) -> nn.Conv2d:
    """1x1 卷积"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=1, bias=False)


# 定义一个类，实现 Shift-MLP 模块
class shiftmlp(nn.Module):
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0., shift_size=5):
        super().__init__()  # 调用父类的构造函数
        out_features = out_features or in_features  # 如果输出特征数未指定，则与输入特征数相同
        hidden_features = hidden_features or in_features  # 如果隐藏特征数未指定，则与输入特征数相同
        self.dim = in_features  # 输入特征的维度
        self.fc1 = nn.Linear(in_features, hidden_features)  # 全连接层，用于特征变换
        self.dwconv = DWConv(hidden_features)  # 深度可分离卷积层
        self.act = act_layer()  # 激活函数
        self.fc2 = nn.Linear(hidden_features, out_features)  # 全连接层，用于特征变换
        self.drop = nn.Dropout(drop)  # Dropout 层，用于防止过拟合

        self.shift_size = shift_size  # 平移尺寸
        self.pad = shift_size // 2  # 填充大小，用于平移操作

        self.apply(self._init_weights)  # 对模型的参数进行初始化

    def _init_weights(self, m):  # 定义参数初始化函数
        if isinstance(m, nn.Linear):  # 如果是线性层
            trunc_normal_(m.weight, std=.02)  # 对权重进行截断正态分布初始化
            if isinstance(m, nn.Linear) and m.bias is not None:  # 如果存在偏置项
                nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
        elif isinstance(m, nn.LayerNorm):  # 如果是 LayerNorm 层
            nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
            nn.init.constant_(m.weight, 1.0)  # 初始化权重为常数
        elif isinstance(m, nn.Conv2d):  # 如果是二维卷积层
            fan_out = m.kernel_size[0] * m.kernel_size[1] * m.out_channels  # 计算卷积核参数数量
            fan_out //= m.groups  # 根据分组数调整参数数量
            m.weight.data.normal_(0, math.sqrt(2.0 / fan_out))  # 对权重进行截断正态分布初始化
            if m.bias is not None:  # 如果存在偏置项
                m.bias.data.zero_()  # 初始化偏置为零

    def forward(self, x, H, W):  # 前向传播函数
        B, N, C = x.shape  # 获取输入张量的形状

        # 将输入张量转换成二维形状
        xn = x.transpose(1, 2).view(B, C, H, W).contiguous()
        # 对输入张量进行填充
        xn = F.pad(xn, (self.pad, self.pad, self.pad, self.pad), "constant", 0)
        # 将填充后的张量分成多个小块
        xs = torch.chunk(xn, self.shift_size, 1)
        # 对每个小块进行平移操作
        x_shift = [torch.roll(x_c, shift, 2) for x_c, shift in zip(xs, range(-self.pad, self.pad + 1))]
        # 将平移后的小块拼接起来
        x_cat = torch.cat(x_shift, 1)
        # 裁剪拼接后的张量，去除填充部分
        x_cat = torch.narrow(x_cat, 2, self.pad, H)
        x_s = torch.narrow(x_cat, 3, self.pad, W)

        # 将裁剪后的张量转换成二维形状
        x_s = x_s.reshape(B, C, H * W).contiguous()
        x_shift_r = x_s.transpose(1, 2)

        # 通过全连接层进行特征变换
        x = self.fc1(x_shift_r)

        # 进行深度可分离卷积
        x = self.dwconv(x, H, W)
        x = self.act(x)
        x = self.drop(x)

        # 再次进行平移操作
        xn = x.transpose(1, 2).view(B, C, H, W).contiguous()
        xn = F.pad(xn, (self.pad, self.pad, self.pad, self.pad), "constant", 0)
        xs = torch.chunk(xn, self.shift_size, 1)
        x_shift = [torch.roll(x_c, shift, 3) for x_c, shift in zip(xs, range(-self.pad, self.pad + 1))]
        x_cat = torch.cat(x_shift, 1)
        x_cat = torch.narrow(x_cat, 2, self.pad, H)
        x_s = torch.narrow(x_cat, 3, self.pad, W)
        x_s = x_s.reshape(B, C, H * W).contiguous()
        x_shift_c = x_s.transpose(1, 2)

        # 再次通过全连接层进行特征变换
        x = self.fc2(x_shift_c)
        x = self.drop(x)
        return x


# 定义 Shift-MLP 模块，用于对输入特征进行变换

class shiftedBlock(nn.Module):
    def __init__(self, dim, num_heads=4, mlp_ratio=2., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm, sr_ratio=1, side_dwconv=5):
        super().__init__()  # 调用父类的构造函数

        self.norm2 = norm_layer(dim)  # 归一化层
        mlp_hidden_dim = int(dim * mlp_ratio)  # 计算 MLP 隐藏层的维度
        self.mlp = shiftmlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer,
                            drop=drop)  # Shift-MLP 模块

        # 将原始的自注意力机制替换为双层路径自注意力机制
        self.attention = BiLevelRoutingAttention(dim=dim, num_heads=num_heads, qk_dim=None, qk_scale=qk_scale, topk=4,
                                                 param_routing=False, diff_routing=False)

        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()  # DropPath 层，用于随机丢弃路径

        self.apply(self._init_weights)  # 对模型的参数进行初始化

    def _init_weights(self, m):  # 定义参数初始化函数
        if isinstance(m, nn.Linear):  # 如果是线性层
            trunc_normal_(m.weight, std=.02)  # 对权重进行截断正态分布初始化
            if isinstance(m, nn.Linear) and m.bias is not None:  # 如果存在偏置项
                nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
        elif isinstance(m, nn.LayerNorm):  # 如果是 LayerNorm 层
            nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
            nn.init.constant_(m.weight, 1.0)  # 初始化权重为常数
        elif isinstance(m, nn.Conv2d):  # 如果是二维卷积层
            fan_out = m.kernel_size[0] * m.kernel_size[1] * m.out_channels  # 计算卷积核参数数量
            fan_out //= m.groups  # 根据分组数调整参数数量
            m.weight.data.normal_(0, math.sqrt(2.0 / fan_out))  # 对权重进行截断正态分布初始化
            if m.bias is not None:  # 如果存在偏置项
                m.bias.data.zero_()  # 初始化偏置为零

    def forward(self, x, H, W):  # 前向传播函数
        B, N, C = x.shape  # 获取输入张量的形状
        x = x.view(B, H, W, C)  # 将输入张量转换为四维形状
        x = self.attention(x)  # 使用双层路径自注意力机制进行特征提取，输入输出形状为 (B, H, W, C)
        x = x.view(B, N, C)  # 将输出张量重新转换为三维形状
        x = x + self.drop_path(self.mlp(self.norm2(x), H, W))  # 使用 DropPath 层和 Shift-MLP 进行特征融合
        return x


# 定义深度可分离卷积模块
class DWConv(nn.Module):
    def __init__(self, dim=768):
        super(DWConv, self).__init__()  # 调用父类的构造函数
        self.dwconv = nn.Conv2d(dim, dim, 3, 1, 1, bias=True, groups=dim)  # 定义深度可分离卷积层

    def forward(self, x, H, W):  # 前向传播函数
        B, N, C = x.shape  # 获取输入张量的形状
        x = x.transpose(1, 2).view(B, C, H, W)  # 将输入张量转换为四维形状
        x = self.dwconv(x)  # 应用深度可分离卷积
        x = x.flatten(2).transpose(1, 2)  # 将输出张量转换为二维形状
        return x


# 定义重叠补丁嵌入模块
class OverlapPatchEmbed(nn.Module):
    """图像到补丁嵌入的转换模块"""

    def __init__(self, img_size=224, patch_size=7, stride=4, in_chans=3, embed_dim=768):
        super().__init__()  # 调用父类的构造函数
        img_size = to_2tuple(img_size)  # 将图像大小转换为二元组
        patch_size = to_2tuple(patch_size)  # 将补丁大小转换为二元组

        self.img_size = img_size  # 图像大小
        self.patch_size = patch_size  # 补丁大小
        self.H, self.W = img_size[0] // patch_size[0], img_size[1] // patch_size[1]  # 计算嵌入的补丁数量
        self.num_patches = self.H * self.W  # 总补丁数量
        # 定义卷积层，用于将输入图像转换为补丁嵌入
        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=stride,
                              padding=(patch_size[0] // 2, patch_size[1] // 2))
        self.norm = nn.LayerNorm(embed_dim)  # 归一化层

        self.apply(self._init_weights)  # 对模型的参数进行初始化

    def _init_weights(self, m):  # 定义参数初始化函数
        if isinstance(m, nn.Linear):  # 如果是线性层
            trunc_normal_(m.weight, std=.02)  # 对权重进行截断正态分布初始化
            if isinstance(m, nn.Linear) and m.bias is not None:  # 如果存在偏置项
                nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
        elif isinstance(m, nn.LayerNorm):  # 如果是 LayerNorm 层
            nn.init.constant_(m.bias, 0)  # 初始化偏置为常数
            nn.init.constant_(m.weight, 1.0)  # 初始化权重为常数
        elif isinstance(m, nn.Conv2d):  # 如果是二维卷积层
            fan_out = m.kernel_size[0] * m.kernel_size[1] * m.out_channels  # 计算卷积核参数数量
            fan_out //= m.groups  # 根据分组数调整参数数量
            m.weight.data.normal_(0, math.sqrt(2.0 / fan_out))  # 对权重进行截断正态分布初始化
            if m.bias is not None:  # 如果存在偏置项
                m.bias.data.zero_()  # 初始化偏置为零

    def forward(self, x):  # 前向传播函数
        x = self.proj(x)  # 应用卷积层，将输入图像转换为补丁嵌入
        _, _, H, W = x.shape  # 获取输出张量的形状
        x = x.flatten(2).transpose(1, 2)  # 将输出张量转换为二维形状
        x = self.norm(x)  # 对补丁嵌入进行归一化
        return x, H, W  # 返回补丁嵌入以及嵌入的高度和宽度


# 导入必要的库
from typing import Dict
import torch
import torch.nn as nn
import torch.nn.functional as F


# 定义双重卷积模块
class DoubleConv(nn.Sequential):
    def __init__(self, in_channels, out_channels, mid_channels=None):
        if mid_channels is None:
            mid_channels = out_channels
        super(DoubleConv, self).__init__(
            nn.Conv2d(in_channels, out_channels, kernel_size=7, padding=3, bias=False),  # 第一个卷积层
        )


# 定义下采样模块
class Down(nn.Sequential):
    def __init__(self, in_channels, out_channels):
        super(Down, self).__init__(
            nn.MaxPool2d(2, stride=2),  # 最大池化层
            DoubleConv(in_channels, out_channels)  # 双重卷积层
        )


# 定义上采样模块
class Up(nn.Module):
    def __init__(self, in_channels, out_channels, bilinear=True):
        super(Up, self).__init__()
        if bilinear:
            self.up = nn.Upsample(scale_factor=2, mode='bilinear', align_corners=True)  # 双线性上采样
            self.conv = DoubleConv(in_channels, out_channels, in_channels // 2)  # 双重卷积层
        else:
            self.up = nn.ConvTranspose2d(in_channels, in_channels // 2, kernel_size=2, stride=2)  # 转置卷积
            self.conv = DoubleConv(in_channels, out_channels)  # 双重卷积层

        self.conv1 = nn.Conv2d(in_channels, in_channels // 2, kernel_size=1)  # 降低通道数的卷积层

    def forward(self, x1: torch.Tensor, x2: torch.Tensor) -> torch.Tensor:
        x1 = self.up(x1)  # 上采样操作
        # 计算两个张量的尺寸差异
        diff_y = x2.size()[2] - x1.size()[2]
        diff_x = x2.size()[3] - x1.size()[3]

        # 对第一个张量进行填充，使其尺寸与第二个张量相同
        x1 = F.pad(x1, [diff_x // 2, diff_x - diff_x // 2, diff_y // 2, diff_y - diff_y // 2])

        x = torch.cat([x2, x1], dim=1)  # 拼接两个张量
        x = self.conv(x)  # 经过双重卷积
        return x


# 定义输出卷积模块
class OutConv(nn.Sequential):
    def __init__(self, in_channels, num_classes):
        super(OutConv, self).__init__(
            nn.Conv2d(in_channels, num_classes, kernel_size=1)  # 一维卷积层
        )


# 定义 UNet 模型
class UNext(nn.Module):
    def __init__(self,
                 img_size=512,
                 embed_dims=[256, 512],
                 num_heads=[8, 2, 4], qkv_bias=False, qk_scale=None, drop_rate=0.,
                 attn_drop_rate=0., drop_path_rate=0., norm_layer=nn.LayerNorm,
                 depths=[1, 1], sr_ratios=[8, 4, 2, 1],
                 in_channels: int = 3,
                 num_classes: int = 2,
                 bilinear: bool = True,
                 base_c: int = 32):
        super(UNext, self).__init__()  # 调用父类的构造函数
        self.in_channels = in_channels  # 输入通道数
        self.num_classes = num_classes  # 类别数量
        self.bilinear = bilinear  # 是否使用双线性插值

        self.in_conv = DoubleConv(in_channels, base_c)  # 输入卷积层
        self.down1 = WJHY(base_c, base_c * 2, factor=2)  # 下采样模块
        self.down2 = WJHY(base_c * 2, base_c * 4, factor=4)  # 下采样模块
        self.down3 = WJHY(base_c * 4, base_c * 8, factor=8)  # 下采样模块

        factor = 2 if bilinear else 1  # 如果使用双线性插值，则设置 factor 为 2，否则设置为 1

        # 上采样模块
        self.up1 = Up(base_c * 16, base_c * 8 // factor, bilinear)
        self.up2 = Up(base_c * 8, base_c * 4 // factor, bilinear)
        self.up3 = Up(base_c * 4, base_c * 2 // factor, bilinear)
        self.up4 = Up(base_c * 2, base_c, bilinear)
        self.out_conv = OutConv(base_c, num_classes)  # 输出卷积层

        dpr = [x.item() for x in torch.linspace(0, drop_path_rate,
                                                sum(depths))]  # 使用 torch.linspace 在 0 和 drop_path_rate
        # 之间生成均匀间隔的数字序列，并转换为列表

        # 定义双层路径自注意力机制模块
        self.block2 = nn.ModuleList([shiftedBlock(
            dim=embed_dims[1], num_heads=num_heads[0], mlp_ratio=1, qkv_bias=qkv_bias, qk_scale=qk_scale,
            drop=drop_rate, attn_drop=attn_drop_rate, drop_path=dpr[0], norm_layer=norm_layer,
            sr_ratio=sr_ratios[0])])

        self.dblock2 = nn.ModuleList([shiftedBlock(
            dim=embed_dims[0], num_heads=num_heads[1], mlp_ratio=1, qkv_bias=qkv_bias, qk_scale=qk_scale,
            drop=drop_rate, attn_drop=attn_drop_rate, drop_path=dpr[0], norm_layer=norm_layer,
            sr_ratio=sr_ratios[0])])

        self.patch_embed4 = OverlapPatchEmbed(img_size=img_size // 8, patch_size=3, stride=2, in_chans=embed_dims[0],
                                              embed_dim=embed_dims[1])

        self.decoder1 = nn.Conv2d(512, 256, 3, stride=1, padding=1)

        self.norm4 = norm_layer(embed_dims[1])
        self.dnorm4 = norm_layer(embed_dims[0])
        self.dbn1 = nn.BatchNorm2d(256)

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        正向传播函数

        Args:
            x (torch.Tensor): 输入张量，形状为 (B, C, H, W)，其中 B 是批量大小，C 是通道数，H 和 W 分别是输入图像的高度和宽度。

        Returns:
            Dict[str, torch.Tensor]: 包含模型输出的字典，其中 'logits' 键对应的值是模型的输出张量，形状为 (B, num_classes, H', W')，
                                    其中 num_classes 是类别数量，H' 和 W' 分别是输出张量的高度和宽度。
        """
        B = x.shape[0]  # 获取批量大小
        x1 = self.in_conv(x)  # 输入卷积层
        x2 = self.down1(x1)  # 下采样模块1
        x3 = self.down2(x2)  # 下采样模块2
        x4 = self.down3(x3)  # 下采样模块3
        out, H, W = self.patch_embed4(x4)  # 补丁嵌入模块
        for i, blk in enumerate(self.block2):  # 循环处理双层路径自注意力机制模块
            out = blk(out, H, W)
        out = self.norm4(out)  # 归一化层
        x5 = out.reshape(B, H, W, -1).permute(0, 3, 1, 2).contiguous()  # 重塑形状

        out = F.relu(F.interpolate(self.dbn1(self.decoder1(x5)), scale_factor=(2, 2), mode='bilinear'))  # 上采样和卷积操作
        _, _, H, W = out.shape  # 获取输出张量的形状
        out = out.flatten(2).transpose(1, 2)  # 重塑形状
        for i, blk in enumerate(self.dblock2):  # 循环处理双层路径自注意力机制模块
            out = blk(out, H, W)
        out = self.dnorm4(out)  # 归一化层
        x = out.reshape(B, H, W, -1).permute(0, 3, 1, 2).contiguous()  # 重塑形状

        x = self.up1(x, x4)  # 上采样模块1
        x = self.up2(x, x3)  # 上采样模块2
        x = self.up3(x, x2)  # 上采样模块3
        x = self.up4(x, x1)  # 上采样模块4
        logits = self.out_conv(x)  # 输出卷积层

        return {"logits": logits}  # 返回包含模型输出的字典


if __name__ == '__main__':
    # 在主程序中，实例化模型并进行测试
    model = UNext(num_classes=3)  # 实例化模型，设置分类数为 3
    x = torch.randn(2, 3, 512, 512)  # 创建随机输入张量
    print(model(x).shape)  # 打印模型的输出形状
