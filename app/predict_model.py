from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图
from math import e
import matplotlib
import numpy as np

class predict_model(object):
    #初始化函数
    #X_trian训练样本，考试次数和试卷难度系数
    #Y_train训练集结果，成绩
    #X_res预测输入
    #Y_res预测结果，默认为0
    #m样本数，会在迭代函数前自动获取
    #theta初始系数（1，1，1）
    #optimal最终theta集
    def __init__(self, *args, **kwargs):
        self.X_train = []
        self.Y_train = []
        self.X_res = []
        self.Y_res = 0
        self.m=0
        self.theta = np.array([1,1,1]).reshape(3,1)
        self.optimal = []
        #默认学习率为0.01
        self.alpha = 0.005
        #默认迭代深度为100000
        self.epoch = 50000
        return super().__init__(*args, **kwargs)

    #训练集获取
    def set_train(self,X_train,Y_train):
        self.X_train=X_train
        self.Y_train=Y_train
        self.m=len(self.X_train)
        X_marixadd=np.ones((self.m,1))
        self.X_train=np.hstack((X_train,X_marixadd))
        return 0

    #预测函数，type=0默认输出预测结果，为1时输出optimal
    def get_res(self,X_res,type=1):
        self.X_res = X_res
        self.set_model()
        self.Y_res = 50*(2/(1+e**-(self.optimal[0]*self.X_res[0]+self.optimal[1]*self.X_res[1]+self.optimal[2])))
        if type == 0:
            return self.Y_res
        if type == 1:
            return self.Y_res,self.optimal

    #模型拟合
    def set_model(self):
        self.optimal = self.gradient_descent()
        return 0

    #损失函数
    def cost_function(self):
        temp =100*(2/(1+e**np.dot(self.X_train,-self.theta))-1)-self.Y_train
        return (1/(2*self.m))*np.dot(temp.transpose(),temp)

    #梯度计算函数
    def gradient_function(self):
        temp =100*(2/(1+e**np.dot(self.X_train,-self.theta))-1)-self.Y_train
        return (1/self.m)*np.dot(self.X_train.transpose(),temp)

    #迭代函数
    def gradient_descent(self):
        gradient = self.gradient_function()
        for i in range(self.epoch):
            self.theta = self.theta - self.alpha * gradient
            gradient = self.gradient_function()
        return self.theta

    #可视化函数
    def draw_model(self):
        model1.set_model()
        fig=plt.figure(figsize=(14, 8))
        ax = Axes3D(fig)
        ax.scatter(self.X_train[:,0],self.X_train[:,1],self.Y_train)
        x=np.linspace(0,10,20)
        y=np.linspace(0,2,20)
        X_area,Y_area=np.meshgrid(x,y)
        Z=self.optimal[0]*X_area+self.optimal[1]*Y_area+self.optimal[2]
        ax.plot_surface(X_area,Y_area,Z=50*(2/(1+e**-Z)),color='y',alpha=0.5)
        ax.set_zlabel('Z', fontdict={'size': 15, 'color': 'red'})
        ax.set_ylabel('Y', fontdict={'size': 15, 'color': 'red'})
        ax.set_xlabel('X', fontdict={'size': 15, 'color': 'red'})
        plt.show()
        return 0

#测试
'''
X=[[1,0.98],[1,0.98],[1,0.98],[1,0.98],
   [2,1.0],[2,1.0],[2,1.0],[2,1.0],
   [3,0.97],[3,0.97],[3,0.97],[3,0.97],
   [4,1.01],[4,1.01],[4,1.01],[4,1.01],
   [5,1.05],[5,1.05],[5,1.05],[5,1.05],
   [6,1.03],[6,1.03],[6,1.03],[6,1.03]]
Y=[[82],[80],[90],[90],
   [79],[82],[82],[84],
   [89],[90],[91],[92],
   [80],[71],[78],[82],
   [63],[64],[66],[68],
   [70],[67],[69],[71],]

model1=predict_model()
model1.set_train(X,Y)
print(model1.get_res([7,1.05]))
'''