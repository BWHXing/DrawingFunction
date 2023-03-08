import tkinter as tk
import pyautogui as ag
from tkinter import ttk
from numpy import arange as np
from sympy import symbols, Eq, solve
from tkinter import messagebox
from math import *

canvas_x = 330  # 画布x轴像素长度
canvas_y = 330  # 画布y轴像素长度
origin = (165, 165)  # 原点的x, y像素值 - 原点中心值为(160, 120)
xmax=8
w=h=165
unit_length_x = 25  # 坐标轴中x的比例长度
unit_length_y = 25  # 坐标轴中y的比例长度
coordinate_x = origin[1]  # 坐标轴 x (在y轴上的)的位置
coordinate_y = origin[0]  # 坐标轴 y (在x轴上的)的位置
# Colored_egg = 0

def Window_Open(W, H):
    X, Y = ag.size()
    winSize = str(W)+"x"+str(H)
    winPos = winSize + "+" + str((X - W) // 2)
    winPos += "+" + str((Y - H) // 2)
    win.geometry(winPos)
    win.resizable(False, False)
    title = u'桌面分辨率：' + str(X) + "x" + str(Y)
    title += ' ' * 5 + u'窗体大小：' + winSize
    win.title(title)
    win.update()

def Graph(func,x0,y0,xmin,xmax,w,h,c='blue',step=0.001):
    'xmin,xmax 自变量的取值范围； c 图像颜色'
    'x0,y0 原点坐标  w,h 横纵轴半长 step 步进'
    w1,w2=25,25 # w1,w2为自变量和函数值在横纵轴上的放大倍数
    for x in np(xmin,xmax+step,step):
        y = func(x)
        coord = x0+w1*x,y0-w2*y,x0+w1*x+1,y0-w2*y+1
        if abs(x*w1)<w and abs(y*w2)<h:
            tCanvas.create_line(coord,fill=c)
    tCanvas.update()

def init():
    tCanvas.create_line(0, coordinate_x, canvas_x, coordinate_x, fill='black', arrow=tk.LAST) # tk.LAST画箭头
    tCanvas.create_line(coordinate_y, canvas_y, coordinate_y, 0, fill='black', arrow=tk.LAST)
    tCanvas.create_line(coordinate_x-4, coordinate_y, coordinate_x+5, coordinate_y, fill='red')
    tCanvas.create_line(coordinate_x, coordinate_y-4, coordinate_x, coordinate_y+5, fill='red')

    for i in range( -ceil((coordinate_y / unit_length_x)) + 1, ceil((canvas_x-coordinate_y) / unit_length_x)):
        # print(i)
        if i==0:
            continue
        j = i*unit_length_x
        # 对于 i*unit_length_x即是获得了实际的坐标轴对应的放大unit_length倍后的值，但是这个值并不是真正的像素点
        # 由于我们是以中心点(coordinate_y, coordinate_x)为原点的，因此我们要在这里加上对应的原点像素值才能得到真正的坐标轴对应的像素点
        tCanvas.create_line(j+coordinate_y, coordinate_x, j+coordinate_y, coordinate_x-5, fill='red')
        tCanvas.create_text(j+coordinate_y, coordinate_x+10, text=i)
    # 同理由于y轴是相反的，所以正半轴为：cordinate_x，负半轴为canvas_y - cordinate_x
    # 此处的算法应该改为range*( -(canvas_y - coordinate_x) / unit_length_y) + 1, (cordinate_x / unit_length_y)) )
    for i in range( -ceil((canvas_y - coordinate_x) / unit_length_y) + 1, ceil((coordinate_x / unit_length_y))):
        if i==0:
            continue
        # print(i)
        j = i*unit_length_y
        # 对于 i*unit_length_y即是获得了实际的坐标轴对应的放大unit_length倍后的值，但是这个值并不是真正的像素点
        # 由于我们是以中心点(coordinate_y, coordinate_x)为原点的，因此我们要在这里加上对应的原点像素值才能得到真正的坐标轴对应的像素点
        tCanvas.create_line(coordinate_y, j+coordinate_x, coordinate_y+5, j+coordinate_x, fill='red')
        tCanvas.create_text(coordinate_y-10, j+coordinate_x, text=-i)

def mod1(a, b):
    x,y=float(a),float(b)
    # 反比例函数
    go = x * y
    return go

def mod2(a1, b1, a2, b2):
    x1,y1,x2,y2=float(a1),float(b1),float(a2),float(b2)
    # print(x1,y1,x2,y2)
    # 一次函数
    k = (y2 - y1) / (x2 - x1)
    b = y1 - x1 * k
    go = [k, b]
    return go

def mod3(a1, b1, a2, b2, a3, b3):
    x1,y1,x2,y2,x3,y3=float(a1),float(b1),float(a2),float(b2),float(a3),float(b3)
    a, b, c = symbols('a,b,c')
    eq1 = Eq((a*x1*x1 + b*x1 + c), y1)
    eq2 = Eq((a*x2*x2 + b*x2 + c), y2)
    eq3 = Eq((a*x3*x3 + b*x3 + c), y3)
    go = solve((eq1, eq2, eq3), (a, b, c))
    return go


def readonly_init(num=0):
    clean()
    if num==0:
        C_x.config(state='readonly')
        C_y.config(state='readonly')
    elif num==1:
        B_x.config(state='readonly')
        B_y.config(state='readonly')
        C_x.config(state='readonly')
        C_y.config(state='readonly')
    elif num==2:
        ...
    elif num==3:
        A_y.config(state='readonly')
        B_y.config(state='readonly')
        C_x.config(state='readonly')
        C_y.config(state='readonly')
    elif num==4:
        A_y.config(state='readonly')
        B_y.config(state='readonly')
        C_y.config(state='readonly')
    elif num==5:
        A_x.config(state='readonly')
        A_y.config(state='readonly')
        B_x.config(state='readonly')
        B_y.config(state='readonly')
        C_x.config(state='readonly')
        C_y.config(state='readonly')

def clean():
    A_x.config(state='normal')
    A_y.config(state='normal')
    B_x.config(state='normal')
    B_y.config(state='normal')
    C_x.config(state='normal')
    C_y.config(state='normal')

def normal_init(event=0):
    clean()
    if cbox.get()=='描点：y=kx+b':
        C_x.delete(0, tk.END)
        C_y.delete(0, tk.END)
        readonly_init()
    elif cbox.get()=='描点：y=k/x':
        B_x.delete(0, tk.END)
        B_y.delete(0, tk.END)
        C_x.delete(0, tk.END)
        C_y.delete(0, tk.END)
        readonly_init(1)
    elif cbox.get()=='描点：y=ax^2+bx+c':
        readonly_init(2)
    elif cbox.get()=='系数：一次函数k b':
        A_y.delete(0, tk.END)
        B_y.delete(0, tk.END)
        C_x.delete(0, tk.END)
        C_y.delete(0, tk.END)
        readonly_init(3)
    elif cbox.get()=='系数：二次函数a b c':
        A_y.delete(0, tk.END)
        B_y.delete(0, tk.END)
        C_y.delete(0, tk.END)
        readonly_init(4)
    # elif cbox.get()=='自定义...':
    #     readonly_init(5)

def Point(fx1,num=0):
    if num==0:
        a_x_=float(A_x.get())
        a_y_=fx1(a_x_)
        a_x,a_y=a_x_*25,a_y_*25
        tCanvas.create_line(coordinate_x+a_x, coordinate_y-a_y, coordinate_x+a_x+1, coordinate_y-a_y-1, fill='red')
        tCanvas.create_text(coordinate_x+a_x, coordinate_y-a_y-10, text='A', fill='red',font=('宋体',14))
    elif num==1:
        a_x_=float(A_x.get())
        a_y_=fx1(a_x_)
        a_x,a_y=a_x_*25,a_y_*25
        tCanvas.create_line(coordinate_x+a_x, coordinate_y-a_y, coordinate_x+a_x+1, coordinate_y-a_y-1, fill='red')
        tCanvas.create_text(coordinate_x+a_x, coordinate_y-a_y-10, text='A', fill='red',font=('宋体',14))
        b_x_=float(B_x.get())
        b_y_=fx1(b_x_)
        b_x,b_y=b_x_*25,b_y_*25
        tCanvas.create_line(coordinate_x+b_x, coordinate_y-b_y, coordinate_x+b_x+1, coordinate_y-b_y-1, fill='red')
        tCanvas.create_text(coordinate_x+b_x, coordinate_y-b_y-10, text='B', fill='red',font=('宋体',14))
    elif num ==2:
        a_x_=float(A_x.get())
        a_y_=fx1(a_x_)
        a_x,a_y=a_x_*25,a_y_*25
        tCanvas.create_line(coordinate_x+a_x, coordinate_y-a_y, coordinate_x+a_x+1, coordinate_y-a_y-1, fill='red')
        tCanvas.create_text(coordinate_x+a_x, coordinate_y-a_y-10, text='A', fill='red',font=('宋体',14))
        b_x_=float(B_x.get())
        b_y_=fx1(b_x_)
        b_x,b_y=b_x_*25,b_y_*25
        tCanvas.create_line(coordinate_x+b_x, coordinate_y-b_y, coordinate_x+b_x+1, coordinate_y-b_y-1, fill='red')
        tCanvas.create_text(coordinate_x+b_x, coordinate_y-b_y-10, text='B', fill='red',font=('宋体',14))
        c_x_=float(C_x.get())
        c_y_=fx1(c_x_)
        c_x,c_y=c_x_*25,c_y_*25
        tCanvas.create_line(coordinate_x+c_x, coordinate_y-c_y, coordinate_x+c_x+1, coordinate_y-c_y-1, fill='red')
        tCanvas.create_text(coordinate_x+c_x, coordinate_y-c_y-10, text='C', fill='red',font=('宋体',14))

def dray_a():
    tCanvas.delete("all")
    init()
    step=0.005
    num=0
    if cbox.get()=='描点：y=kx+b':
        kb=mod2(A_x.get(),A_y.get(),B_x.get(),B_y.get())
        BD.set('y='+str(format(kb[0],'.3f'))+'x+'+str(format(kb[1],'.3f')))
        fx1 = lambda x : kb[0]*x+kb[1]
        num=1
    elif cbox.get()=='描点：y=k/x':
        kb=mod1(A_x.get(),A_y.get())
        BD.set('y='+str(format(kb,'.3f'))+'/x')
        fx1 = lambda x : kb / x
    elif cbox.get()=='描点：y=ax^2+bx+c':
        step=0.01
        abc=mod3(A_x.get(),A_y.get(),B_x.get(),B_y.get(),C_x.get(),C_y.get())
        a,b,c= symbols('a b c')
        BD.set('y='+str(format(abc[a],'.3f'))+'xx+'+str(format(abc[b],'.3f'))+'x+'+str(format(abc[c],'.3f')))
        fx1 = lambda x : abc[a]*x*x + abc[b]*x + abc[c]
        num=2
    elif cbox.get()=='系数：一次函数k b':
        kb=float(A_x.get()),float(B_x.get())
        BD.set(f'y={kb[0]}x+{kb[1]}')
        fx1 = lambda x : kb[0]*x + kb[1]
        num=3
    elif cbox.get()=='系数：二次函数a b c':
        abc=float(A_x.get()),float(B_x.get()),float(C_x.get())
        BD.set(f'y={abc[0]}xx+{abc[1]}x+{abc[2]}')
        fx1 = lambda x : abc[0]*x*x + abc[1]*x + abc[2]
        num=3
    # elif cbox.get()=='自定义...':
    #     newWindow = tk.Toplevel(app)
    #     labelExample = tk.Label(newWindow, text = "New Window")
    #     buttonExample = tk.Button(newWindow, text = "New Window button")

    #     labelExample.pack()
    #     buttonExample.pack()

    Graph(fx1,coordinate_x,coordinate_y,-xmax,xmax,w,h,'blue',step)
    Point(fx1,num)

def clear_a():
    tCanvas.delete("all")
    init()
    A_x.delete(0, tk.END)
    A_y.delete(0, tk.END)
    B_x.delete(0, tk.END)
    B_y.delete(0, tk.END)
    C_x.delete(0, tk.END)
    C_y.delete(0, tk.END)
    cbox.current(0)
    normal_init()
    BD.set('')

def about_a():
    # print(Colored_egg)
    messagebox.showinfo(title='关于', message=
        '前三种模式下输入框从上到下分别是A点的xy坐标,B点的xy坐标,C点的xy坐标\n第四种模式是一次函数的k值和b值第五种则是二次函数的abc值\n\n作者：建宁实验中学2004班易冠宇\nGitHub用户名：BWHXing'
        )
    # if Colored_egg==11:
    #     messagebox.showinfo(title='彩蛋', message='没啥用小彩蛋')
    # Colored_egg+=1

if __name__ == '__main__':
    win = tk.Tk()
    Window_Open(480,360)

    BD = tk.StringVar()
    labela = tk.Label(win,text="表达式",textvariable=BD,font=('宋体',16,'bold'),width=25)
    labela.grid(row=0,column=0,columnspan=4,rowspan=1)

    cbox = ttk.Combobox(win,width=16)
    cbox['state'] = 'readonly'
    cbox.grid(row=0,column=4,columnspan=2)
    cbox['value'] = ('描点：y=kx+b','描点：y=k/x','描点：y=ax^2+bx+c','系数：一次函数k b','系数：二次函数a b c')
    cbox.current(0)

    A=tk.Label(win,text="A",font=('宋体',14,'bold')).grid(row=1,column=4,columnspan=2)
    A_x=tk.Entry(win)
    A_y=tk.Entry(win)
    A_x.grid(row=2, column=4,columnspan=2)
    A_y.grid(row=3, column=4,columnspan=2)

    B=tk.Label(win,text="B",font=('宋体',14,'bold')).grid(row=4,column=4,columnspan=2)
    B_x=tk.Entry(win)
    B_y=tk.Entry(win)
    B_x.grid(row=5, column=4,columnspan=2)
    B_y.grid(row=6, column=4,columnspan=2)

    C=tk.Label(win,text="C",font=('宋体',14,'bold')).grid(row=7,column=4,columnspan=2)
    C_x=tk.Entry(win)
    C_y=tk.Entry(win)
    C_x.grid(row=8, column=4,columnspan=2)
    C_y.grid(row=9, column=4,columnspan=2)


    dray_b=tk.Button(win, text="绘制",command=dray_a, width=8).grid(row=10, column=4)
    clear_b=tk.Button(win, text="清除",command=clear_a, width=8).grid(row=10, column=5)
    about_b=tk.Button(win, text="关于",command=about_a, width=8).grid(row=11, column=4,columnspan=2)

    tCanvas = tk.Canvas(win,
                   bg='#c7ecee',
                   height=330,
                   width=330)
    tCanvas.grid(row=1, column=0,rowspan=11)

    readonly_init()
    init()
    cbox.bind('<<ComboboxSelected>>', normal_init)
    
    win.mainloop()
    