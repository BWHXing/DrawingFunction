# DrawingFunction函数绘制程序

## 创作目的

为了更好的帮助学习，快速而清晰的得到函数图像和解析式，我开发这这个程序

## 创作语言及环境

python-3.9.0-amd64

处理器    Intel(R) Core(TM) i5-3320M CPU @ 2.60GHz   2.60 GHz
机带 RAM    8.00 GB (7.88 GB 可用)
系统类型    64 位操作系统, 基于 x64 的处理器

版本    Windows 10 专业版
版本号    22H2
操作系统内部版本    19045.2604
体验    Windows Feature Experience Pack 120.2212.4190.0

## 创作用的模块

tkinte，pyautogui，numpy，sympy，math

**tkinte，math为固有模块无需安装，其余请打开install.bat进行安装**

## 主要功能

### 绘图

#### 主要绘图函数

```python
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
```

``np(xmin,xmax+step,step)``的np为numpy的arange函数

> numpy.arange(start, stop, step, dtype)

根据 start 与 stop 指定的范围以及 step 设定的步长，生成一个 ndarray。

[NumPy Ndarray 对象 | 菜鸟教程](https://www.runoob.com/numpy/numpy-ndarray-object.html)

这里则是用于生成x自变量的取值范围

将for循环中x的值带入匿名函数求出对应y的值

xy值需先乘以放大倍数使用

变量coord给出这次循环的坐标点，由于在tkinte的canvas画布中左上角为原点(0,0)，向右为x正半轴，向下为y正半轴，所以使用y值减去中点值(165,165)得到在canvas画布中y的值

[Python tkinter库之Canvas 根据函数解析式或参数方程画出图像](https://blog.csdn.net/boysoft2002/article/details/115311607)

#### 初始化坐标轴

```python
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
```

### 计算

##### 正比例函数

```python
def mod2(a1, b1, a2, b2):
    x1,y1,x2,y2=float(a1),float(b1),float(a2),float(b2)
    k = (y2 - y1) / (x2 - x1)
    b = y1 - x1 * k
    go = [k, b]
    return go
```

匿名函数``fx1 = lambda x : go[0]*x+go[1]``传入绘图函数进行绘制

##### 反比例函数

```python
def mod1(a, b):
    x,y=float(a),float(b)
    go = x * y
    return go
```

匿名函数``fx1 = lambda x : go[0]*x+go[1]``传入绘图函数进行绘制

##### 自定义kb值

无需计算，带入匿名函数``fx1 = lambda x : k*x + b``然后传入绘图函数即可

#### 二次函数

##### 抛物线

```python
def mod3(a1, b1, a2, b2, a3, b3):
    x1,y1,x2,y2,x3,y3=float(a1),float(b1),float(a2),float(b2),float(a3),float(b3)
    a, b, c = symbols('a,b,c')
    eq1 = Eq((a*x1*x1 + b*x1 + c), y1)
    eq2 = Eq((a*x2*x2 + b*x2 + c), y2)
    eq3 = Eq((a*x3*x3 + b*x3 + c), y3)
    go = solve((eq1, eq2, eq3), (a, b, c))
    return go
```

[sympy解算Eq 求解方程式_sympy eq](https://blog.csdn.net/t4ngw/article/details/105811002)

匿名函数``fx1 = lambda x : go[0]*x*x+go[1]*x+go[2]``传入绘图函数进行绘制

##### 自定义abc值

无需计算，带入匿名函数``fx1 = lambda x : a*x*x + b*x + c``然后传入绘图函数即可

### 其他

显示当前函数的表达式，根据使用的模式自动禁用输入框
