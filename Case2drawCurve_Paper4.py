"""
The intention of this script is to adjust the initial imperfection of a solo plate - 3-simply support 1-free case 2.
Created by Y. CHENG in January 2025.
"""
import pandas as pd
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os, sys
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess

"""
Input files:
・Input file (.inp file of the model to which you want to introduce initial deformation)
・Analysis result csv file(Can be generated directly in Abaqus: Report → Field Output)
Output files:
・edges figures (pdf)
"""


plate_b = 900
plate_l = 900

def SelectFile():
    def anldialog_clicked():
        fTyp = [("", "*.csv")]
        iFile = os.path.dirname(__file__)
        iFilePath2 = filedialog.askopenfilename(filetype=fTyp, initialdir=iFile)
        entry2.set(iFilePath2)

    # Function to be executed when the execute button is pressed
    def conductMain():
        global filepath
        anlPath = entry2.get()
        if anlPath != "":
            filepath = (anlPath)
            root.quit()
        else:
            messagebox.showerror("error", "No path setting")
            sys.exit()

    root = Tk()
    root.title("File References")

    # Frame2
    frame2 = ttk.Frame(root, padding=10)
    frame2.grid(row=4, column=1, sticky=E)
    anlLabel = ttk.Label(frame2, text="Original analysis file＞＞", padding=(5, 2))
    anlLabel.pack(side=LEFT)
    entry2 = StringVar()
    anlEntry = ttk.Entry(frame2, textvariable=entry2, width=30)
    anlEntry.pack(side=LEFT)
    anlButton = ttk.Button(frame2, text="Reference", command=anldialog_clicked)
    anlButton.pack(side=LEFT)

    # Frame3
    frame3 = ttk.Frame(root, padding=10)
    frame3.grid(row=7, column=1, sticky=W)
    # execute button setting
    button1 = ttk.Button(frame3, text="Execute", command=conductMain)
    button1.pack(fill="x", padx=30, side="left")
    # Cancel button setting
    button2 = ttk.Button(frame3, text="Close", command=sys.exit)
    button2.pack(fill="x", padx=30, side="left")
    root.mainloop()


def sinWave_change(df):
    # initial imperfection
    # w0 (x, y) = alpha0 * w0max * (sin (pi/b) * x ) * (sin (pi/b) * y )
    global plate_b
    global plate_l
    w0max = plate_b / 100
    return w0max * np.sin(np.pi * df.loc[:, 'Y'] / plate_l) * (df.loc[:, 'X'] / plate_b)


def edge_def_draw(a_df, edgename, pdffile):
    # figures format setting
    font = {'family': 'serif', 'serif': 'Times New Roman', 'size': 12}
    plt.rc('font', **font)
    fig = plt.figure()

    if a_df.equals(dfplate_edgeX):
        plt.scatter(a_df.loc[:, 'X'].to_list(), a_df.loc[:, 'sinWave'].to_list(), c="gray", label="Target_SinWave",
                    marker=".", s=9)
        plt.scatter(a_df.loc[:, 'X'].to_list(), a_df.loc[:, 'analysis'].to_list(), c="red", label="Analysis",
                    marker=".", s=9)
        plt.grid(axis="x")
        plt.xlabel("x (mm)", size="large")
        plt.ylabel("Deformation (mm)", size="large")
        plt.xlim(0, 500.0)
        plt.ylim(0, 8.0)
        plt.legend(title=edgename + f' ({len(a_df)}nodes)')
        pdffile.savefig(fig)
    else:
        plt.scatter(a_df.loc[:, 'Y'].to_list(), a_df.loc[:, 'sinWave'].to_list(), c="gray", label="Target_SinWave",
                    marker=".", s=9)
        plt.scatter(a_df.loc[:, 'Y'].to_list(), a_df.loc[:, 'analysis'].to_list(), c="red", label="Analysis",
                    marker=".", s=9)
        plt.grid(axis="x")
        plt.xlabel("y (mm)", size="large")
        plt.ylabel("Deformation (mm)", size="large")
        plt.xlim(0, 500.0)
        plt.ylim(0, 8.0)
        plt.legend(title=edgename + f' ({len(a_df)}nodes)')
        pdffile.savefig(fig)
    return None


if __name__ == "__main__":
    # select Excel file
    SelectFile()
    analysisfile = filepath

    # ------------------------------------------------------------------------------------------------------------------------------
    # read and manipulate analysis deformation data
    # a_df = pd.read_csv(analysisfile, skiprows=1, encoding='utf-8')
    a_df = pd.read_csv(analysisfile, skiprows=0, encoding='shift-jis')
    a_df.columns = ['-', '-', '-', '-', 'label', 'X', 'Y', 'Z', '-', '-', '-', 'U1', 'U2', 'U3']

    a_df['X'] = pd.to_numeric(a_df['X'], errors='coerce')
    a_df['Y'] = pd.to_numeric(a_df['Y'], errors='coerce')
    a_df['Z'] = pd.to_numeric(a_df['Z'], errors='coerce')
    a_df['U3'] = pd.to_numeric(a_df['U3'], errors='coerce')

    a_df = a_df.loc[:, ['label', 'X', 'Y', 'Z', 'U3']]  # select what we need
    a_df = a_df.query('0 <= X <= @plate_b')
    # print(a_df.head())

    a_df['analysis'] = a_df['U3']  # based on 'label','X','Y','Z' added new colum
    a_df['sinWave'] = pd.to_numeric(sinWave_change(a_df))
    #a_df['calculated'] = a_df['sinWave'] + a_df['analysis']  # 添加了新列calculated
    print(a_df.head())

    # ------------------------------------------------------------------------------------------------------------------------------
    # select plate edge for figure
    # X=0~300mm, Symmetrical along the x-axis
    dfplate_edgeX = a_df.query('Y == @plate_l/2')
    dfplate_edgeY = a_df.query('X == @plate_b')

    dfplate_edgeX = dfplate_edgeX.loc[:, ['label', 'X', 'Y', 'analysis', 'sinWave']]
    dfplate_edgeY = dfplate_edgeY.loc[:, ['label', 'X', 'Y', 'analysis', 'sinWave']]

    # draw edges figures
    # pdfname = 'E:\\Docteral Doc\\paper4\\initial_imperfection\\Initial deformation plate.pdf'
    pdfname = 'C:\\Users\\cheng\\Desktop\\Docteral Doc\\paper4\\initial_imperfection\\150\\ID_ID_ID_150figure.pdf'
    pp = PdfPages(pdfname)
    edgeX = edge_def_draw(a_df=dfplate_edgeX, edgename='X plus direction', pdffile=pp)
    edgeY = edge_def_draw(a_df=dfplate_edgeY, edgename='Y plus direction', pdffile=pp)
    pp.close()
    # ------------------------------------------------------------------------------------------------------------------------------


print('Completed')
try:
    subprocess.Popen(pdfname, shell=True)
except:
    print('Close pdf')
