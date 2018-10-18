from numpy import *
import operator




"""创建一个数据集，包含2个类别的四个样本"""
def createDataSet():
    #生成一个矩阵，每行表示一个样本
    group = array([[1.0,0.9],[1.0,1.0],[0.1,0.2],[0.0,0.1]])
    #4个样本分别所属的类别
    labels = ['A类','A类','B类','B类']

    return group,labels


"""KNN分类算法函数"""
def KNNClassify(newInput,dataSet,labels,k):
    numSamples = dataSet.shape[0]  #shape[0] 表示行数

    #step 1 计算距离
    #title(A,reps) :方法功能 构造一个矩阵，通过A重复reps次得到
    diff = tile(newInput,(numSamples,1)) - dataSet #按元素求差值
    squaredDiff = diff ** 2 #将差值平方
    squaredDist = sum(squaredDiff,axis=1) #按行累加
    distance = squaredDist ** 0.5 #将差值平方和求平方，即得距离

    #step 2 对距离排序
    #argsort()方法功能： 返回排序后的索引值
    sortedDistances = argsort(distance)
    classCount = {}
    for i in range(k):
        #step 3 选择k个最近邻
        voteLabel = labels[sortedDistances[i]]
        #step 4 计算k个最近邻中各类别出现的次数
        classCount[voteLabel] = classCount.get(voteLabel,0) + 1

    #step 5 返回最大的
    sortedClasCount = sorted(classCount.items(),key=operator.itemgetter(1))

    return  sortedClasCount[0][0]



if __name__ == "__main__":
    group,labels = createDataSet()
    test1 = [1.1,0.8]
    test2 = [0.5,0.8]
    k = 3
    test1KNN = KNNClassify(test1,group,labels,k)
    test2KNN = KNNClassify(test2,group,labels,k)

    print(test1KNN)