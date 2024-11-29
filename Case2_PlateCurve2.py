"""
The intention of this script is to draw the original curves of a solo plate.
Created by Y. CHENG in Oct 2024.
"""
import pandas as pd
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
import math

import numpy as np
import matplotlib.pyplot as plt

# 定义函数，这里是你具体的曲线公式
def euler_curve(R):
    return np.where(R <= 1.0, 1.0, 1 / R**2)

def elasticPlasticFiniteDeformation(R): #弹塑性有限变位理论
    case1 = R <= 0.5
    case2 = (R > 0.5) & (R <= 1.0)
    case3 = (R > 1.0) & (R <= 1.3)
    result = np.where(
        case1,
        1.0,
        np.where(
            case2,
            0.080 * (R - 0.5) ** 2 - 0.480 * (R - 0.5) + 1.0,
            np.where(
                case3,
                0.470 * R ** 2 - 1.340 * R + 1.650,
                np.nan  # Handling R values outside the given range
            )))
    return result

def UltiStress(R):#极限应力曲线 北田俊行et. al.
    return np.where(R <= 0.5, 1.0, 
                    0.571 * (R - 0.5)**2 - 1.01 * (R-0.5) + 1)


def basler_formula(R):
    sqrt_2 = np.sqrt(2)
    case1 = R <= 0.45
    case2 = (R > 0.45) & (R < sqrt_2)
    case3 = R >= sqrt_2
    result = np.where(
        case1,
        1.0,
        np.where(
            case2,
            1 - 0.53 * (R - 0.45) ** 1.36,
            np.where(
                case3,
                (1 / R) ** 2,
                np.nan
            )))
    return result

def Fukumoto(R):
    return np.where(R <= 0.7, 1.0, (0.7/R)**0.64)

def Usami(R): # with RS
    return np.where(R <= 0.389, 1.0, -0.174 + 0.968 / R - 0.286 / R**2 + 0.0338 / R**3)

def road_bridge_curve(R):
    return np.where(R <= math.sqrt(0.5), 1.0, 0.5 / R**2)

# 创建x轴的数据范围
x = np.linspace(0, 2, 1000)
R = np.linspace(0, 2, 1000)

# 创建图形和子图
# font = {'family': 'serif', 'serif': 'Times New Roman', 'size': 12}
font = {'family': 'serif', 'serif': 'Century Gothic', 'size': 12}
plt.rc('font', **font)
plt.figure(figsize=(6, 4))


# 绘制曲线
plt.plot(R, euler_curve(R), label='Euler Curve (1744)', c="red")
plt.plot(R, basler_formula(R), label='Basler et. al.(1961)', c="black")
plt.plot(R, Fukumoto(R), label='Fukumoto et. al.(1990)', c="magenta")
# plt.plot(R, Usami(R), label='Usami et. al. with RS(1996)', c="green")
# plt.plot(R, UltiStress(R), label='Ultimate Stress (北田俊行et. al.)', c="orange")
plt.plot(R, road_bridge_curve(R), label='Specifications for highway bridges(2002)', c="blue")
plt.plot(R, elasticPlasticFiniteDeformation(R), label='Buckling Design Guidelines(2005)', c="green")

# 添加图例
plt.xlim(0, 2.0)
plt.ylim(0, 2.5)
plt.legend(facecolor='white', edgecolor='black', framealpha=1, fancybox=False)

# 添加标题和轴标签
plt.title(' ')
plt.xlabel('Width-Thickness Ratio Parameter R')
plt.ylabel('Sigma cr/Sigma y')

# 显示图形
plt.grid(True)
plt.xticks(np.arange(0, 2.1, 0.5))
plt.yticks(np.arange(0, 2.7, 0.2))
plt.show()
# pdfname = 'E:\\Docteral Doc\\paper4\\initial_imperfection\\Initial defomation plate.pdf'
# pdffile.savefig(fig)
