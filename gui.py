import os
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from Nougat import pre_read
from PDF_query import query
import shutil
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import markdown2

class Application(Frame):
    """Application Class"""
    target_file_path = "path"
    mmd_path = "default"

    def __init__(self, master=None):
        super().__init__(master)
        self.frame3 = None
        self.button_quit = None
        self.text = None
        self.frame2 = None
        self.frame1 = None
        self.button_analyse = None
        self.button_read = None
        self.button_PDF = None
        self.entry_PDF = None
        self.label_PDF = None
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):

        self.frame1 = Frame(root)  # first frame
        self.frame1.pack(side="top")
        """select file"""
        self.label_PDF = Label(self.frame1, text="目标路径:")
        self.label_PDF.pack(side="left")
        self.entry_PDF = Entry(self.frame1, textvariable=path, width=50)
        self.entry_PDF.pack(side="left")
        self.button_PDF = Button(self.frame1, text="路径选择", command=self.selectPDF)
        self.button_PDF.pack(side="left")

        self.frame2 = Frame(root)  # second frame
        self.frame2.pack(side="top")
        """read context"""
        self.button_read = Button(self.frame2, text="上传", command=self.nougatRun)
        self.button_read.pack(side="left")
        """analyse paper"""

        self.button_analyse = Button(self.frame2, text="获取分析结果", command=self.analysePaper)
        self.button_analyse.pack(side="left")
        self.frame3 = Frame(root)  # second frame
        self.frame3.pack(side="top")
        self.text = Text(self.frame3)
        self.text.pack()

        """clear cookies"""
        self.button_quit = Button(self.frame3, text="Quit", command=self.on_closing)
        self.button_quit.pack(side="bottom")

    def on_closing(self):
        # 窗口关闭时执行清除操作
        self.clear_and_quit()
        self.master.destroy()

    def selectPDF(self):
        self.target_file_path = askopenfilename(title="Select PDF file", filetypes=(("pdf files", "*.pdf"),))
        path.set(self.target_file_path)
        # print(self.target_file_path)

    def nougatRun(self):
        """load file"""
        source_path = self.target_file_path
        destination_path = "files/temporary.pdf"
        try:
            # 使用 shutil.copy() 函数复制文件
            shutil.copy(source_path, destination_path)
            print(f"文件 {source_path} 已成功上传 {destination_path}")
        except FileNotFoundError:
            print(f"找不到文件 {source_path}")
        except IsADirectoryError:
            print(f"{source_path} 是一个目录，无法上传")
        except shutil.SameFileError:
            print(f"目标文件已上传，无需重复上传")
        except PermissionError:
            print(f"没有权限读取文件 {source_path} 上传")
        except Exception as e:
            print(f"发生错误：{e}")
        pre_read(destination_path)
        self.mmd_path = os.path.splitext(destination_path)[0] + ".mmd"
        messagebox.showinfo("Message", "加载成功，请点击分析，大约需要1分钟")

    def analysePaper(self):
        """model process"""
        #result_text = query(self.mmd_path)
        test_text = """1) Title: Studying the Placement of EV Charging Stations in Parking Facilities in Cities
2) Authors: Jingpeng Ma, Qi He
3) Aim of the article: The aim of the article is to study different EV charger placement strategies in reducing traffic congestion in parking facilities in cities.
4) Methodology: The authors implemented a SUMO (Simulation of Urban Mobility) based approach to simulate and study the placement of EV charging stations. They used a Monte Carlo method to assess the average waiting time for drivers under different charger placement strategies.
5) Problem solved: The article addresses the problem of traffic congestion within parking facilities due to the allocation of EV chargers. It aims to find strategies to reduce congestion and improve the efficiency of EV charging.
6) Formulas used:
- Poisson distribution formula: \(P(X=k)=\frac{\lambda^{k}}{k!}e^{-\lambda}\) (Equation 1) - The authors use this formula to model the probability distribution of the number of cars arriving at a parking lot per unit time.
- Dijkstra algorithm - The authors use this algorithm to find the best path for route selection in the simulation.

Abstract:
The article focuses on studying the placement of EV charging stations in parking facilities in cities to reduce traffic congestion. The authors use a SUMO-based approach and a Monte Carlo method to simulate and assess different charger placement strategies. The research aims to contribute to the development of sustainable transportation systems and urban planning.

Introduction:
The introduction highlights the need for energy conservation and emission reduction in the automobile industry, leading to the adoption of EVs and the development of charging infrastructure. The authors mention the problems of charging station overload and traffic congestion within cities. They also discuss the specific challenges in China, such as the rapid growth of EVs and the insufficient and unbalanced construction of charging facilities.

Theoretical Foundations of Simulation:
This section explains the use of SUMO software for simulating traffic in Suzhou Industrial Park. The authors discuss the basic principles and advantages of SUMO, including its open-source nature, microscopic simulation capabilities, and the ability to import actual maps. They also describe the modeling of parking lots and charging facilities using SUMO, including the correction of road networks and the differentiation of regular parking spaces and spaces with charging stations.

Modeling of Traffic Conditions and Vehicle Flow:
The authors discuss the process of adding traffic flow to the simulated road network. They explain the use of the Poisson distribution to model the number of cars arriving at a parking lot per unit time. They also describe the use of the Dijkstra algorithm for route selection and the calculation of parking times for electric cars and gasoline cars.

Case Analysis:
The case analysis focuses on the feasibility analysis of the experiment in Suzhou Industrial Park. The authors highlight the car ownership and EV usage in Suzhou and the challenges of unbalanced planning and congestion in parking lots. They use the industrial park as an example to analyze parking activities during the evening rush hour.

Overall, the article aims to study the placement of EV charging stations in parking facilities to reduce traffic congestion. The authors use simulation and modeling techniques to assess different strategies and provide insights for sustainable transportation systems and urban planning.
"""
        # 创建一个Figure对象
        fig = plt.figure(figsize=(40, 30))
        plt.text(0, 0, test_text, ha='left', va='baseline', fontsize=10, multialignment='left')
        plt.axis('off')  # 关闭坐标轴

        # 创建FigureCanvasTkAgg对象，将Figure添加到Tkinter窗口
        canvas = FigureCanvasTkAgg(fig, master=self.frame3)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def clear_and_quit(self):
        directory_path = "files"  # 指定目录名称
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
        except FileNotFoundError:
            print(f"Directory not found: {directory_path}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x500+200+300")
    root.title("Paper Evaluator")
    path = StringVar()  # 将path移到类之外
    app = Application(master=root)

    app.mainloop()  # mainloop to monitor event
