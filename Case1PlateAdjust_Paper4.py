"""
The intention of this script is to adjust the initial imperfection of a solo plate - 4-simply support case 1.
Created by Y. CHENG in August 2024.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os,sys
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
・Adjusted model's inp file
・edges figures
"""


plate_b = 1200

def SelectFile():
# Displaying a file dialog
# Function for specifying a file
    def inpdialog_clicked():
        fTyp = [("", "*.inp")]
        iFile = os.path.dirname(__file__)
        iFilePath1 = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
        entry1.set(iFilePath1)
    def anldialog_clicked():
        fTyp = [("", "*.csv")]
        iFile = os.path.dirname(__file__)
        iFilePath2 = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
        entry2.set(iFilePath2)

    # 実行ボタン押下時の実行関数
    def conductMain():
        global filepath
        inpPath = entry1.get()
        anlPath = entry2.get()
        if  inpPath != "" and anlPath != "":
            filepath = (inpPath,anlPath)
            root.quit()
        else:
            messagebox.showerror("error", "No path setting")
            sys.exit()

    root = Tk()
    root.title("File References")


    # Frame1
    frame1 = ttk.Frame(root, padding=10)
    frame1.grid(row=2, column=1, sticky=E)
    inpLabel = ttk.Label(frame1, text="INP file＞＞", padding=(5, 2))
    inpLabel.pack(side=LEFT)
    entry1 = StringVar()
    inpEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
    inpEntry.pack(side=LEFT)
    inpButton = ttk.Button(frame1, text="Reference", command=inpdialog_clicked)
    inpButton.pack(side=LEFT)

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
    frame3.grid(row=7,column=1,sticky=W)
    # execute button setting
    button1 = ttk.Button(frame3, text="Execute", command=conductMain)
    button1.pack(fill = "x", padx=30, side = "left")
    # cancel button setting
    button2 = ttk.Button(frame3, text="Close", command=sys.exit)
    button2.pack(fill = "x", padx=30, side = "left")
    root.mainloop()


def sinWave_change(df):
    # initial imperfection
    # w0 (x, y) = alpha0 * w0max * (sin (pi/b) * x ) * (sin (pi/b) * y )
    alpha0 = 1.0
    global plate_b
    w0max = plate_b / 150
    return alpha0 * w0max * np.sin(np.pi * df.loc[:,'X'] / plate_b) * np.sin(np.pi * df.loc[:,'Y'] / plate_b)


def edge_def_draw(a_df,edgename,pdffile):
# figures format setting
    font = {'family': 'serif', 'serif': 'Times New Roman', 'size': 12}
    plt.rc('font', **font)
    fig = plt.figure()
    
    if a_df.equals(dfplate_edgeX):
        plt.scatter(a_df.loc[:,'X'].to_list(), a_df.loc[:,'sinWave'].to_list(), c="gray", label="Target_SinWave",marker=".",s=9)
        plt.scatter(a_df.loc[:,'X'].to_list(), a_df.loc[:,'analysis'].to_list(), c="red", label="Analysis",marker=".",s=9)
        plt.scatter(a_df.loc[:,'X'].to_list(), a_df.loc[:,'Z'].to_list(), c="blue", label="Calculated",marker=".",s=9)
        plt.grid(axis="x")
        plt.xlabel("x (mm)", size = "large")
        plt.ylabel("Deformation (mm)", size = "large")
        plt.xlim(0, 600.0)
        plt.ylim(-0.5, 10.0)
        num_nodes = len(dfplate_edgeX)
        plt.legend(title=edgename + f' ({num_nodes } nodes)')
        pdffile.savefig(fig)
    else:
        plt.scatter(a_df.loc[:,'Y'].to_list(), a_df.loc[:,'sinWave'].to_list(), c="gray", label="Target_SinWave",marker=".",s=9)
        plt.scatter(a_df.loc[:,'Y'].to_list(), a_df.loc[:,'analysis'].to_list(), c="red", label="Analysis",marker=".",s=9)
        plt.scatter(a_df.loc[:,'Y'].to_list(), a_df.loc[:,'Z'].to_list(), c="blue", label="Calculated",marker=".",s=9)
        plt.grid(axis="x")
        plt.xlabel("y (mm)", size = "large")
        plt.ylabel("Deformation (mm)", size = "large")
        plt.xlim(0, 600.0)
        plt.ylim(-0.5, 10.0)
        num_nodes = len(dfplate_edgeY)
        plt.legend(title=edgename + f' ({num_nodes } nodes)')
        pdffile.savefig(fig)
    return None


