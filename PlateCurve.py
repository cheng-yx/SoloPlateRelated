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


def euler_curve(R):
    return np.where(R <= 1.0, 1.0, 1 / R**2)

def m_curve(R):
    return np.where(R <= 0.571, 1.0, 0.968 / R - 0.286 / R**2 + 0.0338 / R**3)

def m_2s_curve(R):
    return np.where(R <= 0.389, 1.0, -0.174 + 0.968 / R - 0.286 / R**2 + 0.0338 / R**3)

def Nara(R):
    return np.where(R <= 0.451, 1.0, (0.451/R)**0.511 )

def road_bridge_curve(R):
    return np.where(R <= math.sqrt(0.5), 1.0, 0.5 / R**2)

def elasticPlasticFiniteDeformation(R): #弹塑性有限变位理论
    case1 = R <= 0.5
    case2 = (R > 0.5) & (R <= 1.0)
    case3 = (R > 1.0) & (R <= 2.1)
    result = np.where(
        case1,
        1.0,
        np.where(
            case2,
            0.390 * (R - 0.5) ** 2 - 0.911 * (R - 0.5) + 1.0,
            np.where(
                case3,
                (0.015/ (R - 0.8)) - 0.146 * R + 0.713,
                np.nan  # Handling R values outside the given range
            )))
    return result

# Analysis result
def analysisScatter_and_fit_curve(color, label_points, label_fit):
    # Data points for scatter
    x_points = np.array([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2.0]) # Confidential Data
    y_points = np.array([1.0, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2])

    # Polynomial fitting (degree 3)
    poly_coefficients = np.polyfit(x_points, y_points, deg=3)
    poly_fit = np.poly1d(poly_coefficients)

    # Generate fitted curve data
    x_fit = np.linspace(min(x_points), max(x_points), 100)
    y_fit = poly_fit(x_fit)

    plt.plot(x_points, y_points, 'o', label=label_points, c=color)
    # Plot fitted curve
    plt.plot(x_fit, y_fit, '--', label=label_fit, c=color, alpha=0.7)

    # Return the scatter points and fitted curve data
    return x_points, y_points, x_fit, y_fit


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
plt.plot(R, m_curve(R), label='Fukumoto et. al. M (1984)', c="black")
plt.plot(R, m_2s_curve(R), label='Fukumoto et. al. M-2S (1984)', c="gray")
plt.plot(R, Nara(R), label='Nara et. al(1988)', c="magenta")
plt.plot(R, road_bridge_curve(R), label='Specifications for Highway Bridges (2002)', c="blue")
plt.plot(R, elasticPlasticFiniteDeformation(R), label='Buckling Design Guidelines(2005)', c="green")
analysisScatter_and_fit_curve(
    color="orange",
    label_points="Analytical Results",
    label_fit="Fitted Curve (Analytical Results)")

# 添加图例
plt.xlim(0, 2.0)
plt.ylim(0, 2.65)
plt.legend(facecolor='white', edgecolor='black', framealpha=1, fancybox=False,
    prop={'size': 10})

# 添加标题和轴标签
plt.title(' ')
plt.xlabel('Width-Thickness Ratio Parameter R')
plt.ylabel('Sigma cr/Sigma y')

# 显示图形
plt.grid(True)
plt.xticks(np.arange(0, 2.1, 0.5))
plt.yticks(np.arange(0, 2.65, 0.2))
plt.show()
# pdfname = 'E:\\Docteral Doc\\paper4\\initial_imperfection\\Initial defomation plate.pdf'
# pdffile.savefig(fig)