if __name__ == "__main__":
    # select Excel and input file 
    SelectFile()
    inputfile, analysisfile = filepath
    
    # read original input data 
    with open(inputfile,'r') as ifile:
        l = ifile.readlines()
        for index,line in enumerate(l):
            if '*Element' in line:
                coord_index = index
                break
        otherdata1 =  l[:11]
        data = l[11:coord_index]
        otherdata2 =  l[coord_index:]
    # write data into CSV file 
      
    with open('temp1.csv','w') as cfile:
        for d in data:
            cfile.write(d)

    #------------------------------------------------------------------------------------------------------------------------------
    # read and manipulate analysis deformation data
    # a_df = pd.read_csv(analysisfile, skiprows=1, encoding='utf-8')
    a_df = pd.read_csv(analysisfile, skiprows=0, encoding='shift-jis')
    a_df.columns = ['-','-','-','-','label','X','Y','Z','-','-','-','U1','U2','U3']
    
    a_df['X'] = pd.to_numeric(a_df['X'], errors='coerce')
    a_df['Y'] = pd.to_numeric(a_df['Y'], errors='coerce')
    a_df['Z'] = pd.to_numeric(a_df['Z'], errors='coerce')
    a_df['U3'] = pd.to_numeric(a_df['U3'], errors='coerce')

    a_df = a_df.loc[:,['label','X','Y','Z','U3']] #select what we need
    a_df = a_df.query('0 <= Y <= @plate_b/2')
    print(a_df)

    a_df['analysis'] = a_df['U3'] #based on 'label','X','Y','Z' added new colum
    a_df['sinWave'] = pd.to_numeric(sinWave_change(a_df))
    a_df['calculated'] = a_df['Z'] - (a_df['analysis'] - a_df['sinWave']) #add new column 'calculated'

    # print(a_df.head())
    
    #------------------------------------------------------------------------------------------------------------------------------
    # select plate edge for figure 
    # X=0~300mm, Symmetrical along the x-axis
    dfplate_edgeX = a_df.query('Y == @plate_b/2')
    # dfplate_edgeX = a_df.query('Z == 0.0 and Y == @plate_b/2')
    # Y=0~300mm, Symmetrical along the y-axis
    dfplate_edgeY = a_df.query('X == @plate_b/2')
    # dfplate_edgeY = a_df.query('Z == 0.0 and X == @plate_b/2')
    
    dfplate_edgeX = dfplate_edgeX.loc[:, ['label', 'X', 'Y', 'calculated','analysis','sinWave']]
    dfplate_edgeX = dfplate_edgeX.sort_values(by='X', ascending=True).rename(columns={'calculated': 'Z'})

    dfplate_edgeY = dfplate_edgeY.loc[:, ['label', 'X', 'Y', 'calculated','analysis','sinWave']]
    dfplate_edgeY = dfplate_edgeY.sort_values(by='Y', ascending=True).rename(columns={'calculated': 'Z'})
    # print(dfplate_edgeX.head())
    # print(dfplate_edgeY.head())

    # draw edges figures
    # pdfname = 'E:\\Docteral Doc\\paper4\\initial_imperfection\\Initial deformation plate.pdf'
    pdfname = 'C:\\Users\\cheng\\Desktop\\Docteral Doc\\paper4\\initial_imperfection\\200\\ID_ID_200ShellModel.pdf'
    pp = PdfPages(pdfname)
    edgeX = edge_def_draw(a_df=dfplate_edgeX, edgename='X plus direction', pdffile=pp)
    edgeY = edge_def_draw(a_df=dfplate_edgeY, edgename='Y plus direction', pdffile=pp)
    pp.close()
    #------------------------------------------------------------------------------------------------------------------------------

    # read original coordinates of model
    df = pd.read_csv('temp1.csv', header=None, on_bad_lines='skip')
    df.columns = ['label','X','Y','Z']
    # update to the new coordinates of model
    for j, i in enumerate(a_df['label']):
        df.iat[int(i) - 1, 3] = a_df.iat[j, 7]


    # update the new coordinates 
    df = df.applymap(lambda x: round(x,8))
    df = df.astype(str)
    for i in ('X','Y','Z'):
        df[i] = df[i].apply(lambda x: x.rstrip('0'))
    df['label'] = df['label'].apply(lambda x: x.rjust(7))
    for i in ('X','Y','Z'):
        df[i] = df[i].apply(lambda x: x.rjust(13))

    # write new input file data
    df.to_csv('temp2.csv', index=False, header=False)
    with open('temp2.csv','r') as file:
        data = file.readlines()
    with open(os.path.join(os.path.dirname(__file__),'ID_'+ os.path.basename(inputfile)),'w') as file:
        for d in otherdata1+data+otherdata2:
            file.write(d)
    #os.remove('temp1.csv')
    #os.remove('temp2.csv')
    # (please open the 'temp2.csv' and check every data is without 'nan' value)

print ('Completed')
try:
    subprocess.Popen(pdfname, shell=True)
except:
    print('Close pdf')